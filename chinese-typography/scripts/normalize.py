#!/usr/bin/env python3
"""
台灣繁體中文排版正規化器 (Taiwan Traditional Chinese typography normalizer).

全部是確定性轉換，任何一步都不需要 LLM 判斷。
請用本腳本取代手工修改：它更快、更一致，而且可逆。

處理流程（順序有意義，每一步的理由見下方註解）：
  1. 保護 code / URL / 路徑 / 版本號 / email（這些絕不更動）
  2. OpenCC s2twp           簡體→繁體 ＋ 台灣慣用詞（選用相依套件，缺少時大聲警告）
  3. 異體字 / 常見錯字 修正  （小型精選對照表）
  4. 引號正規化              直引號／彎引號 → 「」『』
  5. 標點全形化              中文語境的半形標點 → ，。；：？！（）
  6. 盤古之白                中文與英文／數字之間補半形空格（自製 pangu）
  7. 空白清理                壓縮連續空白、修剪行尾
  8. 還原被保護的片段

用法：
  echo "文字" | python3 normalize.py                 # stdin → stdout
  python3 normalize.py FILE.md                        # 正規化後印到 stdout
  python3 normalize.py FILE.md --in-place             # 直接覆寫檔案
  python3 normalize.py FILE.md --diff                 # 只印 unified diff
  python3 normalize.py --text "中文abc"               # 直接處理單一字串
  python3 normalize.py FILE.md --no-convert           # 跳過 OpenCC 簡轉繁

各階段都能用旗標關閉：--no-convert --no-quotes --no-punct
--no-spacing --no-fixes。
"""
import argparse
import re
import sys

# ---------------------------------------------------------------------------
# 字元類別 (character classes)
# ---------------------------------------------------------------------------
# CJK 漢字 ＋ 假名 ＋ 注音。同時用於「盤古之白」間距判斷與「這是不是中文語境」
# 的標點判斷。刻意排除全形符號（＀-），因為那些是已正確的輸出，不是待轉換的輸入。
CJK = (
    r'⺀-⻿぀-ゟ゠-ヺー-ヿ'
    r'㄀-ㄯ㐀-䶿一-鿿豈-﫿'
)
ANY_CJK = re.compile(f'[{CJK}]')

# ---------------------------------------------------------------------------
# 第 1 步：保護絕不可改寫的片段
# ---------------------------------------------------------------------------
# 每個 pattern 命中的內容會被抽出，換成一個私用佔位符，最後再原樣還原。
# 這就是為什麼像 "8.2.10" 這種版本號、或 "src/a.py" 這種路徑，
# 能在標點全形化的過程中存活下來。
# 注意：字元類別刻意只用 ASCII。Python 的 \w 在 unicode 模式下會 match 到中文，
# 因此天真地用 \w 寫 URL／路徑 pattern 會貪婪地把 URL 後面的中文一起吃掉。
# 明確列出 ASCII 字元，能讓比對在遇到第一個中文字時就停下來，這才正確。
_PROTECT_PATTERNS = [
    re.compile(r'```.*?```', re.DOTALL),                       # 圍欄式 code block
    re.compile(r'`[^`\n]+`'),                                   # 行內 code
    re.compile(r"https?://[A-Za-z0-9\-._~:/?#@!$&'()*+;=%]+"),  # URL（不含結尾逗號，那多半是標點）
    re.compile(r'[A-Za-z0-9._+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+'),  # email
    re.compile(r'\d+(?:\.\d+)+'),                               # 版本號／小數鏈 3.14、8.2.10
    re.compile(r'(?:[A-Za-z0-9._-]+/)+[A-Za-z0-9._-]+'),        # 檔案路徑 a/b/c.py
    # 西文縮寫：句點屬於縮寫的一部分，整串保護，句點才不會被轉成 。
    re.compile(r'\b(?:Mr|Mrs|Ms|Dr|Jr|Sr|Prof|St|vs|etc|i\.e|e\.g|a\.k\.a|'
               r'No|Fig|Eq|Vol|p\.m|a\.m)\.', re.IGNORECASE),
]
# 佔位符必須是真實文字絕不會出現的字串，否則還原時會誤傷內文。
# 早期版本用 '{}'.format(i)（也就是裸數字 "0"、"1"…），結果還原時
# replace("0", …) 會把內文裡每一個 "0" 都換掉，像 "100" 就被毀掉了。
# 改用 Unicode 私用區 (PUA) 的哨符字元包住索引，正常文本不會有這些字元。
_PLACEHOLDER = '{}'


def _protect(text, extra_protect=None):
    store = []

    def stash(m):
        store.append(m.group(0))
        return _PLACEHOLDER.format(len(store) - 1)

    # 個人字典 protect 詞優先抽出（最長優先，避免子字串先被吃掉）。
    for term in sorted(extra_protect or [], key=len, reverse=True):
        if term:
            text = re.sub(re.escape(term), stash, text)
    for pat in _PROTECT_PATTERNS:
        text = pat.sub(stash, text)
    return text, store


def _restore(text, store):
    # 反向還原，巢狀的佔位符才能正確解開。
    for i in range(len(store) - 1, -1, -1):
        text = text.replace(_PLACEHOLDER.format(i), store[i])
    return text


# ---------------------------------------------------------------------------
# 第 2 步：OpenCC 簡轉繁（台灣）── 選用相依套件
# ---------------------------------------------------------------------------
# s2twp ＝ 簡體 → 繁體、台灣標準，並且做詞彙在地化
# （软件→軟體、鼠标→滑鼠、视频→影片）。這是一份很大的辭典，
# 不要嘗試自己手刻。若 OpenCC 缺席，我們大聲失敗（Rule 12），
# 讓呼叫端知道這段文字「沒有」被轉換，而不是默默讓簡體字溜過去。
_OPENCC_HINT = (
    "WARNING: OpenCC not installed — 簡轉繁/台灣用語 step SKIPPED. "
    "Text was NOT converted simplified→traditional. "
    "Install: pip install opencc-python-reimplemented"
)


def _opencc_convert(text):
    try:
        from opencc import OpenCC
    except ImportError:
        print(_OPENCC_HINT, file=sys.stderr)
        return text, False
    try:
        return OpenCC('s2twp').convert(text), True
    except Exception as e:  # 不同移植版的設定檔名稱不一
        for cfg in ('s2twp.json', 's2t'):
            try:
                return OpenCC(cfg).convert(text), True
            except Exception:
                continue
        print(f"WARNING: OpenCC present but conversion failed ({e}); text unchanged.",
              file=sys.stderr)
        return text, False


# ---------------------------------------------------------------------------
# 第 3 步：異體字 / 常見錯字 修正
# ---------------------------------------------------------------------------
# 精選且刻意保持精簡。這些是台灣標準字形選擇與高頻錯字，
# 並非完整的異體字表 ── 大部分 OpenCC 已經處理掉了。
# 之後若 eval 揪出真正的漏網之魚再擴充；每一條都要站得住腳。
#
# 台↔臺 有爭議：政府公文用 臺，但 台 在台灣極為通用且被接受
# （台灣、電視台、一台車）。預設偏好通用的 台。
# 麻煩的是 OpenCC s2twp 會把「所有」台都轉成 臺（連量詞「一台」也是），
# 所以預設要把它還原回 台；只有使用者明確要官方字形（--formal-tai）才保留 臺。
# 供 --no-convert 時補強用的地名對照表也一併保留。
_FORMAL_TAI = {'台灣': '臺灣', '台北': '臺北', '台中': '臺中', '台南': '臺南', '台東': '臺東'}
_ALWAYS_FIXES = {'裏': '裡'}   # 裏 → 裡（台灣標準字）


def _fix_variants(text, formal_tai=False):
    for a, b in _ALWAYS_FIXES.items():
        text = text.replace(a, b)
    if formal_tai:
        # 要官方字形：補強地名（OpenCC 已大致完成，這裡涵蓋 --no-convert 的情況）
        for a, b in _FORMAL_TAI.items():
            text = text.replace(a, b)
    else:
        # 預設：還原 OpenCC s2twp 一律轉出的 臺，回到通用的 台
        text = text.replace('臺', '台')
    return text


# ---------------------------------------------------------------------------
# 第 4 步：引號 → 「」『』
# ---------------------------------------------------------------------------
# 台灣慣例：主引號 「」、巢狀 『』（直角引號），而非中國大陸／西式的 ""''。
# 彎引號直接對應。直引號在同一行內成對配對；
# 落單的直引號保留不動（多半是縮寫的撇號或英寸符號）。
def _fix_quotes(text):
    text = text.replace('“', '「').replace('”', '」')   # “ ” → 「 」
    text = text.replace('‘', '『').replace('’', '』')   # ‘ ’ → 『 』
    # 同一行內成對的直雙引號 → 「」
    text = re.sub(r'"([^"\n]*)"', r'「\1」', text)
    return text


# ---------------------------------------------------------------------------
# 第 5 步：半形標點 → 全形，只在中文語境
# ---------------------------------------------------------------------------
# 只在標點緊鄰 CJK 時才轉全形，這樣英文句子與被保護的 code 都能毫髮無傷。
# 句點是特例：只有在 CJK 之後、且不是小數點時才轉 。（小數早已被保護）。
def _fix_punct(text):
    # 省略號／破折號（台灣 MOE 標準：…… 六點、—— 雙破折號）。
    # 必須在句點規則「之前」處理，否則 "..." 的點會被句點規則咬成 "。.。"。
    text = re.sub(r'…+', '……', text)                          # 全形省略號一律收斂成六點 ……
    text = re.sub(f'(?<=[{CJK}])\\.{{3,}}', '……', text)        # 中文後的 ... → ……
    text = re.sub(f'\\.{{3,}}(?=[{CJK}])', '……', text)         # 中文前的 ... → ……
    text = re.sub(r'。{3,}', '……', text)                       # 。。。 → ……
    text = re.sub(f'([{CJK}])\\s*-{{2,}}\\s*(?=[{CJK}])', r'\1——', text)  # 中文間 -- → ——
    text = re.sub(f'([{CJK}])\\s*—+\\s*(?=[{CJK}])', r'\1——', text)       # 中文間 — → ——
    pairs = [(',', '，'), (';', '；'), (':', '：'), ('?', '？'), ('!', '！')]
    for a, b in pairs:
        # 標點前面是 CJK
        text = re.sub(f'([{CJK}])\\s*{re.escape(a)}', rf'\1{b}', text)
        # 標點後面是 CJK（例如開頭語境）
        text = re.sub(f'{re.escape(a)}\\s*([{CJK}])', rf'{b}\1', text)
    # 句點 → 。只在緊接 CJK 之後、且後面不是數字／字母時
    text = re.sub(f'([{CJK}])\\s*\\.(?![0-9A-Za-z])', r'\1。', text)
    # 句點 → 。當它出現在 CJK 之前、且不是西文縮寫或清單/數字標記的一部分。
    # 用來抓被保護版本號後面的句末句點，例如 "2.31.0.然後" → "2.31.0。然後"
    # （版本號此時是佔位符，所以句點前面的字元是 "}"，不是字母／數字）。
    # look-behind 裡的數字正是用來保護 Markdown 有序清單標記：
    # "1. 記得…" 必須維持 "1."──轉成 "1。" 會破壞清單。
    text = re.sub(f'(?<![A-Za-z0-9])\\.\\s*(?=[{CJK}])', '。', text)
    # 括號：任一側碰到 CJK 時轉全形
    text = re.sub(f'\\(\\s*([^()\n]*?[{CJK}][^()\n]*?)\\)', r'（\1）', text)
    return text


# ---------------------------------------------------------------------------
# 第 6 步：盤古之白 ── 中文與英文／數字之間補空格（自製 pangu）
# ---------------------------------------------------------------------------
# 移植自廣為人知的 pangu.js 核心規則集。英文字母、數字、
# 以及少數符號，會在 CJK 那一側補上一個半形空格。
# 全形標點「不」補空格（它自帶視覺留白）。
# 只有英數字與數學／結構符號會觸發盤古之白。句末標點
# （, . ; : ! ? ~）刻意排除 ── 那是標點階段的工作。
# 若呼叫端傳 --no-punct，半形逗號就該原地不動，不該多出一個結尾空格。
_ANS = r'A-Za-z0-9'
_SYM = r'@$%^&*\-+=|/`'   # 反引號納入，讓行內 code 與中文之間也有盤古之白
_CJK_ANS = re.compile(f'([{CJK}])([{_ANS}{_SYM}])')
_ANS_CJK = re.compile(f'([{_ANS}{_SYM}])([{CJK}])')


def _pangu(text):
    text = _CJK_ANS.sub(r'\1 \2', text)
    text = _ANS_CJK.sub(r'\1 \2', text)
    return text


# ---------------------------------------------------------------------------
# 第 7 步：空白清理
# ---------------------------------------------------------------------------
def _cleanup(text):
    out = []
    for line in text.split('\n'):
        line = re.sub(r'[ \t]{2,}', ' ', line)       # 壓縮行內連續空白
        # 全形標點周圍不留空格
        line = re.sub(r'\s+([，。；：？！）」』])', r'\1', line)
        line = re.sub(r'([（「『])\s+', r'\1', line)
        out.append(line.rstrip())
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# 全形英數 → 半形 (full-width ASCII letters/digits → half-width)
# ---------------------------------------------------------------------------
# 從別處貼來的文字常夾雜全形英數（Ａ３），轉回半形才能正確套盤古之白與大小寫。
# 只動英數，不碰全形標點（那是我們刻意要的中文標點）。
def _to_halfwidth(text):
    return ''.join(
        chr(ord(c) - 0xFEE0) if '！' <= c <= '～' and (
            c.isalnum()) else c
        for c in text
    )


# ---------------------------------------------------------------------------
# 專有名詞大小寫 (proper-noun casing)
# ---------------------------------------------------------------------------
# 中文文案排版指北 rule 10：技術專有名詞用正規大小寫。精選、保守，
# 只收幾乎一律固定寫法的品牌／縮寫；用詞界線比對，避免誤傷英文內文。
# 使用者可用個人字典擴充（見 user-dictionary.json，權限最高）。
_CASING = {
    'github': 'GitHub', 'gitlab': 'GitLab', 'javascript': 'JavaScript',
    'typescript': 'TypeScript', 'nodejs': 'Node.js', 'node.js': 'Node.js',
    'ios': 'iOS', 'ipados': 'iPadOS', 'macos': 'macOS', 'iphone': 'iPhone',
    'ipad': 'iPad', 'android': 'Android', 'php': 'PHP', 'mysql': 'MySQL',
    'postgresql': 'PostgreSQL', 'graphql': 'GraphQL', 'html': 'HTML',
    'css': 'CSS', 'json': 'JSON', 'api': 'API', 'url': 'URL', 'sql': 'SQL',
    'youtube': 'YouTube', 'wifi': 'Wi-Fi',
}


def _fix_casing(text, extra=None):
    table = dict(_CASING)
    if extra:
        table.update({k.lower(): v for k, v in extra.items()})  # 使用者覆寫內建
    for low, canon in table.items():
        # 詞界線比對、忽略大小寫；只在整個 token 與 key 相同時替換。
        text = re.sub(rf'(?<![A-Za-z0-9.]){re.escape(low)}(?![A-Za-z0-9])',
                      canon, text, flags=re.IGNORECASE)
    return text


# ---------------------------------------------------------------------------
# 個人字典 (user dictionary) — 權限最高
# ---------------------------------------------------------------------------
# 使用者的個人偏好檔，凌駕一切（含 OpenCC）。預設讀 skill 根目錄的
# user-dictionary.json，可用 --dict 指定。結構：
#   {
#     "replacements": {"原文": "目標"},   # 最後一步逐字替換，最高優先
#     "casing":       {"myapp": "MyApp"}, # 併入大小寫表，使用者覆寫內建
#     "protect":      ["別動我"],          # 全程不被任何規則更動
#     "formal_tai":   false                # 覆寫 台/臺 預設
#   }
import json
import os

_DICT_NAME = 'user-dictionary.json'


def _find_default_dict():
    # 個人字典放在「專案根目錄」(使用者的 skills 倉庫根)，不綁這個 skill。
    # 從腳本所在位置往上層逐級找 user-dictionary.json，找到最近的一份就用。
    # 這樣字典是整個倉庫共用、也不只給 Claude 用；缺檔則無妨（回傳空）。
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        cand = os.path.join(d, _DICT_NAME)
        if os.path.exists(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:            # 到檔案系統根了，沒找到
            return None
        d = parent


def _load_user_dict(path=None):
    p = path or _find_default_dict()
    if not p or not os.path.exists(p):
        return {}
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"WARNING: user dictionary at {p} unreadable ({e}); ignored.",
              file=sys.stderr)
        return {}


# ---------------------------------------------------------------------------
# 主調度器 (orchestrator)
# ---------------------------------------------------------------------------
def normalize(text, *, convert=True, fixes=True, quotes=True, punct=True,
              spacing=True, width=True, casing=True, formal_tai=False,
              user_dict=None):
    user_dict = user_dict or {}
    if 'formal_tai' in user_dict:           # 個人字典可覆寫 台/臺 預設
        formal_tai = user_dict['formal_tai']
    # 個人字典的 protect 詞與內建保護片段一起抽出，全程不被更動。
    text, store = _protect(text, extra_protect=user_dict.get('protect'))
    opencc_ok = None
    if convert:
        text, opencc_ok = _opencc_convert(text)
    if width:
        text = _to_halfwidth(text)
    if fixes:
        text = _fix_variants(text, formal_tai=formal_tai)
    if quotes:
        text = _fix_quotes(text)
    if punct:
        text = _fix_punct(text)
    # 在「盤古之白」之前先還原：保護的目的是擋住標點與引號改寫，
    # 不是擋住空格。對還原後的文字補空格，才能讓 "版本3.14" → "版本 3.14"、
    # "在src/x.py" → "在 src/x.py"。
    text = _restore(text, store)
    if spacing:
        text = _pangu(text)
    if casing:
        text = _fix_casing(text, extra=user_dict.get('casing'))
    text = _cleanup(text)
    # 個人字典的逐字替換放最後 ── 權限最高，凌駕所有規則與 OpenCC。
    for src_term, dst_term in (user_dict.get('replacements') or {}).items():
        text = text.replace(src_term, dst_term)
    return text, opencc_ok


def _unified_diff(old, new, name):
    import difflib
    return ''.join(difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile=f'{name} (original)', tofile=f'{name} (normalized)'))


def main():
    ap = argparse.ArgumentParser(description='Taiwan Traditional Chinese typography normalizer')
    ap.add_argument('file', nargs='?', help='input file; omit to read stdin')
    ap.add_argument('--text', help='normalize this string directly')
    ap.add_argument('--in-place', action='store_true', help='rewrite the file')
    ap.add_argument('--diff', action='store_true', help='print unified diff only')
    ap.add_argument('--formal-tai', action='store_true', help='convert 台→臺 in place names')
    ap.add_argument('--no-convert', action='store_true', help='skip OpenCC simp→trad')
    ap.add_argument('--no-fixes', action='store_true', help='skip 異體字 fixes')
    ap.add_argument('--no-quotes', action='store_true', help='skip quote normalization')
    ap.add_argument('--no-punct', action='store_true', help='skip punctuation full-width')
    ap.add_argument('--no-spacing', action='store_true', help='skip 盤古之白 spacing')
    ap.add_argument('--no-width', action='store_true', help='skip full-width→half-width letters/digits')
    ap.add_argument('--no-casing', action='store_true', help='skip proper-noun casing (github→GitHub)')
    ap.add_argument('--dict', dest='dict_path', help='path to personal user-dictionary.json (highest priority)')
    args = ap.parse_args()

    user_dict = _load_user_dict(args.dict_path)

    if args.text is not None:
        src = args.text
        name = '<text>'
    elif args.file:
        with open(args.file, encoding='utf-8') as f:
            src = f.read()
        name = args.file
    else:
        src = sys.stdin.read()
        name = '<stdin>'

    out, opencc_ok = normalize(
        src,
        convert=not args.no_convert,
        fixes=not args.no_fixes,
        quotes=not args.no_quotes,
        punct=not args.no_punct,
        spacing=not args.no_spacing,
        width=not args.no_width,
        casing=not args.no_casing,
        formal_tai=args.formal_tai,
        user_dict=user_dict,
    )

    if args.diff:
        sys.stdout.write(_unified_diff(src, out, name) or '(no changes)\n')
    elif args.in_place and args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(out)
        changed = src != out
        print(f"{'updated' if changed else 'no change'}: {args.file}", file=sys.stderr)
    else:
        sys.stdout.write(out)

    if not args.no_convert and opencc_ok is False:
        sys.exit(2)   # 訊號：簡轉繁那一步被跳過了


if __name__ == '__main__':
    main()

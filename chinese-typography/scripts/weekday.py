#!/usr/bin/env python3
"""
日期補星期幾 (annotate weekday) — normalize.py 的「前處理」工具。

把 `06/25`、`2026/06/25` 這種日期後面補上台灣慣用的全形星期括號：
  06/25  →  06/25（四）

刻意「不」併進 normalize.py：normalize 是確定性、冪等的「排版轉換」，
而算星期幾是「日曆運算」（需要年份、要算對、不是純字串替換）。兩者關注點
不同，混在一起會破壞 normalize 的冪等性。用法是先跑這支把文字定稿，再交給
normalize 做排版。

設計重點（每條都有對應的失敗模式）：
  - 年份預設今年，但會「大聲」回報假設了哪一年（fail-loud-lite）。
    文件 12 月寫、日期填 01/05 時，預設今年可能就錯——把假設攤出來讓人掃一眼。
  - bare 形 `MM/DD` 只收「雙位數」(zero-pad)，躲開分數/比例 1/2、3/4、24/7。
    `YYYY/MM/DD` 因為年份已消歧，月日放寬成 1–2 位。
  - 左右用 lookaround 擋住數字/斜線/點，躲開版本號、路徑、民國年 115/06/25。
  - 非法日期 (02/30、13/01) → 原地不動 ＋ 記 warning，不靜默吞。
  - 已經有括號 (06/11（下週四）) 預設保留（那是人工語意）；--overwrite 才覆寫。

用法：
  echo "06/25 開會" | python3 weekday.py                # → 06/25（四），假設今年
  python3 weekday.py FILE.md --year 2026                # 指定年份
  python3 weekday.py FILE.md --diff
  python3 weekday.py FILE.md --in-place --year 2026
  python3 weekday.py --text "預計於 06/25 舉行" --year 2026
"""
import argparse
import datetime
import re
import sys

# Python date.weekday(): 週一=0 … 週日=6，正好對到台灣的 一二三四五六日。
_WD = "一二三四五六日"

# 日期樣式。三種分支：
#   YYYY/MM/DD     — 4 位年 + 1~2 位月 + 1~2 位日
#   MM/DD          — 只收雙位數，否則 1/2、3/4 這種分數會被誤判成日期
#   [YYYY年]M月D日 — 中文「月日」式，有 月/日 標記消歧，月日放寬成 1~2 位；
#                    年份選用，自帶就用它。國字版（六月二十五日）刻意不收——
#                    \d 不吃中文數字，天生排除，成本高、罕見、ROI 低。
# 左 (?<![\d/.]) 擋住前面是數字/斜線/點（版本號、路徑、a/b/c、民國年 115/06/25
# 的 /06）。右 (?![\d/]) 擋住後面還接數字/斜線（避免吃半截 YYYY/MM/DD）。
# 既有的星期括號（全形或半形皆認）一起抓進來，用來判斷「已經標過」。
_DATE_RE = re.compile(
    r'(?<![\d/.])'
    r'(?P<date>'
    r'(?:(?P<y>\d{4})/(?P<mo1>\d{1,2})/(?P<d1>\d{1,2}))'
    r'|'
    r'(?:(?P<mo2>\d{2})/(?P<d2>\d{2}))'
    r'|'
    r'(?:(?:(?P<y2>\d{4})年)?(?P<mo3>\d{1,2})月(?P<d3>\d{1,2})日)'
    r')'
    r'(?![\d/])'
    r'(?P<paren>[（(][^）)]*[）)])?'
)


def add_weekday(text, year=None, *, overwrite=False):
    """在日期後補（星期）。回傳 (新文字, warnings)。

    year=None 時用今年，並對每個無年份的日期記一條「假設年份」warning。
    overwrite=False 時，已有括號的日期原樣保留。
    """
    warns = []
    assumed = year is None
    if assumed:
        year = datetime.date.today().year

    def repl(m):
        yg = m.group('y') or m.group('y2')   # 斜線式或中文式自帶的年份
        y = int(yg) if yg else year
        mo = int(m.group('mo1') or m.group('mo2') or m.group('mo3'))
        d = int(m.group('d1') or m.group('d2') or m.group('d3'))
        try:
            wd = _WD[datetime.date(y, mo, d).weekday()]
        except ValueError:
            warns.append(f"略過非法日期：{m.group('date')}")
            return m.group(0)
        if m.group('paren') and not overwrite:
            return m.group(0)            # 已標過，保留人工語意（如「下週四」）
        if assumed and not yg:
            warns.append(f"{m.group('date')} 無年份 → 假設 {year} 年 → （{wd}）")
        return f"{m.group('date')}（{wd}）"

    return _DATE_RE.sub(repl, text), warns


def _unified_diff(old, new, name):
    import difflib
    return ''.join(difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile=f'{name} (original)', tofile=f'{name} (+weekday)'))


def main():
    ap = argparse.ArgumentParser(description='Annotate dates with Taiwan weekday 一二三四五六日')
    ap.add_argument('file', nargs='?', help='input file; omit to read stdin')
    ap.add_argument('--text', help='process this string directly')
    ap.add_argument('--year', type=int, help='year for bare MM/DD dates (default: this year)')
    ap.add_argument('--overwrite', action='store_true', help='replace existing （…） annotations')
    ap.add_argument('--in-place', action='store_true', help='rewrite the file')
    ap.add_argument('--diff', action='store_true', help='print unified diff only')
    args = ap.parse_args()

    if args.text is not None:
        src, name = args.text, '<text>'
    elif args.file:
        with open(args.file, encoding='utf-8') as f:
            src = f.read()
        name = args.file
    else:
        src, name = sys.stdin.read(), '<stdin>'

    out, warns = add_weekday(src, year=args.year, overwrite=args.overwrite)

    if args.diff:
        sys.stdout.write(_unified_diff(src, out, name) or '(no changes)\n')
    elif args.in_place and args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(out)
        print(f"{'updated' if src != out else 'no change'}: {args.file}", file=sys.stderr)
    else:
        sys.stdout.write(out)

    # fail-loud：假設年份／非法日期都印到 stderr，別讓使用者沒看到。
    for w in warns:
        print(f"NOTE: {w}", file=sys.stderr)


if __name__ == '__main__':
    main()

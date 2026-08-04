#!/usr/bin/env python3
"""
normalize.py 的回歸測試 (regression tests).

執行：python3 test_normalize.py
每一條都鎖住一個曾經出錯、或容易再出錯的行為。
"""
from normalize import normalize


def n(s, **kw):
    kw.setdefault('convert', False)  # 預設關閉 OpenCC，讓測試不依賴外部套件
    out, _ = normalize(s, **kw)
    return out


CASES = [
    # (說明, 輸入, 期望輸出, kwargs)
    ("盤古之白：中英之間補空格", "使用Python3寫程式", "使用 Python3 寫程式", {}),
    ("標點全形化", "他說,對吧?", "他說，對吧？", {}),
    ("引號轉直角", '他說"你好"', "他說「你好」", {}),
    # 這是最重要的回歸：佔位符曾用裸數字，還原時會把內文的數字毀掉。
    ("數字不被佔位符汙染（曾經的嚴重 bug）",
     "我有100台手機跟3.14版,共1000元", "我有 100 台手機跟 3.14 版，共 1000 元", {}),
    ("版本號被保護、後面句點轉全形",
     "版本是2.31.0.然後呢", "版本是 2.31.0。然後呢", {}),
    ("Markdown 有序清單標記不被破壞", "1. 記得設定", "1. 記得設定", {}),
    ("純英文句子不被動到", "This is fine, really.", "This is fine, really.", {}),
    ("--no-punct：半形逗號原地不動、不長出空格",
     "好用多了,推薦", "好用多了,推薦", dict(punct=False, quotes=False, fixes=False)),
    ("冪等：已正規化的文字再跑一次不變",
     "使用 Python 寫程式，很開心。", "使用 Python 寫程式，很開心。", {}),
    ("code span 內的引號不轉", "執行`git -m \"x\"`完成", "執行 `git -m \"x\"` 完成", {}),
    # 雙階段還原：行內 code 含中文時，內部逐字不被 pangu 拆，只有外緣加空格
    ("行內 code 含中文：內部逐字、外緣加空格",
     "執行`會議6月25日`完成", "執行 `會議6月25日` 完成", {}),
    # code 在所有規則跑完後才還原 → casing 碰不到，`github` 不變 GitHub
    ("行內 code 不被 casing 改寫", "看`github`設定", "看 `github` 設定", {}),
    # 對照組：同樣的 github 在 code 外仍會被 casing 正規化
    ("code 外的 github 仍正規化（對照）", "用github跑", "用 GitHub 跑", {}),
    # 省略號曾被句點規則咬成 "。.。"，這是嚴重 bug 的回歸鎖
    ("省略號 ... → ……（台灣六點），不可變 。.。",
     "然後...就這樣", "然後……就這樣", {}),
    ("破折號 -- → ——（中文間）", "就這樣--結束", "就這樣——結束", {}),
    ("純英文省略號不動", "wait... what", "wait... what", {}),
    # 數字+中文日期/時間單位：使用者偏好「加空格」(與 zhlint skipZhUnits 慣例相反)
    ("數字+中文單位仍加盤古之白（使用者偏好）",
     "我5月要去,共12時30分", "我 5 月要去，共 12 時 30 分", {}),
    ("專有名詞大小寫 github→GitHub、ios→iOS",
     "用github跑在ios上", "用 GitHub 跑在 iOS 上", {}),
    ("全形英數 → 半形", "全形ＡＢＣ１２３", "全形 ABC123", {}),
    ("--no-casing 關閉大小寫", "用github", "用 github", dict(casing=False)),
    ("西文縮寫句點不轉 。（Fig./e.g.）",
     "見Fig.3跟e.g.這個", "見 Fig.3 跟 e.g.這個", {}),
    # 個人字典：權限最高，逐字替換凌駕一切
    ("個人字典 replacements 蓋過規則",
     "敝公司很棒", "本團隊很棒", dict(user_dict={"replacements": {"敝公司": "本團隊"}})),
    ("逐字替換長鍵先套：短鍵寫在前面也不會把長鍵咬掉半截",
     "快快閃記憶體儲器", "快閃記憶體",
     dict(user_dict={"replacements": {"快快閃記憶體儲": "快閃記憶體",
                                      "快快閃記憶體儲器": "快閃記憶體"}})),
    ("個人字典 formal_tai 覆寫預設→臺",
     "在台北", "在臺北", dict(user_dict={"formal_tai": True})),
    # s2twp 漏掉的台灣在地用詞修正（defaults.json，OpenCC 之後套用；輸入用已轉繁形）
    ("賬→帳（撞 Beancount 記帳）", "記賬", "記帳", {}),
    ("vocab_fixes 攝像頭→攝影機", "攝像頭", "攝影機", {}),
    ("vocab_fixes 不誤傷 識別證（只收人臉識別）", "員工識別證", "員工識別證", {}),
    # markdown 強調符號：空格補在標記外側，絕不插進標記與內容之間
    ("Markdown 粗體不被撐破（曾經的 bug：**來源** → ** 來源 **）",
     "**來源**：後面的內容", "**來源**：後面的內容", {}),
    ("粗體外側補空格、內側不插：中文**bold**中文",
     "中文**bold**中文", "中文 **bold** 中文", {}),
    ("底線強調同理：中文__bold__中文",
     "中文__bold__中文", "中文 __bold__ 中文", {}),
    ("星號數學式仍有 CJK 邊界空格", "答案是3*4啦", "答案是 3*4 啦", {}),
    # pangu.js v8.0.0 SOLITARY_NBSP：孤立 NBSP 轉一般空格、連續 NBSP 保留
    ("孤立 NBSP → 一般空格", "中文\u00a0abc", "中文 abc", {}),
    ("連續 NBSP 是刻意版面，保留", "縮排\u00a0\u00a0\u00a0內容", "縮排\u00a0\u00a0\u00a0內容", {}),
    # pangu.js v8.0.0 斜線啟發式：2+ 斜線的行視為路徑／並列分隔符，不加空格
    ("多斜線行：含中文的路徑不被拆", "/home/用戶/文件", "/home/用戶/文件", {}),
    ("多斜線行：並列分隔符不加空格", "選甲/乙/丙其一", "選甲/乙/丙其一", {}),
    ("單斜線維持原行為（斜線兩側加空格）", "中文/英文", "中文 / 英文", {}),
]

# 需要 OpenCC 才能跑的案例（s2twp 逐行偵測）。缺套件時整段跳過並大聲說，
# 不假裝通過 —— 與 normalize.py 對 OpenCC 缺席的 fail-loud 立場一致。
OPENCC_CASES = [
    # (說明, 輸入, 期望輸出, kwargs)  —— 這裡 convert 預設「開」
    ("簡體輸入照轉（软件→軟體）", "这个软件很好用", "這個軟體很好用", {}),
    ("已是繁體：文件 不被二次轉成 檔案", "請看這份文件", "請看這份文件", {}),
    ("已是繁體：登錄／聲明 不被改成 登入／宣告",
     "登錄資訊與授權聲明", "登錄資訊與授權聲明", {}),
    ("已是繁體：英文本體 不被切成 英文字體（曾經的切詞災難）",
     "英文本體很重要", "英文本體很重要", {}),
    ("混排：簡體行照轉、繁體行不動",
     "繁體的文件\n简体的软件", "繁體的文件\n簡體的軟體", {}),
    ("--force-convert 回到整篇轉換（文件→檔案）",
     "請看這份文件", "請看這份檔案", dict(force_convert=True)),
    # opencc-python-reimplemented 0.1.7 的 s2twp 有貪婪比對錯字（BYVoid/OpenCC 1.4.1
    # 已修，但那份修正流不進這個被釘住的套件），補在 data/defaults.json 的 vocab_fixes。
    # 這幾條鎖的是「出貨的預設表真的補上了」，不是「替換機制會動」。
    ("s2twp 貪婪錯字：互联网络 不吐出 網際網路絡", "互联网络技术", "網際網路技術", {}),
    ("s2twp 貪婪錯字：快闪存储器 不吐出 快快閃記憶體儲器（短鍵是長鍵前綴，順序會咬人）",
     "快闪存储器很小", "快閃記憶體很小", {}),
    ("s2twp 貪婪錯字：快闪存储 單獨出現也要對", "快闪存储技术", "快閃記憶體技術", {}),
    ("老挝 官方國名（跟進 OpenCC 1.4.1）",
     "老挝人民民主共和国", "寮人民民主共和國", {}),
    # 刻意不收 数字人文→數位人文：這一層沒有詞界線，「數字」＋「人文…」跨小句會被咬。
    # 這條鎖的是「別再把它加回出貨的 defaults.json」（使用者自己的 user-dictionary.json
    # 不在測試載入範圍，那是他的檔案）。理由見 references/glossary.md。
    ("數字人文 不進 defaults.json（跨小句會誤傷）",
     "報表上的數字人文科系的學生未必看得懂", "報表上的數字人文科系的學生未必看得懂", {}),
]


def main():
    fails = total = 0

    def run(desc, src, want, kw):
        nonlocal fails, total
        total += 1
        got = n(src, **kw)
        ok = got == want
        if not ok:
            fails += 1
        print(f"{'PASS' if ok else 'FAIL'}  {desc}")
        if not ok:
            print(f"      input:  {src!r}")
            print(f"      want:   {want!r}")
            print(f"      got:    {got!r}")

    for desc, src, want, kw in CASES:
        run(desc, src, want, kw)

    try:
        import opencc  # noqa: F401
        for desc, src, want, kw in OPENCC_CASES:
            run(desc, src, want, {**kw, 'convert': True})
    except ImportError:
        print(f"SKIP  OpenCC not installed — {len(OPENCC_CASES)} 條 s2twp 逐行偵測案例未跑")

    print(f"\n{total-fails}/{total} passed")
    raise SystemExit(1 if fails else 0)


if __name__ == '__main__':
    main()

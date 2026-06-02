#!/usr/bin/env python3
"""
weekday.py 的回歸測試。執行：python3 test_weekday.py

全部用「明確年份」鎖死，測試不可依賴今天是哪天。
2026 已驗：06/25=四、06/11=四（與真實行事曆一致）。
"""
from weekday import add_weekday


def w(s, **kw):
    out, _ = add_weekday(s, **kw)
    return out


def warns(s, **kw):
    _, ws = add_weekday(s, **kw)
    return ws


CASES = [
    # (說明, 輸入, 期望輸出, kwargs)
    ("bare MM/DD 補星期", "預計於 06/25 舉行", "預計於 06/25（四） 舉行", dict(year=2026)),
    ("YYYY/MM/DD 補星期", "2026/06/25 開會", "2026/06/25（四） 開會", dict(year=2026)),
    ("YYYY 內含年，忽略 --year", "2026/06/25", "2026/06/25（四）", dict(year=1999)),
    # 已有括號是人工語意（下週四），預設保留、不蓋掉
    ("已有括號預設保留", "06/11（下週四）前回覆", "06/11（下週四）前回覆", dict(year=2026)),
    ("--overwrite 才覆寫括號", "06/11（下週四）", "06/11（四）", dict(year=2026, overwrite=True)),
    # 分數/比例不是日期：單位數或非雙位數一律不碰
    ("分數 3/4 不碰（單位數）", "比例 3/4 與 1/2", "比例 3/4 與 1/2", dict(year=2026)),
    ("24/7 不碰（日為單位數）", "全年 24/7 運作", "全年 24/7 運作", dict(year=2026)),
    ("雙位月+單位日不碰", "活動 12/5 截止", "活動 12/5 截止", dict(year=2026)),
    # 民國年：115/06/25 的 /06/25 左邊接 /，不可被當成 06/25
    ("民國年不誤判", "民國 115/06/25", "民國 115/06/25", dict(year=2026)),
    # 非法日期：原地不動
    ("非法日期 13/01 不動", "錯的 13/01 日期", "錯的 13/01 日期", dict(year=2026)),
    ("非法日期 02/30 不動", "02/30 不存在", "02/30 不存在", dict(year=2026)),
    # 一行多個日期
    ("一行多個日期", "06/25 與 06/11 兩天", "06/25（四） 與 06/11（四） 兩天", dict(year=2026)),
    # 冪等：補完再跑一次不變
    ("冪等：再跑一次不變", "06/25（四） 舉行", "06/25（四） 舉行", dict(year=2026)),
    # 版本號不誤判
    ("版本號 1.2/3.4 不碰", "ver 1.2/3.4 build", "ver 1.2/3.4 build", dict(year=2026)),
    # 中文「月日」式（阿拉伯數字）：有 月/日 標記消歧，單位數日也安全
    ("中文 6月25日 補星期", "會議 6月25日 舉行", "會議 6月25日（四） 舉行", dict(year=2026)),
    ("中文 12月5日 單位數日也收", "12月5日 截止", "12月5日（六） 截止", dict(year=2026)),
    ("YYYY年M月D日 自帶年份、忽略 --year", "2026年6月25日", "2026年6月25日（四）", dict(year=1999)),
    ("中文日期已有括號保留", "6月25日（四）", "6月25日（四）", dict(year=2026)),
    # ── 負向鎖：以下是「故意不做」的功能，鎖住現況；有人日後加支援會被這些測項提醒 ──
    ("國字版 六月二十五日 不收（刻意，ROI 低）", "六月二十五日 舉行", "六月二十五日 舉行", dict(year=2026)),
    ("過去年份照算、不做過期檢查", "06/25", "06/25（四）", dict(year=2020)),
]

WARN_CASES = [
    # (說明, 輸入, 期望 warning 數, predicate, kwargs)
    ("無年份→記假設年份 warning", "06/25 開會", 1, lambda ws: any('假設' in x for x in ws), dict(year=None)),
    ("非法日期→記 warning", "13/01", 1, lambda ws: any('非法' in x for x in ws), dict(year=2026)),
    ("有年份 YYYY 不記假設", "2026/06/25", 0, lambda ws: ws == [], dict(year=None)),
    # 負向鎖：單位數日被當「非日期」靜默跳過，刻意不警告（否則每個分數都會吵）
    ("單位數日靜默跳過、不警告", "活動 6/5 截止", 0, lambda ws: ws == [], dict(year=2026)),
    # 負向鎖：過去年份照算，不做「日期太舊→年份可能填錯」的猜測式警告
    ("過去年份不額外警告", "06/25", 0, lambda ws: ws == [], dict(year=2020)),
]


def main():
    fails = 0
    for desc, src, want, kw in CASES:
        got = w(src, **kw)
        ok = got == want
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {desc}")
        if not ok:
            print(f"      input:  {src!r}")
            print(f"      want:   {want!r}")
            print(f"      got:    {got!r}")

    for desc, src, n, pred, kw in WARN_CASES:
        ws = warns(src, **kw)
        ok = len(ws) == n and pred(ws)
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {desc}")
        if not ok:
            print(f"      warns:  {ws!r}")

    total = len(CASES) + len(WARN_CASES)
    print(f"\n{total-fails}/{total} passed")
    raise SystemExit(1 if fails else 0)


if __name__ == '__main__':
    main()

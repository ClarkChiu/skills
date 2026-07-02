# ui-design-advisor 品牌資產協議實作計畫

> 依 `docs/specs/2026-07-02-uda-brand-assets-design.md`。批次指令下的自主執行（假設已標明於設計 §4）。

1. **`references/brand-assets.md`**（新）：協議本體——never-guess 硬規則＋為什麼（記憶色是平均且過期）、三層取得優先序、brand-spec 格式模板、覆寫規則。驗收：`grep -c "MUST NOT"` ≥1、三層各有標號段落。
2. **`SKILL.md`**：`allowed-tools` 加 `WebFetch`；步驟 1 加品牌偵測掛鉤（指向 brand-assets.md）；步驟 3 加「brand-spec 色值凌駕色盤列」；brief 結構 Palette 項註明品牌場合引 brand-spec。驗收：`grep -c "brand-assets\|WebFetch"` ≥3。
3. **attribution.md＋sources.lock**：補第 6 源 `alchaincyf/huashu-design`（MIT、principles only、commit `0e7ec8aca005`、date 2026-07-02、比對重點：上游品牌協議與反 slop 清單的演進）。驗收：JSON 合法、6 源。
4. **`evals/evals.json`** 補一案 `brand-never-guess`：品牌請求＋無 brand-spec → 不憑記憶給 hex（問或抓＋附來源）。驗收：案數 +1、JSON 合法。
5. 驗證全部→提交：`✨ feat(ui-design-advisor): 品牌資產協議——絕不憑記憶猜品牌色，分層取得＋brand-spec 固化`＋docs 提交。

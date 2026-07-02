# ui-design-advisor 品牌資產協議設計

> 2026-07-02。原則參考 `alchaincyf/huashu-design` 的品牌資產協議與反 slop 論證（MIT，方法非檔；評估見 `research/audits/2026-07-02-huashu-design.md`）。
> **流程備註**：使用者已下「三項依序做完」批次指令後離線；連網姿態一題未答，採建議選項「混合分層」為**標明的假設**；設計→計畫→執行連走、獨立提交可撤銷，回線後可整批複核或推翻。

## 1. 目標與範圍

**目標**：出現可辨識品牌（公司、產品、開源專案）時，ui-design-advisor MUST NOT 憑訓練記憶猜品牌色值／標誌用法——記憶裡的品牌色是各版本的平均、常過期，正是「AI 預設產出＝所有品牌的平均＝沒有品牌被認出來」問題的來源。改為分層取得、固化成 brand-spec、日後重用。

**範圍內**：新 reference `references/brand-assets.md`（協議本體）；SKILL.md 工作流掛鉤＋`allowed-tools` 加 `WebFetch`；attribution／sources.lock 補 huashu 上游；evals 補一案。

**非目標**：不做 huashu 的五步強制連網流程（WebSearch 搜官網那步不搬——本技能有離線路徑）；不抓標誌圖檔進儲存庫（brand-spec 記來源網址與色值，不存二進位）；不改 data/ 收錄資料。

## 2. 協議（brand-assets.md 的內容要點）

**觸發**：Design Read（步驟 1）發現請求涉及可辨識品牌時。

**取得優先序（混合分層）**：
1. 使用者提供的資產／既有 brand-spec（`docs/design/brand/<brand>-spec.md` 若存在）——最高。
2. 會話有 `WebFetch` 時：抓官方來源釘色值——品牌官網 CSS／設計指南頁、`svgl.app`／`simpleicons.org`（standing hex 資料庫）。記下來源網址與抓取日期。
3. 無網或抓不到：`AskUserQuestion` 要色值／檔案。**任何一層都不允許退回「憑印象寫 hex」**。

**固化**：取得後寫 `docs/design/brand/<brand>-spec.md`（品牌名、primary／secondary hex、深淺底用法但書、來源網址＋日期），下次同品牌直接重用（第 1 層命中）。

**覆寫規則**：brand-spec 的色值凌駕 `data/` 色盤列——收錄資料選「風格」，品牌資產定「顏色」。

## 3. 驗收（Given/When/Then）

1. Given 使用者要求「幫 TXOne 官網定設計方向」且無既有 brand-spec、會話無網，When 執行，Then 產出的 brief 不含憑記憶的品牌 hex，而是問使用者要色值。
2. Given 會話有 WebFetch，When 同上請求，Then 色值附來源網址＋日期，並寫出 brand-spec 檔。
3. Given `docs/design/brand/txone-spec.md` 已存在，When 再次執行同品牌請求，Then 直接重用、不重抓不重問。
4. Given 無品牌的一般請求（「做個 SaaS 儀表板」），When 執行，Then 協議不觸發、流程與現行完全相同。

## 4. 自我審查

- 假設標明：混合分層未經使用者確認（AFK），若要改「保持離線」只需從 SKILL.md 拿掉 WebFetch 並刪協議第 2 層——設計已隔離該層，改動成本一行。
- 與「Your preferences win」節相容：brand-spec 本質上就是該節說的「使用者檔案優先」，協議只是把取得過程紀律化。
- 無佔位符；範圍不跨技能。

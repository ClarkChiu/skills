# 外部 Skill 評估判準 (Skill Evaluation Criteria)

> `skill-curator` 的決策大腦。評估「該不該用、怎麼用」一個外部 skill。
> 由 2026-06-02 的 11-skill 評估流程萃取。安全裁決委由 `skill-auditor`；
> 發現委由 `skill-finder`；本檔管「**相關性 + 決策 + 記錄**」。

## 出發點：以使用者定位為錨

評估**不是**問「這 skill 好不好」，而是「**對這個人的工作/生活有沒有用**」。
讀 **repo 根 `CLAUDE.md` 的「使用者定位」段**（可攜真相來源；memory `user-profile` 僅本機快取）。摘要：網路/系統軟體工程師（10+ 年），骨幹是
**測試自動化架構 + DevOps/IaC（Terraform/CI-CD）+ 雲端（GCP）+ Python + 協定/標準研究
（專利・論文）**，5+ 年 PM/產品，寫**大量 EN + zh-TW 技術文件**。範圍是「技能 + LLM
幫工作與生活全面」，不只中文處理。
→ 測試自動化、DevOps/IaC、雲端、網路/協定、**技術寫作**、PM/spec、research、ML 都**高度
相關**，不是 niche。深度在網路/系統/基建/測試自動化，**別過度看重純前端 web 類**。

## 五步決策流程

```
[0] 相關性  → 對我的情境（dev/系統/PM/寫作/研究/生活）有用嗎？無 → 停。
[1] 重複性  → 重複內建或我現有的 skill 嗎？是 → 用既有的，或「擴充我的」而非裝它。
[2] 資安    → 交給 skill-auditor。裁決非 SAFE → 停（或只在沙箱）。
[3] 來源    → 作者可信？有維護？還是個人 2★/單一 fork/兩份不一致？
[4] 裝 or 自製 → 見下方判準表。
[5] 記錄    → 本機詳細（gitignored）：audits/ + 當日工作日誌；公開：research/skill-index.md 中性一列。
```

## 步驟 4 核心：直接裝 vs 參考自製 vs 跳過

判斷一個 skill 的**價值載體在哪裡**，決定怎麼用：

| 訊號 | 傾向 | 為什麼 |
|---|---|---|
| 夾**非平凡程式/策展資料**，來源**可信且有維護** | **直接裝** | 重造輪子不值；裝了還跟上游更新 |
| 純 **prose / persona**（價值是可編輯文字） | **參考自製** | 複製成本趨近零；自製可客製、不背依賴 |
| 來源**弱**（個人低星、無維護、repo 內兩份不一致、無 frontmatter） | **參考自製** | 不把生產流程綁在不穩的 repo |
| 你有**強烈客製需求**（zh-TW、你的技術棧、你的 PM 風格） | **參考自製** | 自製剛好給你要的那版 |
| 重複**內建/現有**能力 | **都不要** | 用既有的；頂多擴充自己的 |
| 介於之間（策展 prose，如譯好的規則集） | **收錄＋客製** | 從現成檔起步、複製進 repo、標 attribution、調口味 |
| **可信來源＋夾 code，但 code 是 opt-in 周邊、核心價值在 prose** | **偏參考自製** | 別被「有 code＋來源好」誤導成直接裝——先問「那段 code 對**這個使用者**是價值還是用不到的周邊？」周邊 → 自寫 prose；真要那段 code 才收錄 |

### Tie-breaker：當「直接裝」與「參考自製」同時成立

一個 skill 可能**同時**命中「夾 code＋來源可信」(→裝) 和「價值在 prose」(→自製)。
別平均、別看到 code 就喊裝。決勝問句：**「那段工程，對這個使用者是不可複製的價值，還是
他根本用不到的 opt-in 周邊？」**
- 是核心價值且難複製（如 ui-ux-pro-max 的 161 調色盤策展、deep-research 的 3200 行）→ **直接裝**。
- 是 opt-in 周邊、這個人多半不開（如 brainstorming 的 Visual Companion 本地 server，對終端為主的全端）→ **參考自製**：擷取 prose、接進自己 pipeline；真要那段周邊才降 **收錄**。
（實例：brainstorming 來源強、夾 node server，但核心價值是「設計先於寫碼」的 prose 閘門 → 參考自製，非直接裝。）

### 一句話心法
> **能下載的工程就裝，能寫的文字就自己寫成你要的樣子。**
> prose skill 價值是「文字本身」→ 自製 + 掛進自己 repo（受 skill-evolve 追上游）比 APM 依賴薄 fork 穩。
> code/data skill 價值是「難複製的工程或策展」→ 直接裝。

## 風險與安裝面（auditor 的補充重點）

資安「乾淨」不等於「零成本」。即使 SAFE，仍要看**安裝面**：

- **特權安裝**：`sudo`、遠端抓 install 腳本執行、改 `~/.bashrc` → 高警戒（例：minimax-docx setup.sh 裝 .NET）。
- **未釘版自動裝**：`pip install --break-system-packages`、`npm i -g`、`npx playwright install chromium`、import 時自動 bootstrap → 供應鏈面。
- **安裝器 ≠ 執行期**：腳本本身可能乾淨，地雷在它的 CLI 安裝器（例：ui-ux-pro-max 的 `extract.ts` shell 字串插值）→ **手動複製 skill 夾、避開 CLI**。
- **自動裝系統依賴**（叫 agent 自己 brew/apt 裝 Python）→ 自己先裝，別讓它自動跑。
- **純 prose、無 net/shell** = 最低風險級（例：humanizer、product-spec-builder）。

## 常見陷阱（實戰萃取）

- **一條列 ≠ 一個 skill**：`minimax-docx、pdf、xlsx` 一行其實 3 個。展開再算。
- **清單來源信任度低**：第三方中文推薦清單會把不同作者、不同品質的 skill 湊一起。
- **同名不同物**：`dev-builder` 撞名 `21st-dev-builder-v2`；`ppt-generator` 實為 `pptx-generator`。對 canonical repo，別信 listing。
- **星數存疑**：無 API auth 的渲染頁星數可能誤讀/灌水（superpowers「215k」極可能誤讀）→ 標未驗證，不當事實。
- **不同 skill 吃同一檔但格式未必相容**：product-spec-builder／dev-builder／ui-prompt-generator 都吃 `Product-Spec.md` 但不同作者 → 串接前確認欄位。
- **process.env 不一定是外洩**：`apiKey: process.env.X` 直接進 SDK constructor＝標準用法；要看 key 有沒有被串進 URL/log/第三方請求才算 exfil。
- **document 不外送 ≠ 安全無虞**：MiniMax 不傳文件內容，但安裝特權才是它的風險。

## 輸出：記錄格式

每次評估都留軌跡，分**本機**與**公開**兩層（`research/` 除 `skill-index.md` 外皆 gitignored）：

- **本機（不公開）**：
  - `audits/YYYY-MM-DD-<skill>.md`：完整 SKILL AUDIT REPORT（skill-auditor 格式）。
  - `<YYYY-MM-DD>-skill-research-log.md`（當日工作日誌）：日期｜名稱｜URL｜作者｜重複?｜
    **資安重點｜詳細理由**——第三方資安細節、漏洞、措辭都留這層。
- **公開**：`skill-index.md` 一列**中性**摘要：日期｜名稱｜URL｜作者｜重複內建?｜裁決。
  **不放**資安細節/漏洞揭露/對第三方評語；裁決定位為「對本專案的適配決定」，非品質評斷。
  理由：公開 repo 不該點名批評他人 skill，也不該未通知就揭露第三方漏洞。
- 研究 ≠ 安裝；裝前 v1.0 安全 ≠ 你抓的那版安全，裝後複審本機版本。

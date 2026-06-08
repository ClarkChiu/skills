# skills

> Clark Chiu 的 AI 代理技能集

以 APM（Agent Package Manager）管理的個人技能套件。內含可跨多種 AI 代理主機（Claude Code、OpenCode、Hermes Agent、Codex CLI、Cursor 等）使用的 `SKILL.md` 技能，集中維護於同一個專案，避免散落在各家命令列工具或第三方技能平台上。

## 目的

這個專案是我用 **技能（skills）＋ LLM 協助工作與生活** 的中樞——範圍涵蓋前後端與系統程式開發、產品管理（PRD／需求／優先級）、研究與寫作，**不只限於中文處理**。中文排版（`chinese-typography`）只是其中一個面向。評估與引入任何外部技能時，都以「能否實際幫到這些工作／生活情境」為出發點，並一律先過 `skill-auditor` 安全稽核、把研究與裁決記錄下來，再決定是否安裝。

## 自建技能（本專案維護）

| 技能 | 說明 |
| --- | --- |
| [`skill-auditor`](./skill-auditor/) | 安裝任何 AI 代理技能**之前**必跑的安全稽核協議。讀取目標 `SKILL.md` 與整個技能目錄，依六步驟協議檢查惡意指令、權限濫用、提示注入、混淆與外洩行為，最後輸出含裁決（✅ SAFE／⚠️／❌）與安全執行計畫的 **SKILL AUDIT REPORT**。本身不執行任何程式碼，為純 Markdown。 |
| [`skill-finder`](./skill-finder/) | 唯讀搜尋開放技能生態（`skills.sh`），抓取候選 `SKILL.md` 供檢視，並在任何安裝決定前轉交 `skill-auditor`。只發唯讀 HTTPS GET 請求，不執行 `npx skills`、不執行第三方程式碼、不傳送遙測。負責「發現與評估」，安裝由使用者自行決定。 |
| [`p2pscout`](./p2pscout/) | 工具型技能（以 Go 撰寫，非純 Markdown）。跨多個索引來源搜尋 BitTorrent 資源，依實測的節點群健康度（分散式雜湊表加追蹤伺服器，可選握手驗證）排序，挑出現在真的抓得到的那一筆；下載委派 aria2。代理以 `go run ./cmd/p2pscout` 直接呼叫（首次編譯後進快取），無需手動建置。需本機安裝 Go 1.25 以上。 |
| [`chinese-typography`](./chinese-typography/) | 臺灣繁體中文排版與正規化。自動補盤古之白（中英文間空格）、半形標點轉全形、引號改直角引號「」『』、簡轉繁並在地化臺灣用語（OpenCC `s2twp`）、修正異體字。核心是**確定性 Python 腳本**（非靠模型逐字猜）＋最高權限的個人字典 `user-dictionary.json`；通用表放 `data/defaults.json`，不動程式碼即可編輯。需本機 OpenCC 才做簡轉繁，缺套件會大聲警告而非默默略過。 |
| [`slide-deck`](./slide-deck/) | 準則導向的投影片設計引擎（非套模板）。將內容生成**單一自包含 HTML 檔**：固定 1920×1080 畫布、**跨裝置自動重算大小縮放填滿任何螢幕**（ResizeObserver 監看，手機第一次載入即滿版、不用重新整理）、可列印成 PDF、手機可滑動／點擊分區導覽。內建原創風格預設與版式準則（一頁一想法、型階、垂直預算、配色／動效紀律、繁中換行），附確定性檢查器 `check_deck.py` 出貨前把關。儲存庫不放任何第三方模板資產；需可編輯 `.pptx` 時改用 ppt-master（見 `references/output-formats.md`）。 |
| [`skill-evolve`](./skill-evolve/) | 隨叫隨跑的**自我維護偵察**。掃自寫 skill 的 `references/attribution.md` 找出上游參考來源，用 GitHub API 比對各 skill 的 `sources.lock` 基線看有無更新，並擴展搜尋新出現的相關專案，最後**出報告與你討論**——只偵察與建議，**從不自動改 skill**。**僅適用於本專案自寫的 skill**；外部（經 APM 引入）的技能用 `apm install` 隨上游更新即可，不歸它管。採納任何新來源前先過 `skill-auditor`。需本機 Python；建議設 `GITHUB_TOKEN`（公開讀取權限即可）以免 API 限流。 |
| [`skill-curator`](./skill-curator/) | **研究 Skill 大師**——評估外部 skill「該不該用、怎麼用」的**編排 + 決策 + 記錄**層。丟一個 skill（名稱／URL／一整份推薦清單）→ 跑五步流程（相關性→重複性→資安→來源→裁決）→ 給裁決（🟩 直接裝／🟦 參考自製／🟨 收錄＋客製／🟥 跳過）並寫進 `research/` 決策日誌。**呼叫**而非重做 `skill-finder`（發現）與 `skill-auditor`（資安裁決，不得蓋過）；判準大腦在 `references/criteria.md`。發現與決策，**不安裝**。 |
| [`humanizer`](./humanizer/) | 去除文字的 AI 生成痕跡，讓它讀起來像人寫的（中英雙語）。偵測並改寫內容灌水、宣傳腔、模糊歸因、三段式、AI 詞彙、填充語等模式；另處理臺灣繁體中文特有的痕跡：罐頭開場白（「值得一提的是」）、中國商業術語（賦能、抓手）、翻譯腔（「進行了優化」）、複數濫用「們」（「工具們」）。設計上**文風歸 humanizer、排版歸 `chinese-typography`**：標點／引號／盤古之白／簡轉繁／地區用詞都交給排版層，先 humanizer 後 normalize 兩段管線。英文規則原樣收錄自 `blader/humanizer`（由 `skill-evolve` 追上游），中文規則自寫（淺白臺灣用法）。純 prompt、不執行程式碼；只處理一般文字，不處理程式碼或 markdown 結構檔。 |
| [`design-gate`](./design-gate/) | 設計閘門：寫程式碼前，先把模糊想法逼成設計、再拆成可獨立執行的計畫。兩階段——先**設計**（逐題收斂、提 2–3 方案、寫成設計文件、自我複審），中間一道**硬閘門**（設計沒拍板前不寫程式碼、不建專案雛形、不叫實作），再**計畫**（拆成 2–5 分鐘一個的任務，每個標明確檔案路徑、完整可跑程式碼、驗證指令、提交）。只做前段；實際寫程式碼與測試的紀律交棒給 `CLAUDE.md` 的 Rule 0–12，不重複。規則改寫自 `obra/superpowers` 的 `brainstorming` 與 `writing-plans`（MIT），去品牌路徑、調成 pytest＋git 與這位使用者的本行；上游的多代理工程編排刻意未收錄（裁決見 `research/`）。純 prompt、不執行程式碼、不連網。 |
| [`verify-before-done`](./verify-before-done/) | 完成閘門：宣稱「測試過了／build 綠了／bug 修好了／搬遷完成」之前，先把該跑的驗證**重新跑一次、讀完整輸出和 exit code**，確認真的成立才能說。把 `CLAUDE.md` Rule 12（fail loud）落成五步閘門。刻意和內建 `verify`（跑 app 看行為）切開、不重複——這個是任何 test／lint／build／修復宣稱的輕量紀律閘門。改寫自 `obra/superpowers` 的 `verification-before-completion`（MIT）。含 Bash（要實際跑驗證指令）。 |
| [`systematic-debugging`](./systematic-debugging/) | 四階段根因除錯，擋掉「猜一個改一個」的瞎修：先把問題穩定重現、讀完錯誤訊息、查最近改動、回溯資料流找根因 → 比對能跑／壞掉的差異 → 單變數假設逐一測 → 先寫會失敗的重現測試再修。鐵律「沒找到根因不准修」；同一個 bug 修 ≥3 次還不好就停、質疑架構。交棒給 `verify-before-done` 做最終確認。改寫自 `obra/superpowers` 的 `systematic-debugging`（MIT）。含 Bash。 |
| [`ui-design-advisor`](./ui-design-advisor/) | UI **設計決策**層：動手寫前端前，先定「該長怎樣」。給產品／畫面／功能，挑出一致的視覺設計語言——風格、含 hex 的配色、字體配對、圖表型別、效果、無障礙要點，每項都對照收錄的策展資料（UI 風格、產業色盤、字體配對、圖表選型、UX 啟發式、WCAG/ARIA），產出一份 DESIGN BRIEF 再交棒內建 `frontend-design` 實作。資料**收錄**自四個來源：`nextlevelbuilder/ui-ux-pro-max-skill`、`mattdesl/dictionary-of-colour-combinations`、`plugin87/ux-ui-agent-skills`、`SteveBarnett/Checklists`（皆 MIT；只取資料、不取腳本；逐檔稽核見 `research/`）。LLM 直接讀檔（CSV/JSON/MD），靠 `data/INDEX.md` 路由只讀當次相關的表。 |
| [`solo-think`](./solo-think/) | 讓 Hermes Agent 在你離線、閒置時「自己想事情」：由 Hermes 的 heartbeat 週期喚醒，做夢式反思加上思考佇列，把想法寫進記憶檔。**只向內反思、絕不對外動作**——靠 heartbeat 的 `--toolsets file` 與技能 `allowed-tools` 兩層結構性鎖死，它手上根本沒有任何能對外的工具。只讀寫記憶與工作區設定檔；反思方向由 `focus` 錨定、時段由 `active_hours` 限制，觸發頻率交給 heartbeat 排程，不靠它自己估算用量。改寫自 `loryoncloud/Heartbeat-Like-A-Man`（MIT）：砍掉原作的自主對外探索與社群巡邏、從 OpenClaw 移植到 Hermes、改寫成臺灣繁體中文。 |
| [`tutor`](./tutor/) | 互動式家教協定（費曼＋蘇格拉底兩種模式），給「想真正搞懂」而非只要答案的時候用。承載價值是把硬規則釘死：一回合只講一個概念或只問一題、問完就停下來等、蘇格拉底模式絕不直接給答案（卡住只縮小提問範圍）、費曼模式答錯不前進改換類比、收尾一定由學習者把整個主題講回來再給「對／漏／錯」的誠實裁定——沒有這些規則，模型聊兩輪就會破功變成單向開講。零基礎自動走費曼、已有半懂或立場走蘇格拉底，明講模式優先。改寫自 @AnatoliKopadze 二十條提示詞中的 #18、#20（經動區譯文評估）；另三條成下一列的 roleplay-coach，餘十五條評估後跳過。 |
| [`roleplay-coach`](./roleplay-coach/) | 高風險對話的排練教練：薪資談判、模擬面試、困難對話三種情境。扮演**會真實抵抗的對手**——不輕易讓步、弱論點給具體反駁、強論點承認了照樣施壓；一回合一句、絕不自己演完兩邊；目標不切實際就在開演**之前**直說；結束必出戲做覆盤，重點是點名「你沒打出去的那張牌」——這是真實對手永遠不會告訴你的。困難對話採「先給劇本（開場白、對方三種可能反應的逐字應對、最容易踩的陷阱、收場方式），再陪你排練」。用真實對話會發生的語言排練。改寫自同一文章的 #9、#10、#12。 |
| [`social-card`](./social-card/) | 準則導向的 **IG／LinkedIn 社群卡片圖生成引擎**（非套模板）。把文章／筆記／截圖排成固定比例的卡片畫面，經 **agent-browser** 渲染成精確尺寸 PNG（IG 4:5／1:1／9:16、LinkedIn 1:1／1.91:1，FB 降級為單張）。兩套原創風格（Swiss 紀律／Editorial 雜誌）× 原創色盤 × 七個版式角色；承載鐵則**一卡一想法、先砍字不縮字**，附 `scripts/qa-rules.js` 經 `agent-browser eval` 檢查溢出／字級地板／標題上限／限動安全區。**只生成圖、不發文不管理**（發布屬另案 Meta API）。取 `op7418/guizang-social-card-skill` 的設計系統原則自製：未收任何上游檔（授權 AGPL/ISC 不一致）、平台改 IG/LinkedIn、render 由 playwright 換成 agent-browser。 |

## 外部技能（經 APM 引入第三方）

由 `apm.yml` 宣告、`apm.lock.yaml` 鎖定版本後安裝，部署到 `.claude/skills/`、`.agents/skills/`（這些目錄已列入 `.gitignore`，不進版控；靠鎖定檔記錄的版本（commit／hash）重現）。這些外部技能隨 `apm install` 跟上游更新即可；自寫技能的上游來源追蹤則交給 `skill-evolve`，兩者分工。

### [`vercel-labs/agent-browser`](https://github.com/vercel-labs/agent-browser)

| 技能 | 說明 |
| --- | --- |
| `agent-browser` | 給 AI 代理用的瀏覽器自動化命令列工具：導航、填表、點擊、截圖、抓取資料、測試網頁應用程式；也支援 Electron 桌面應用程式與雲端瀏覽器。 |

### [`anthropics/skills`](https://github.com/anthropics/skills)（17 個）

| 技能 | 說明 |
| --- | --- |
| `algorithmic-art` | 用 p5.js 做演算法／生成藝術。 |
| `brand-guidelines` | 套用 Anthropic 官方品牌色彩與字體。 |
| `canvas-design` | 以設計理念產生 `.png`／`.pdf` 視覺作品（海報、設計稿）。 |
| `claude-api` | 建置／除錯／優化 Claude API、Anthropic SDK 應用程式（含提示快取、模型遷移）。 |
| `doc-coauthoring` | 結構化協作撰寫文件、提案、技術規格。 |
| `docx` | 建立／讀取／編輯 Word `.docx`。 |
| `frontend-design` | 產生高設計品質的前端介面。 |
| `internal-comms` | 撰寫公司內部溝通（狀態報告、領導層更新、FAQ、事故報告等）。 |
| `mcp-builder` | 建置高品質 MCP 伺服器（Python FastMCP／Node TS SDK）。 |
| `pdf` | PDF 讀取、合併、拆分、旋轉、浮水印、填表、OCR 等。 |
| `pptx` | 建立／讀取／編輯 PowerPoint `.pptx` 簡報。 |
| `skill-creator` | 建立、改進、評測技能。 |
| `slack-gif-creator` | 製作 Slack 最佳化動態 GIF。 |
| `theme-factory` | 為產出物套用主題（10 種預設或即時生成）。 |
| `web-artifacts-builder` | 建置複雜多元件的 claude.ai HTML Artifacts（React／Tailwind／shadcn）。 |
| `webapp-testing` | 用 Playwright 測試本機網頁應用程式。 |
| `xlsx` | 試算表 `.xlsx`／`.csv` 讀寫、公式、圖表、資料清理。 |

## 安裝

### 透過 APM

```bash
apm install
```

會依 `apm.yml` 與 `apm.lock.yaml` 將技能部署到 `.claude/skills/` 與 `.agents/skills/`。

### 手動符號連結（不經 APM）

純 Markdown 技能載入只是讓指令對主機代理可用，不會執行程式碼，直接建立符號連結到對應目錄即可。部分技能附帶腳本，使用時需對應執行環境：`p2pscout` 需 Go 1.25 以上（`go run`）；`chinese-typography` 需 Python，簡轉繁另需 OpenCC；`slide-deck` 的檢查器 `check_deck.py` 需 Python；`skill-evolve` 需 Python，並建議設 `GITHUB_TOKEN`（公開讀取即可）以免查更新時被 GitHub API 限流。

把每個自建技能（見上方「自建技能」表）的目錄 symlink 進主機代理的 skills 目錄即可——Claude Code 是 `~/.claude/skills/`、OpenCode 是 `~/.config/opencode/skills/`。範本，每個技能各做一次（`<技能名>` 換成 `chinese-typography`、`design-gate`… 等）：

```bash
SKILL="<技能名>"
ln -snf "$(pwd)/$SKILL" ~/.claude/skills/"$SKILL"           # Claude Code
ln -snf "$(pwd)/$SKILL" ~/.config/opencode/skills/"$SKILL"  # OpenCode
```

> `skill-finder` 在評估階段會呼叫 `skill-auditor`，兩者請一起安裝。

其餘主機（Hermes、Codex、Cursor）與「以 `pre-tool hook` 強制執行稽核」的設定，詳見 [`skill-auditor/README.md`](./skill-auditor/README.md)。

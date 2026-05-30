# skills

> Clark Chiu 的 AI 代理技能集

以 APM（Agent Package Manager）管理的個人技能套件。內含可跨多種 AI 代理主機（Claude Code、OpenCode、Hermes Agent、Codex CLI、Cursor 等）使用的 `SKILL.md` 技能，集中維護於同一個專案，避免散落在各家命令列工具或第三方技能平台上。

## 自建技能（本專案維護）

| 技能 | 說明 |
| --- | --- |
| [`skill-auditor`](./skill-auditor/) | 安裝任何 AI 代理技能**之前**必跑的安全稽核協議。讀取目標 `SKILL.md` 與整個技能目錄，依六步驟協議檢查惡意指令、權限濫用、提示注入、混淆與外洩行為，最後輸出含裁決（✅ SAFE／⚠️／❌）與安全執行計畫的 **SKILL AUDIT REPORT**。本身不執行任何程式碼，為純 Markdown。 |
| [`skill-finder`](./skill-finder/) | 唯讀搜尋開放技能生態（`skills.sh`），抓取候選 `SKILL.md` 供檢視，並在任何安裝決定前轉交 `skill-auditor`。只發唯讀 HTTPS GET 請求，不執行 `npx skills`、不執行第三方程式碼、不傳送遙測。負責「發現與評估」，安裝由使用者自行決定。 |
| [`p2pscout`](./p2pscout/) | 工具型技能（以 Go 撰寫，非純 Markdown）。跨多個索引來源搜尋 BitTorrent 資源，依實測的節點群健康度（分散式雜湊表加追蹤伺服器，可選握手驗證）排序，挑出現在真的抓得到的那一筆；下載委派 aria2。代理以 `go run ./cmd/p2pscout` 直接呼叫（首次編譯後進快取），無需手動建置。需本機安裝 Go 1.25 以上。 |

## 外部技能（經 APM 引入第三方）

由 `apm.yml` 宣告、`apm.lock.yaml` 鎖定版本後安裝，部署到 `.claude/skills/`、`.agents/skills/`（這些目錄已列入 `.gitignore`，不進版控；靠鎖定檔記錄的版本（commit／hash）重現）。

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

純 Markdown 技能載入只是讓指令對主機代理可用，不會執行程式碼，直接建立符號連結到對應目錄即可。`p2pscout` 為工具型技能，符號連結後另需本機有 Go 才能 `go run`。

```bash
REPO="$(pwd)"  # 本專案根目錄

# Claude Code（全域）
mkdir -p ~/.claude/skills
ln -snf "$REPO/skill-auditor" ~/.claude/skills/skill-auditor
ln -snf "$REPO/skill-finder" ~/.claude/skills/skill-finder
ln -snf "$REPO/p2pscout" ~/.claude/skills/p2pscout

# OpenCode
mkdir -p ~/.config/opencode/skills
ln -snf "$REPO/skill-auditor" ~/.config/opencode/skills/skill-auditor
ln -snf "$REPO/skill-finder" ~/.config/opencode/skills/skill-finder
ln -snf "$REPO/p2pscout" ~/.config/opencode/skills/p2pscout
```

> `skill-finder` 在評估階段會呼叫 `skill-auditor`，兩者請一起安裝。

其餘主機（Hermes、Codex、Cursor）與「以 `pre-tool hook` 強制執行稽核」的設定，詳見 [`skill-auditor/README.md`](./skill-auditor/README.md)。

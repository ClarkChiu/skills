# skills

> Clark Chiu 的 AI Agent 技能集（Skills Collection）

以 APM（Agent Package Manager）管理的個人技能套件。內含可跨多種 AI agent 主機（Claude Code、OpenCode、Hermes Agent、Codex CLI、Cursor 等）使用的 `SKILL.md` 技能，集中維護於同一個專案，避免分散在各家 CLI 或第三方技能平台（registry）上。

## 自建技能（本專案維護）

| 技能 | 說明 |
| --- | --- |
| [`skill-auditor`](./skill-auditor/) | 安裝任何 AI agent 技能**之前**必跑的安全稽核協議。讀取目標 `SKILL.md` 與整個技能目錄，依 6 步驟協議檢查惡意指令、權限濫用、提示注入、混淆與外洩行為，最後輸出含裁決（✅ SAFE / ⚠️ / ❌）與安全執行計畫的 **SKILL AUDIT REPORT**。本身不執行任何程式碼，純 markdown。 |
| [`skill-finder`](./skill-finder/) | 唯讀搜尋開放技能生態（`skills.sh`），抓取候選 `SKILL.md` 供檢視，並在任何安裝決定前路由到 `skill-auditor`。只發唯讀 HTTPS GET，不跑 `npx skills`、不執行 vendor code、不送 telemetry。負責「發現與評估」，安裝由使用者自行決定。 |

## 外部技能（經 APM 引入第三方）

由 `apm.yml` 宣告、`apm.lock.yaml` 鎖定版本後安裝，部署到 `.claude/skills/`、`.agents/skills/`（這些目錄 gitignored，不進版控；靠 lockfile 的 commit/hash 重現）。

### [`vercel-labs/agent-browser`](https://github.com/vercel-labs/agent-browser)

| 技能 | 說明 |
| --- | --- |
| `agent-browser` | 給 AI agent 用的瀏覽器自動化 CLI：導航、填表、點擊、截圖、抓資料、測試 web app；也支援 Electron 桌面 app 與雲端 browser。 |

### [`anthropics/skills`](https://github.com/anthropics/skills)（17 個）

| 技能 | 說明 |
| --- | --- |
| `algorithmic-art` | 用 p5.js 做演算法／生成藝術。 |
| `brand-guidelines` | 套用 Anthropic 官方品牌色彩與字體。 |
| `canvas-design` | 以設計理念產生 `.png`／`.pdf` 視覺作品（海報、設計稿）。 |
| `claude-api` | 建置／除錯／優化 Claude API、Anthropic SDK app（含 prompt caching、模型遷移）。 |
| `doc-coauthoring` | 結構化協作撰寫文件、提案、技術規格。 |
| `docx` | 建立／讀取／編輯 Word `.docx`。 |
| `frontend-design` | 產生高設計品質的前端介面。 |
| `internal-comms` | 撰寫公司內部溝通（狀態報告、領導層更新、FAQ、事故報告等）。 |
| `mcp-builder` | 建置高品質 MCP server（Python FastMCP／Node TS SDK）。 |
| `pdf` | PDF 讀取、合併、拆分、旋轉、浮水印、填表、OCR 等。 |
| `pptx` | 建立／讀取／編輯 PowerPoint `.pptx` 簡報。 |
| `skill-creator` | 建立、改進、評測技能。 |
| `slack-gif-creator` | 製作 Slack 最佳化動態 GIF。 |
| `theme-factory` | 為產出物套用主題（10 種預設或即時生成）。 |
| `web-artifacts-builder` | 建置複雜多元件 claude.ai HTML artifacts（React／Tailwind／shadcn）。 |
| `webapp-testing` | 用 Playwright 測試本地 web app。 |
| `xlsx` | 試算表 `.xlsx`／`.csv` 讀寫、公式、圖表、資料清理。 |

## 安裝

### 透過 APM

```bash
apm install
```

會依 `apm.yml` 與 `apm.lock.yaml` 將技能部署到 `.claude/skills/` 與 `.agents/skills/`。

### 手動 symlink（不經 APM）

技能為純 markdown，載入只是讓指令對主機 agent 可用，不會執行程式碼。直接 symlink 到對應目錄即可：

```bash
REPO="$(pwd)"  # 本專案根目錄

# Claude Code（全域）
mkdir -p ~/.claude/skills
ln -snf "$REPO/skill-auditor" ~/.claude/skills/skill-auditor
ln -snf "$REPO/skill-finder" ~/.claude/skills/skill-finder

# OpenCode
mkdir -p ~/.config/opencode/skills
ln -snf "$REPO/skill-auditor" ~/.config/opencode/skills/skill-auditor
ln -snf "$REPO/skill-finder" ~/.config/opencode/skills/skill-finder
```

> `skill-finder` 在評估階段會呼叫 `skill-auditor`，兩者請一起安裝。

其餘主機（Hermes、Codex、Cursor）與「以 pre-tool hook 強制執行稽核」的設定，詳見 [`skill-auditor/README.md`](./skill-auditor/README.md)。

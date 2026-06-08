# 從 mattpocock/skills 挖掘的一批技能 — 設計文件

- 日期：2026-06-08
- 狀態：**已核准**（使用者拍板範圍與四項關鍵決策，2026-06-08）
- 參考來源：mattpocock/skills（MIT）的 tdd / git-guardrails-claude-code / caveman /
  to-issues、to-prd / grill-with-docs（取方法與構想，不收檔）。研究見
  `research/audits/2026-06-08-mattpocock-skills.md`。

## 範圍（本輪 4 新技能 + 1 增補）

| # | 產出 | 形式 | 來源 |
|---|---|---|---|
| 1 | `tdd` | 新技能 | Matt tdd |
| 2 | `git-guardrails` | 新薄技能（hook 載體） | Matt git-guardrails |
| 3 | `terse`（精簡模式，取代 caveman） | 新技能 | Matt caveman，修正中文 |
| 4 | `to-issues` | 新技能（design-gate 下游） | Matt to-issues |
| 5 | ADR + 統一語彙 | 增補進 `design-gate` | Matt grill-with-docs |

## 已核准的四項決策

1. **git-guardrails 範圍**：安裝步驟讓使用者選「專案層」或「全域」；都**合併**進對應的
   `settings.json`，**絕不覆蓋既有 RTK hook**。
2. **terse**：手動開關（說「精簡模式」/ `/terse` 進入，再說一聲退出），預設不動。
3. **tdd**：語言無關的 red-green-refactor 紀律核心 + pytest／網路協定整合測試範例。
4. **to-issues**：發布前一律先把 issue 清單給使用者確認，才用 `gh` 真的建立。

## 各項設計

### 1. `tdd`（新技能，英文）
- **定位**：寫碼**中**的建構迴圈，補 `design-gate`(前) → **tdd**(中) → `verify-before-done`(後) 的中段。
- SKILL.md：plan → tracer-bullet RED（寫一個只確認一件事的失敗測試、跑、確認紅）→ GREEN
  （最小實作、跑、確認綠）→ refactor（綠燈下才重構）。硬規則：紅燈不重構、一次一個測試、
  測試驗意圖不只驗行為（呼應 CLAUDE Rule 9）。
- references：`test-design.md`（測什麼/不測什麼、邊界）、`mocking.md`（何時 mock、協定測試
  用真 socket vs 假）、`refactoring.md`。範例用 pytest + 一個網路協定整合測試。
- 邊界：design-gate 的 writing-plans 已有「失敗測試先行/紅燈步驟」權威版，tdd 引用它、做深執行。
- attribution + sources.lock 釘 Matt tdd（方法非檔）。

### 2. `git-guardrails`（新薄技能，英文）
- **定位**：可攜的危險 git 攔截。APM 部署技能本體（含腳本）；安裝步驟把 hook **合併**進
  settings.json（使用者選專案/全域）。
- `scripts/block-dangerous-git.sh`：讀 PreToolUse 的 stdin JSON、取 `.tool_input.command`、
  比對危險樣式後 `exit 2` 擋下。**強化**（勝過 Matt 原版字串 grep）：
  - 樣式錨定（避免誤殺 commit message 含 "git push" 等）；
  - 涵蓋 `push --force`/`--force-with-lease`、`reset --hard`、`clean -fd`/`-f`、`branch -D`、
    `checkout .`/`restore .`、`push` 到受保護分支（main/master）。
- SKILL.md：安裝程序——偵測既有 settings.json、**合併**一條 PreToolUse/Bash hook（保留 RTK
  那條,在同 matcher 下追加或加第二 matcher）、把腳本放到對應 hooks 目錄；可一鍵移除。
- attribution + sources.lock 釘 Matt git-guardrails。

### 3. `terse`（新技能，英文 + 語言感知規則）
- **定位**：取代 caveman。手動開關的省 token 模式。
- **核心修正（解決中文怪腔怪調）**：**砍內容、不砍文法**。刪開場白、避險詞、複述問題、客套、
  重複；答案先講。**語言自適應**：中文維持自然臺灣繁體語法（不要電報式/文言）、英文才可電報式。
- 與 `humanizer` 互補：humanizer 管「像不像人」、terse 管「省不省 token」；兩者都不砍正確文法。
- 安全例外（承 Matt）：資安警告、破壞性操作確認時自動退出精簡。

### 4. `to-issues`（新技能，英文）
- **定位**：把計畫/規格/PRD 拆成可獨立認領的 GitHub issue（曳光彈垂直切片、依相依順序），
  是 `design-gate` 的天然下游。
- 流程：讀計畫 → 切成垂直切片 → **先把 issue 清單（標題+切片+相依）整份給使用者確認** →
  才用 `gh issue create` 逐一建立、掛 `ready-for-agent` 之類標籤。用使用者已登入的 `gh`，
  技能本身不碰 token。
- 邊界：design-gate 出計畫 → to-issues 發布；不重複 design-gate 的規劃。
- attribution + sources.lock 釘 Matt to-issues。

### 5. ADR + 統一語彙增補進 `design-gate`
- 在 design-gate 的設計階段加：**統一語彙**（對齊時沉澱專案術語表）與 **ADR 即時落檔**。
- ADR = Architecture Decision Record：一決策一檔放 `docs/adr/NNNN-<topic>.md`，Nygard 精簡格式
  （脈絡/決策/後果/狀態），不改舊檔、要變用新檔 superseded。
- 形式：在 design-gate 加一個 `references/adr.md`（格式 + 何時寫），SKILL.md 設計階段提示
  「重要決策當場落 ADR、沉澱術語」。更新 design-gate attribution 註明 grill-with-docs 啟發。

## 撰寫語言
全部英文（工程/流程技能，照房規）；description 帶中文觸發語。`terse` 的規則本身語言感知。

## 登錄（每個新技能都要）
apm.yml `- ./<skill>/`、README 自建表、skill-map（條目 + 邊界列）、全域 symlink、apm install。
design-gate 增補不需新登錄，但 skill-map 的 design-gate 條目補一句 ADR/語彙。

## 成功標準
1. tdd：給一個功能 → 先紅後綠的迴圈，測試驗意圖；範例含協定整合測試。
2. git-guardrails：裝後 `git push --force` 被擋、`git status` 正常；RTK hook 仍在。
3. terse：中文提問用精簡模式 → 自然臺灣繁體、只是更短，不是電報體；英文可電報式。
4. to-issues：給計畫 → 先出 issue 清單給確認、確認後才建立。
5. design-gate：設計時產出 ADR 檔到 docs/adr/、術語沉澱。
6. 全部：零網路外洩、零讀金鑰（git-guardrails/to-issues 只用使用者既有 CLI）。

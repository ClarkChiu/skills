# daily-brief — 設計文件

- 日期：2026-06-28
- 狀態：**已核准**（使用者拍板：build-your-own、名 daily-brief、英文 SKILL.md、走 design-gate→skill-creator）
- 研究與裁決：`research/2026-06-28-skill-research-log.md`（skill-curator 完整管線，裁決 🟦 自製）
- 公開索引：`research/skill-index.md`（2026-06-28 列）

## 1. 目的與範圍

**做什麼**：一個自建技能 `daily-brief`——單一功能、無狀態的「每日優先級日報引擎」。讀進當日的
待辦／收件匣／行事曆／脈絡／昨日未竟，輸出一份排好優先級、精簡、可掃讀的日報。

**為什麼自製（不裝外部）**：研究顯示此領域最有名的東西是**純文字提示**（AI Chief of Staff、
CEO brief、艾森豪提示），無可維護正典；整合型 agent（OpenPaw/geoffrey/…）價值在 macOS 專屬
程式整合，與使用者（Linux/GCP/終端）不合。價值落在 prose ＋強客製需求（多語、PM 風格、與既有
技能整合）＝自製。繁中頭部作者（Esor、unclef）也主張「不給萬用咒語、依個人脈絡自建」，正好支持
為這位使用者做貼合版。

**不做什麼（範圍外）**：
- **不自建送達層**（定時、寄信）——用內建 `schedule` 觸發即可。
- **不自建輸入整合**（讀 Gmail/Calendar 的 OAuth、MCP 連線）——輸入由日後的 MCP/agent 餵進來；
  本技能只負責「把輸入變成日報」這一段，保持無狀態、可被 agent 串。
- 不做多輪對話式的「規劃系統教學」（那是繁中咒語的路線）；本技能是單次函式。

## 2. 引擎提示（draft B，已定稿）

技能核心是一段英文引擎提示，內容即對話中收斂的 draft B 終版：

- **Role**：使用者的 daily chief-of-staff；signal over noise，產出一份而非清單傾倒。
- **Inputs**（任一可缺，`TASKS` 為唯一必填）：`TASKS` / `EMAIL` / `CALENDAR` / `CONTEXT` /
  `YESTERDAY` / `DATE`。
- **Method**（7 步）：1 昨日盤點（回顧迴圈＋反覆延後偵測）→ 2 Email 萃取（從收件匣抽出該做的
  事、濾雜訊）→ 3 艾森豪分類（DO/SCHEDULE/DELEGATE/DROP）→ 4 Frog（最難先做）→ 5 1-3-5 塑形
  （超出明確延後）→ 6 減法（點名 1–2 件可砍）→ 7 負荷檢查（估時 vs 行事曆）。
- **Output**：跟隨輸入語言；中文輸出套**盤古之白**（漢字與拉丁字母／數字間留白，負荷檢查數字最多
  最明顯）；email 友善、可掃讀；預設分段式，有排程才另出整點時間軸表（繁中偏好）。八個區塊標籤：
  🔙 昨日盤點 / 🎯 今日焦點 / 🐸 先吃這隻青蛙 / 📅 已排程／可延後 / 📤 委派／批次／刪除 /
  ⏱ 負荷檢查 / ✂️ 今天可以不做 / ⭐ 若只做一件事。
- **Guardrails**：不虛構任務/死線/優先級（缺則問或標假設）；失敗大聲（延後/刪除要明說，不靜默）；
  一次一份、不說教。

## 3. 已核准的技能建構決定

1. **名稱**：`daily-brief`。
2. **SKILL.md 語言＝英文**：語言無關的流程/生產力技能，且本就多語設計（輸出跟隨語言），比照
   `decision-lens`。對話回覆仍臺灣繁體中文。
3. **`allowed-tools`：`Read`**——當使用者指向一份 todo/email 檔時可讀取；其餘輸入走 inline 或
   MCP，不需 Write/Bash/網路（最低風險層，純 prose 引擎）。
4. **屬「改寫自上游觀念」** → 配 `attribution.md`＋`sources.lock`（成對）：艾森豪/GTD/Ivy Lee/
   1-3-5 為公開方法（principles only，無檔案收錄）；提示範式參考 AI Chief of Staff／CEO brief；
   多語設計參考 NirDiamant/Prompt_Engineering；提示庫參考 0x2e-Tech/awesome-ai-prompts；繁中
   在地化來源（bnext/technice/playpcesor）記在 attribution 敘述。sources.lock 釘可由 skill-evolve
   追蹤的 GitHub 源（NirDiamant、awesome-ai-prompts）。

## 4. 檔案結構

```
daily-brief/
  SKILL.md                      # 英文；frontmatter(name/description 帶觸發語/allowed-tools: Read)
                                # ＋ 引擎提示（draft B 終版）＋ 用法（含「送達用內建 schedule」指引）
  references/
    prioritization.md           # 框架速查：艾森豪/Eat-the-Frog/1-3-5/減法 的一頁說明（引擎引用）
    attribution.md              # 來龍去脈（公開方法 principles-only、提示範式、繁中在地化）
  evals/
    evals.json                  # 測「意圖」非只「行為」，每案附斷定，可確定性判斷者標 deterministic
  sources.lock                  # skill-evolve 基準（NirDiamant、awesome-ai-prompts 等 GitHub 源）
```

無 `scripts/`：純 prose 引擎、無確定性程式邏輯，故無 pytest；`evals.json` 即驗證層
（CLAUDE.md §2「非平凡邏輯留一個可跑檢查」——此處邏輯在提示，檢查在 evals 的意圖斷定）。

## 5. 登記（房規清單）

- `apm.yml`：加 `- ./daily-brief/`。
- `README.md`：自建技能表加一列。
- `skill-curator/references/skill-map.md`：歸到「Standalone tools」，補與 `decision-lens`(Crux)、
  `to-issues`、`solo-think`、內建 `schedule` 的邊界。
- symlink `~/.claude/skills/daily-brief` → repo（全域可用；apm install 只進專案範圍）。

## 6. 測試／驗證（evals 意圖斷定）

- **觸發**：「幫我排今天的待辦」「每日日報」「daily brief」「把這些 email 整理成今天該做的」應
  觸發 daily-brief，不誤觸 decision-lens（一次性決策）或 to-issues（發 GitHub issue）。
- **行為意圖**：給一組亂序 TASKS → 輸出含艾森豪分類＋Frog＋若只做一件事；給 YESTERDAY 有反覆未竟
  → 觸發「反覆延後要做決定」而非再延後；中文輸入 → 中文輸出且**數字與漢字間有盤古之白**；給
  newsletter 類 EMAIL → 不被當成任務。
- **邊界斷定**：純決策問題（該不該換工作）→ 不該是 daily-brief；要發 GitHub issue → 不該是
  daily-brief。

## 7. 邊界（skill-map 用）

- vs `decision-lens` Crux：daily-brief＝每日輕量待辦分流（recurring）；Crux＝一次性重量級問題優先級
  決策（評分決定性/牽引性/階段性）。cadence 與重量不同。
- vs `to-issues`：daily-brief＝個人日報；to-issues＝把計畫發成 GitHub issue。
- vs `solo-think`：daily-brief＝對外可用的結構化日報（給人看/寄信）；solo-think＝只向內反思、不對外。
- vs 內建 `schedule`/`loop`：daily-brief＝內容引擎；schedule＝定時觸發＋送達（兩者組合＝每日自動日報）。

## 8. 撰寫語言

SKILL.md／references／attribution＝英文（流程技能、多語設計、利 skill-evolve 比對）。evals.json 的
說明文字可中英，輸入樣本維持原樣。對話回覆＝臺灣繁體中文。

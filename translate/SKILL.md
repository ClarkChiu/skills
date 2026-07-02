---
name: translate
description: >-
  EN↔zh-TW 雙向翻譯（臺灣繁體中文），兩種模式：快翻（直翻）與精翻（分析→初稿→
  批評診斷→依批評重翻，發表品質）。USE THIS SKILL when the user asks to
  翻譯、快翻、精翻、中翻英、英翻中、「把這段翻成中文／英文」、"translate to
  Chinese/English"、"refined translation"、"translate this article/file", or
  provides English/Chinese text with translation intent. 承重紀律：精翻的批評
  步驟只診斷、不動筆改寫。Do NOT use for language pairs other than EN↔zh-TW;
  do NOT use to de-AI a finished text (that's humanizer) or to fix
  punctuation/typography (that's chinese-typography).
allowed-tools: Read, Write, Edit, Grep, Glob
---

# translate — EN↔zh-TW 三段式翻譯

雙向翻譯：英文 ↔ 臺灣繁體中文。核心是三段式紀律——初翻 → 自我批評（**只診斷**）→ 依批評重翻——讓譯文讀起來像目標語言原生寫成，而不是「翻出來的」。

## 模式

| 模式 | 步驟 | 產出 | 何時用 |
|---|---|---|---|
| 快翻 | 直翻（套下方原則＋詞彙表） | 對話內直接給；來源是檔案才寫檔 | 短文、隨手翻、非發表用 |
| 精翻 | 分析 → 初稿 → 批評 → 重翻 | `01`–`04` 中間檔＋最終稿 | 要發表、重要文件 |

**觸發與升級規則：**

- 說「快翻」「隨手翻」→ 快翻；說「精翻」「要發表」「出版品質」→ 精翻。
- 只說「翻譯」→ **預設快翻**。但若輸入是整份檔案、或超過約 800 字，先提示一句：「這份篇幅較長，若要發表建議精翻；繼續快翻嗎？」使用者不換就照快翻做。
- 快翻完成後固定提示：「要再往上走一層，說『繼續精翻』。」升級時把快翻結果存為 `02-draft.md` 當初稿，**MUST NOT 重翻**，補齊術語分析後直接進批評步。

## 翻譯原則（兩模式都適用）

1. **重寫而非直譯**：品質測試是「這段讀起來像不像目標語言原生寫的？」不像就重寫。
2. **事實優先**：數字、日期、專有名詞、邏輯 MUST 與原文一致；不確定的術語保留原文並標註，不要硬猜。
3. **自然語序**：長句拆短；比喻與慣用語按意圖轉譯，不逐字。
4. **術語一致**：全文同一譯法；專業術語首次出現以括號附原文。
5. **格式保留**：markdown 結構（標題、粗體、連結、圖片、表格）原樣保留；程式碼區塊內容、程式識別字、JSON 欄位名 **MUST NOT 翻譯**。
6. **註釋節制**：預設讀者是技術背景，只在真的缺脈絡時加簡短說明。

## 詞彙表（譯入 zh-TW 時的權威順序）

高層凌駕低層，遇到就查、**讀檔不複製**：

1. `chinese-typography/user-dictionary.json` 的 `replacements`（機械強制層，例：訊令→信令）
2. `chinese-typography/references/glossary.md`（個人用詞釘選＋但書）
3. 本技能 [references/terms-en-zhtw.md](references/terms-en-zhtw.md)（EN↔zh-TW 術語對照，網路／測試／雲端領域）
4. 臺灣一般出版慣例（OpenCC s2twp 詞彙取向）

譯出 EN 時只用第 3 層反查（zh-TW→EN 術語）。

## 精翻流程

四步、每步一檔，詳細模板見 [references/refined-workflow.md](references/refined-workflow.md)：

| 檔 | 內容 |
|---|---|
| `01-analysis.md` | 內容摘要、全文術語表、語氣評估、翻譯難點 |
| `02-draft.md` | 初稿 |
| `03-critique.md` | **只診斷**：問題清單（類別／位置／描述／修法）＋統計 |
| `04-final.md` | 依批評逐項修正的最終稿 |

**承重規則：批評步 MUST NOT 在同一步改寫譯文**——邊看邊改會讓批評流於表面。批評依方向讀對應清單：EN→zh-TW 用 [references/critique-en2zhtw.md](references/critique-en2zhtw.md)，zh-TW→EN 用 [references/critique-zhtw2en.md](references/critique-zhtw2en.md)。

**輸出位置**：來源是檔案 → 檔案旁 `<basename>-zhtw/`（或 `<basename>-en/`）；來源是對話貼文 → 中間檔寫進系統暫存區，最終譯文直接貼回對話。

## 長文（無分塊腳本的策略）

先通讀**全文**完成 `01-analysis.md`——術語表在這一步建立，就是跨節一致性的保證——再按標題分節翻譯、依序合併；節間銜接問題交給批評步兜底。

天花板：幾萬字級長文若出現節間不一致，屆時再評估加 Python 分塊腳本；現在不做。

## 完成時的下游建議（不自動執行）

- 譯入 zh-TW → 建議跑 `chinese-typography` 正規化（純中文一般文字，安全）。
- 要發表 → 正規化之前先過 `humanizer` 去 AI 味。

## 邊界

- **翻譯腔**（源語言結構殘留：歐化句、中式英文）歸本技能的批評清單；**AI 生成腔**（灌水、三段式、AI 詞彙）歸 `humanizer`——兩邊不複製彼此規則。
- **排版**（盤古之白、全形標點、簡轉繁、異體字）歸 `chinese-typography`，本技能的批評只做預檢、不代勞。
- 只做 EN↔zh-TW，其他語言對不接。

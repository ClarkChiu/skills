# slide-deck — CJK／Latin 字體軸 設計文件

- 日期：2026-06-28
- 狀態：**已核准**（使用者拍板：方案 A、CJK 家族黑名單、`--selftest`；2026-06-28）
- 由來：`skill-evolve` 2026-06-28 巡檢，從上游 `hugohe3/ppt-master`（v2.11.0）萃取
  「CJK 與 Latin 字體獨立選配、依語言偵測決定字體堆疊」這條設計原則。借觀念、用
  slide-deck 自己的零相依 HTML 實作，不抄上游程式碼。研究紀錄見 `slide-deck/sources.lock`
  的 `hugohe3/ppt-master` 條目。

## 1. 目的與範圍

**做什麼**：把「CJK 與 Latin 是兩條獨立的字體軸」這件事，從目前散落、隱性的狀態，
formalize 成 slide-deck 設計系統裡一條明確的原則，並加一條確定性的 linter 檢查擋住最
常見的兩個失誤。

**為什麼是這條、而不是兩條**：上游偵察原本提了兩條原則，但對照 slide-deck 現況後，
只有字體軸是真缺口：

- **資訊密度雙檔——已完整覆蓋，本案不做。** `principles.md` §9「Density modes」已是
  Speaker-led／Reading-first 雙模對照表（bullet 上限、字級、頁數、留白），§10「Deck
  rhythm」更有 anchor/dense/breathing 的節奏層；連上游另一招「先產 2–3 張真實首頁讓人
  選風格」`SKILL.md` Phase 2 也早有（show, don't tell）。frontend-slides／ppt-master 的
  密度觀念，slide-deck 沒有缺。**故 `slide-deck/sources.lock` 的 `zarazhangrui/frontend-slides`
  與 `hugohe3/ppt-master` 之中，密度面判為無實質。**
- **CJK／Latin 字體軸——真缺口，但很窄。** §13 已處理**尺寸軸**（CJK 標題縮 25–30%、
  混排行高偏高），但**字體家族堆疊的獨立性**沒有明訂規則。

**不做什麼（範圍外）**：
- 不動密度模式（§9）與節奏層（§10）。
- 不新增任何第三方字體檔或相依（slide-deck 的零相依鐵則不變）。
- 不做字體的視覺預覽工具（Phase 2 的 show-don't-tell 已足夠）。

## 2. 缺口的具體樣貌（現況）

每個 style preset 的字體是**單一有序堆疊**，例如 `style-presets.md`：

```css
--font-display:"Switzer",sans-serif; --font-body:"Switzer",sans-serif;
```

而現行 CJK 指引（`style-presets.md` 131–133 行）只說「把 `Noto Sans TC` / `Noto Serif TC`
**加進**相關字體堆疊」。這在 Latin 字體排前面時剛好可行——CSS 逐字 fallback 會讓 Latin
字母命中 Latin face、Han 字落到 CJK face。但有三個沒被講清楚、會出錯的點：

1. **順序紀律沒寫死**：若有人把 CJK 家族排在第一（`"Noto Sans TC","Switzer",…`），CSS 會
   用 CJK face 去算繪 Latin 字母——多數 CJK 字體的 Latin 字形扁平／近等寬，整份簡報的西文
   品質被拉低。這是隱性、肉眼不一定立刻看出的失誤。
2. **依語言載入沒寫**：純 Latin、無 Han 的簡報若仍宣告 CJK webfont，整套 CJK 是 MB 級，
   未 subset 的強制載入會拖慢甚至當掉 PDF 匯出（呼應 §3 既有的 webfont 紀律）。
3. **雙 face 搭配沒指引**：CJK face 要去配 Latin face 的字重與調性，否則兩個字面讀起來
   像兩個人講話。

## 3. 已核准的設計決定

1. **文件落點＝方案 A**：字體家族規則寫進 `principles.md` **§3（the type scale）**——字體
   宣告本就屬這一節；尺寸軸維持在 §13；`style-presets.md` 的 CJK 註記更新指回 §3。
   （否決方案 B 另開新章節——會跟 §13 重疊切碎；否決方案 C 只改 preset 註記——核心的
   「Latin 優先序」進不了主原則、分量不足。）
2. **同時加一條 linter 機械檢查**：確定性的失誤交給 `check_deck.py`，符合技能「機械規則
   交給 linter」的既有慣例。
3. **自我檢查用 `--selftest` 旗標**：本技能無 pytest 框架，照 CLAUDE.md Rule 9／§2「非平凡
   邏輯留一個可跑檢查」，用無框架的 assert 式自我檢查。

## 4. 要寫進文件的內容（原則層）

### 4.1 `principles.md` §3 新增一段「兩軸字體（CJK＋Latin 是兩個 face）」

緊接在 §3 現有的「Webfont discipline」項之後，新增：

> **兩軸字體（CJK 與 Latin 是兩個 face，不是一個）。** 雙語簡報用的是兩個字型家族，不是
> 一個：一個 Latin face、一個 CJK face，組成一條**有序的** `font-family` 堆疊。規則：
>
> - **Latin face 在前、CJK face 在後**：`font-family:"Switzer","Noto Sans TC",sans-serif`。
>   逐字 fallback 於是讓 Latin 字母用 Latin face、Han 字落到 CJK face。**絕不把 CJK 家族
>   排第一**——它的 Latin 字形通常扁平／等寬，會把整份簡報的西文拉低。
> - **挑 CJK face 去配 Latin face**：grotesque／sans 的 Latin → 配 `Noto Sans TC` 一類
>   黑體；serif／display 的 Latin → 配 `Noto Serif TC` 一類明體。字重與調性對齊，讓兩個
>   face 讀起來是同一個聲音。
> - **依簡報主導語言決定載入**：先決定這份簡報是 Latin 主導還是 CJK 主導。Latin 主導、
>   通篇無 Han 的簡報**不得**載入 CJK webfont——整套 CJK 家族是 MB 級，未 subset 的強制
>   載入會拖慢／當掉 PDF 匯出（見本節 Webfont discipline）。CJK 主導的簡報則仍要在堆疊裡
>   保留一個真正的 Latin face，給內嵌的術語、數字、日期用。
> - 跨兩軸的**尺寸**已在 §13 處理（CJK 標題 −25–30%、混排行高偏高），此處不重複。

### 4.2 `style-presets.md` 131–133 行改寫

把現行「add `Noto Sans TC` / `Noto Serif TC` to the relevant font stack」改寫為明確的
**Latin 優先有序堆疊＋依語言主導決定載入**，並指回 `principles.md` §3：

> - 雙語簡報用兩軸字體：把 CJK face **接在 Latin face 之後**組成有序堆疊
>   （`"<Latin>","Noto Sans TC",sans-serif`），不可讓 CJK 家族排第一。依簡報主導語言決定
>   要不要載入 CJK webfont——純 Latin 簡報不載。完整規則見 `principles.md` §3「兩軸字體」。

### 4.3 `SKILL.md` Phase 4「Generate」補半行

在「Replace the `:root` variables with the chosen preset」一句後補：

> 雙語簡報的字體堆疊遵守 §3 兩軸順序（Latin face 在前、CJK face 在後）。

## 5. linter 檢查（`check_deck.py` 第 8 條）

在現有第 7 條（overflow 檢查）之後新增一段，產生兩個確定性 WARN。

### 5.1 CJK 家族黑名單（已核准）

以小寫子字串比對，涵蓋常見 CJK 字型家族：

```
"noto sans tc", "noto serif tc", "noto sans sc", "noto serif sc",
"noto sans jp", "noto serif jp", "noto sans hk", "source han",
"pingfang", "microsoft yahei", "hiragino", "heiti", "songti",
"ms mincho", "ms gothic", "simsun", "simhei"
```

### 5.2 兩個檢查

訊息語言：與既有 7 條 WARN 一致採**英文**（Rule 11 順從 linter 既有慣例；輸出是程式產物）。

1. **順序 bug**：逐一解析每條 `font-family:` 宣告，切成 token；若某個 CJK 家族 token 出現
   在「任何非 CJK、非 generic（sans-serif/serif/monospace）家族」**之前**，發
   `WARN  CJK font listed before the Latin family in a font stack — Latin glyphs will render in the CJK face; put the Latin family first`。
   （注意：純 `"Noto Sans TC",sans-serif` 這種「CJK＋generic、無獨立 Latin face」的堆疊**不**
   觸發——只有當確實有一個 Latin 家族被排到 CJK 之後才算順序錯。）
2. **載入未用**：若整份文件出現任一 CJK 家族（webfont 載入或堆疊引用），但既有的 `CJK_RE`
   在投影片文字裡找到 **0 個** Han 字 → 發
   `WARN  CJK webfont declared but the deck has no Han glyphs — drop it to keep the file light and PDF-safe`。

### 5.3 自我檢查 `--selftest`（已核准）

在 `main()` 加一個分支：`python3 check_deck.py --selftest` 時，對兩段內嵌樣本字串跑第 8 條
的偵測函式並 assert：

- 樣本 A（CJK-first，含 Han）：應觸發「順序 bug」WARN、不觸發「載入未用」。
- 樣本 B（Latin-first，含 Han）：兩個 WARN 都不觸發。
- 樣本 C（宣告 CJK webfont、但無 Han 字）：應觸發「載入未用」WARN。

全部 assert 通過則印 `selftest OK` 並 return 0；否則 return 1。把第 8 條的偵測抽成一個
純函式（吃 doc 字串、回傳 warn 清單），讓 `audit()` 與 `--selftest` 共用，避免重複邏輯。

## 6. 測試與驗證

| 驗證 | 指令 | 預期 |
|---|---|---|
| 新檢查自我測試 | `python3 slide-deck/scripts/check_deck.py --selftest` | 印 `selftest OK`、exit 0 |
| 不誤報既有 CJK 簡報 | `python3 slide-deck/scripts/check_deck.py slide-deck/examples/txone-profile.zh-TW.html` | 第 8 條不產生新 WARN（其字體堆疊應為 Latin-first 且有 Han 字） |
| 既有檢查不回歸 | 同上 | 既有 errors/warns 數量不因本次改動而改變 |

## 7. 改動的檔案清單

| 檔案 | 改動 |
|---|---|
| `slide-deck/references/principles.md` | §3 新增「兩軸字體」一段（4.1） |
| `slide-deck/references/style-presets.md` | 131–133 行改寫（4.2） |
| `slide-deck/SKILL.md` | Phase 4 補半行（4.3） |
| `slide-deck/scripts/check_deck.py` | 第 8 條兩個 WARN ＋ 抽純函式 ＋ `--selftest`（5） |
| `slide-deck/sources.lock` | bump `frontend-slides`／`ppt-master` 兩個 pending 源，記載採納結果 |

## 8. 撰寫語言

slide-deck 是主題綁中文排版的技能，`principles.md`／`style-presets.md`／`SKILL.md` 既有內容
即為臺灣繁體中文，本次新增段落沿用中文。`check_deck.py` 是程式，註解與
**WARN 訊息沿用其既有英文風格**（既有 7 條 WARN 皆英文，Rule 11 順從慣例；§5 已定）。

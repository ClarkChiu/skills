# social-card 第三風格家族「Sweet（甜美系）」設計

> 2026-07-02。原則參考 `JimLiu/baoyu-skills` 的 baoyu-xhs-images `cute` 預設與 baoyu-infographic `kawaii` 風格（MIT，**原則自寫、零檔案收錄**；評估見 `research/audits/2026-07-02-baoyu-skills.md`）。對話中已確認做第三家族；濃度採「收斂甜美系」為暫定假設（使用者離線時依建議選項推進，可推翻）；機讀元素組合結構裁決不採（見 §6）。

## 1. 目標與範圍

**目標**：給 social-card 補上甜美系視覺語言，涵蓋現有 Swiss（技術理性）／Editorial（雜誌敘事）都不合身的內容：旅遊、美食、生活、個人分享（近期實例：越南旅遊貼文）。

**範圍內**：`style-system.md` 新家族一節＋兩個原創色盤；`assets/template-sweet.html` 起手模板；SKILL.md 家族選擇表更新；家族×版式角色相容小表；裝飾紀律文字規則；attribution／sources.lock 補上游；evals 補案。

**非目標**：不做滿版 kawaii（愛心星星鋪滿、Q 版臉、臉紅裝飾）；不改 qa-rules.js（既有規則家族無關，裝飾壓字若日後成為實際問題再加腳本規則——天花板註記）；不重構為機讀 YAML 結構；不動 layouts.md 的版式角色與字數上限；不新增平臺比例。

## 2. 家族規格（寫進 style-system.md 的內容要點）

**選擇時機**（家族選擇表加一欄）：旅遊、美食、生活風格、個人分享、輕鬆話題 → Sweet；技術／資料 → Swiss；敘事長文 → Editorial 不變。

**視覺語言**：
- **形**：大圓角（24–32px，比 Editorial 的 subtle radius 更明顯）、貼紙式元素（白色粗描邊 sticker outline）、拍立得相框作為照片處理的家族變體（銜接 `screenshot-treatment.md`）。
- **字**：圓潤無襯線（rounded sans 系統字族優先，如 system rounded fallback 堆疊）；標題可帶極輕的手寫感傾斜；**字級階梯與地板沿用既有 type scale，不另立**。
- **裝飾**：手繪風塗鴉（心、星、花、波浪線）以 CSS／inline SVG 原創繪製；**MUST 每卡最多 3 個裝飾元素、MUST NOT 壓到文字**；裝飾用 `--deco` 色、低視覺權重（縮小、降不透明度）。
- **既有鐵則全數沿用**：一卡一想法、先砍字不縮字、安全區、零第三方資產。

**兩個原創色盤**（沿用四變數契約＋新增選用 `--deco`）：

```css
/* macaron — 粉彩草莓；旅遊、生活 */
.theme-macaron { --paper:#fff5f7; --ink:#46323d; --muted:#a38a95; --accent:#e0507e; --deco:#8fd0c5; }

/* cream-mint — 奶油薄荷；美食、清爽話題 */
.theme-mint    { --paper:#f4faf5; --ink:#2e4137; --muted:#7c988a; --accent:#e8933a; --deco:#f2b8c6; }
```

ink 對 paper 的對比維持既有「舒適餘裕」標準（兩組皆深墨於極淺紙底，目測 >10:1，實作時以 QA 目視確認）。

## 3. 家族×版式角色相容表（輕量學 xhs 的相容表想法）

| 版式角色 | Swiss | Editorial | Sweet |
|---|---|---|---|
| cover | ✓ | ✓ | ✓（裝飾可稍多，仍 ≤3） |
| points | ✓ | ✓ | ✓ |
| checklist | ✓ | ✓ | ✓（勾選符號可用手繪風） |
| comparison | ✓ | ✓ | △（表格線改圓角卡） |
| quote | ✓ | ✓ | ✓ |
| stat | ✓ | △ | △（大數字可用 accent，不加裝飾） |
| summary/CTA | ✓ | ✓ | ✓ |

放進 `style-system.md`，選型時查表；△＝可用但注意事項照括號。

## 4. 模板與檔案

- 新增 `assets/template-sweet.html`：結構同既有兩個模板（fixed-dimension `<section class="card ig-45">`＋theme class＋CSS 變數區塊），內建 macaron 主題示範一張 cover＋一張 points、貼紙描邊與塗鴉的 CSS 寫法範例。
- `references/style-system.md`：標題改「three families」、加 Sweet 一節＋色盤＋相容表。
- `SKILL.md`：描述與家族列舉處同步（Swiss + Editorial + Sweet）。
- `references/attribution.md`＋`sources.lock`：補 `JimLiu/baoyu-skills`（principles only，釘 `a4e78af8136f`）——與既有 guizang 條目並列。
- `evals/evals.json` 補兩案：旅遊內容觸發 Sweet 家族；裝飾紀律（每卡 ≤3、不壓字）。

## 5. 品管

qa-rules.js 不改。裝飾紀律是文字規則（§2 的 MUST），由既有 QA 的目視步驟把關；`render-qa.md` 的檢查清單加一行「Sweet 家族：數裝飾元素、查壓字」。
`# 天花板：若裝飾壓字在實際使用中反覆出現，屆時在 qa-rules.js 加 .deco 與文字節點的重疊檢查`。

## 6. 裁決記錄：不採機讀元素組合結構

xhs-images 把風格拆成 canvas／image_effects／typography／decorations 四軸機讀 YAML＋相容表。**不採**，理由：三個家族的選型一張文字表就零錯誤，機讀索引的價值在家族多（frontend-slides 34 套才需要 selection-index）或代理選型頻繁出錯時才顯現；現在上＝為三列資料建一套 schema（YAGNI）。只取它的「相容表」想法（§3）。重評條件：家族 ≥5 或選型錯誤實際發生。

## 7. 驗收準則（Given/When/Then）

1. Given 一篇越南旅遊筆記要做 IG 4:5 輪播，When 執行 social-card，Then 選型落在 Sweet 家族（或明述為何不選），色盤為 macaron／mint 之一。
2. Given Sweet 家族產出的任一張卡，When 檢視，Then 裝飾元素 ≤3、無裝飾壓字、字級不低於既有地板。
3. Given 技術文章輸入，When 執行，Then 仍預設 Swiss——Sweet 不搶既有內容的預設位。
4. Given 產出的 HTML，When 檢查資源，Then 無第三方字型檔／圖片資產（塗鴉為 CSS／inline SVG 原創）。
5. Given `sources.lock`，When skill-evolve 掃描，Then 能看到 guizang 與 baoyu 兩個上游條目各自釘定。

## 8. 自我審查

- 濃度假設（收斂甜美系）為暫定，使用者可推翻——若改「全力 kawaii」則 §2 裝飾上限與 §5 需重寫。
- 無佔位符；色盤 hex、圓角值、裝飾上限皆具體。
- 一致性：§2 沿用既有 type scale 與四變數契約，與 style-system.md 現況相容；§5 不改腳本與 §1 非目標一致。
- 範圍：單一技能內的增量，不跨子系統，不需拆分。

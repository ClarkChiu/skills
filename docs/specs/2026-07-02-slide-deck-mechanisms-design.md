# slide-deck 機制升級設計（版式鎖＋選型表＋預覽銳化）

> 2026-07-02。原則參考：`op7418/guizang-ppt-skill` 的版式鎖＋校驗器（**AGPL-3.0，僅取原則、零檔案**；評估 `research/audits/2026-07-02-guizang-ppt-skill.md`）與 `zarazhangrui/frontend-slides` 的機讀選型中繼資料（MIT，已在 sources.lock 追蹤；評估 `research/audits/2026-07-02-frontend-slides.md`）。
> **流程備註**：使用者批次指令「三項依序做完」後離線，設計→執行連走、獨立提交可撤銷。
> **範圍修正**：原備忘錄的「漸進揭露」確認不做——風格庫是單一 135 行檔案，無情境成本問題（YAGNI）；「3 預覽先選」已存在於 SKILL.md Phase 2，本輪只銳化組成規則。

## 1. 改動一：版式鎖（主菜，guizang 原則）

**現況**：`assets/template.html` 七個原型已帶 `data-label`，`check_deck.py` 只在「有標且是 content/agenda」時查 bullet 上限——沒標的投影片逃過全部角色檢查。

**升級**（原則：約束讓 AI 產出更可靠；版式登記表擋「自創版式」）：
- 登記表＝`layouts.md` 的九角色（正規化後）：`cover, agenda, section, content, bignumber, quote, comparison, timeline, closing`（接受 `big-number`／`section-divider` 等連字號變體與任意大小寫）。
- `check_deck.py` 新增兩檢查（**皆 WARN**，`--strict` 才擋——既有簡報不破）：
  - 投影片缺 `data-label` → WARN「無法做角色檢查，補上登記角色名」。
  - `data-label` 不在登記表 → WARN「未登記的版式（列合法清單）——自創版式是版面品質不穩的主因」。
- 擴充機械上限：沿用 content=5、agenda=6 bullets；新增**稀疏角色字數上限**——cover／section／closing／bignumber／quote 屬「近空」角色（layouts.md 密度表），可見文字單位 > 50 → WARN（quote 的 ≤36 Han/22 EN 由此涵蓋）。
- `--selftest` 加三案：缺標、未登記角色、quote 超字數。
- `layouts.md` 補一行「每張投影片 MUST 帶登記角色的 `data-label`——這是校驗器做角色檢查的鉤子」；SKILL.md Phase 4 同步一句。

## 2. 改動二：選型表（frontend-slides 原則）

`style-presets.md` 開頭加機讀選型表：六預設 × `best_for` × **`avoid_for`**（現況只有正向對映，缺反向排除）× 溫度。表與各節文字同源，選型時**先查表再讀中選那節**。

| preset | best_for | avoid_for |
|---|---|---|
| Swiss | 產品、財務、精確嚴肅 | 溫暖敘事、兒童教育 |
| Editorial | 敘事、品牌、演講 | 密集數據、規格審查 |
| Brutalist | 發布、宣言、立場 | 保守客戶、醫療金融合規 |
| Dark Neon | AI、開發者、深夜產品 | 列印為主、明亮會議室投影 |
| Warm Humanist | 教育、醫療、社群 | 硬核技術規格、財報 |
| Technical | 規格、架構、內部審查 | 對外行銷、情感敘事 |

## 3. 改動三：預覽組成規則銳化（兩家獨立收斂的訊號）

SKILL.md Phase 2 的 show-don't-tell 從「2–3 個預設」銳化為：**1 穩（選型表最對位）＋1 大膽（溫度相鄰但更有態度）＋1 外卡**；加**預覽真實性規則**——預覽用真實內容的標題頁，MUST NOT 把內部流程字樣（「方案 A」「preset: swiss」）渲染進投影片畫面。

## 4. 出處與記錄

- attribution.md 補 guizang-ppt-skill（AGPL，**原則非檔**——版式鎖思想；明寫 AGPL 禁收檔）與 frontend-slides 本輪採納項。
- sources.lock：**新增** `op7418/guizang-ppt-skill`（commit 上次稽核 HEAD）；**更新** frontend-slides 的 note（本輪採納 avoid_for 選型表＋預覽組成規則）。
- evals 補一案：產出簡報每張帶登記 `data-label`；校驗器抓得到自創角色。

## 5. 驗收（Given/When/Then）

1. Given 一份有一張投影片缺 `data-label` 的簡報，When 跑 check_deck.py，Then 出現缺標 WARN；`--strict` 下 exit 1。
2. Given `data-label="hero-mega"`（未登記），When 跑校驗，Then WARN 並列出合法角色清單。
3. Given quote 角色塞了 60 字，When 跑校驗，Then 稀疏角色超字數 WARN。
4. Given `--selftest`，When 執行，Then 新舊案例全過、印 selftest OK。
5. Given 既有範例 `examples/txone-profile.zh-TW.html`，When 非 strict 跑校驗，Then exit 0（不破壞既有資產）。

## 6. 自我審查

- 版式鎖採 WARN 不採 ERROR：與 guizang 的硬擋不同——本技能有 `--strict` 機制承接嚴格模式，預設不破壞既有簡報（相容性優先，記錄為刻意偏離上游）。
- AGPL 邊界：只取「登記表＋校驗」的想法，正規化邏輯與字數上限全部原創（check_deck.py 既有結構的延伸）。
- 無佔位符；範圍單一技能。

# social-card Sweet 家族實作計畫

> 依已批准設計 `docs/specs/2026-07-02-social-card-sweet-design.md` 拆任務。
> 取捨（沿用前例）：關鍵 CSS 給全碼；模板結構與文字規格給規格＋驗收標準。
> 硬邊界：不改 qa-rules.js、不動 layouts.md、不收上游任何檔案、塗鴉一律 CSS／inline SVG 原創。

## 任務 1：`references/style-system.md` 加 Sweet 家族

- 標題與開頭：「Swiss and Editorial」→「Swiss, Editorial, and Sweet」；「Two style families, three original palettes」→「Three style families, five original palettes」。
- 選擇表加 Sweet 欄：旅遊／美食／生活／個人分享／輕鬆話題；內容想要親切、柔軟、手作感時。
- 新增「Sweet family」一節：大圓角 24–32px、貼紙白描邊、拍立得相框（照片處理的家族變體，銜接 screenshot-treatment）、rounded sans 字族堆疊、**MUST 每卡裝飾 ≤3、MUST NOT 壓字**、裝飾用 `--deco` 低視覺權重、type scale 沿用不另立。
- 色盤區加兩個主題（全碼）：

```css
/* macaron — 粉彩草莓；旅遊、生活 */
.theme-macaron { --paper:#fff5f7; --ink:#46323d; --muted:#a38a95; --accent:#e0507e; --deco:#8fd0c5; }

/* cream-mint — 奶油薄荷；美食、清爽話題 */
.theme-mint    { --paper:#f4faf5; --ink:#2e4137; --muted:#7c988a; --accent:#e8933a; --deco:#f2b8c6; }
```

- 加設計文件 §3 的家族×版式相容表（含 △ 注意事項）。
- 驗收：`grep -c "theme-macaron\|theme-mint" 檔案` ≥ 2；`grep -c "≤3\|最多 3\|max 3\|at most 3"` ≥ 1。

## 任務 2：`assets/template-sweet.html`（起手模板）

- 骨架照 template-swiss.html：`:root` type-scale 變數、theme class 色盤、`.sheet`／`.card`＋六個固定尺寸 frame class 原樣沿用。
- Sweet 專屬 CSS（關鍵碼）：

```css
/* Sweet base: big radius, sticker outline, restrained doodles */
.card{padding:var(--grid);display:flex;flex-direction:column;border-radius:0;}
.panel{background:var(--paper);border-radius:28px;}
.sticker{display:inline-block;padding:12px 32px;border-radius:999px;
  background:var(--accent);color:var(--paper);font-weight:700;
  border:6px solid #fff;box-shadow:0 4px 0 rgba(0,0,0,.08);}
.polaroid{background:#fff;padding:24px 24px 72px;border-radius:8px;
  box-shadow:0 8px 24px rgba(70,50,61,.15);transform:rotate(-1.5deg);}
.doodle{position:absolute;color:var(--deco);opacity:.8;pointer-events:none;}
```

- 手繪塗鴉：2–3 個 inline SVG 範例（心、星、波浪線，stroke 手繪感、原創繪製）放 `.doodle` 容器，示範絕對定位在留白處（不壓字）。
- 示範卡兩張：cover（macaron 主題、kicker＋圓潤大標＋1 個 sticker＋≤2 個 doodle）＋ points（mint 主題、圓角清單、勾選符號手繪風）。
- 字族堆疊：`"PingFang TC","Noto Sans TC",ui-rounded,"Hiragino Maru Gothic ProN",system-ui,sans-serif`（無第三方字型檔）。
- 驗收：檔內無任何 `http`／`url(` 外部資源；`grep -c "svg" ` ≥ 2；兩張示範卡尺寸 class 正確。

## 任務 3：`SKILL.md` 同步

- description：「(Swiss + Editorial systems, fixed-ratio frames)」→「(Swiss + Editorial + Sweet systems, fixed-ratio frames)」。
- 步驟 2：「(Swiss or Editorial)」→「(Swiss, Editorial, or Sweet)」。
- 步驟 3 模板列舉補 `assets/template-sweet.html`。
- references 清單行「Swiss vs Editorial, original palettes」→「Swiss / Editorial / Sweet, original palettes」。
- 驗收：`grep -c "Sweet" SKILL.md` ≥ 3。

## 任務 4：`references/render-qa.md` 補一行

- 檢查清單加：「Sweet family cards: count decorations (≤3 per card) and confirm no doodle/sticker overlaps text — visual check; not yet in qa-rules.js（天花板：反覆出問題再加腳本規則）」。
- 驗收：`grep -c "Sweet" render-qa.md` ≥ 1。

## 任務 5：`references/attribution.md`＋`sources.lock` 補上游（成對更新）

- attribution 加一節「Sweet family principles adapted from **JimLiu/baoyu-skills**（MIT）」：取 baoyu-xhs-images `cute` 預設與 baoyu-infographic `kawaii` 的甜美系設計語言（馬卡龍色系、貼紙／拍立得元素、圓潤字形方向）＋「元素組合相容表」的想法；**未收任何檔**（上游色票未沿用、塗鴉自畫）；濃度收斂以貼合本技能克制哲學；評估紀錄 `research/audits/2026-07-02-baoyu-skills.md`。
- sources.lock：`checked_at` 更新為 2026-07-02，`sources` 加：

```json
"JimLiu/baoyu-skills": {
  "commit": "a4e78af8136f",
  "release": null,
  "date": "2026-07-02",
  "license": "MIT",
  "skills": ["baoyu-xhs-images", "baoyu-infographic"],
  "note": "Sweet 家族只取甜美系設計語言與相容表想法（cute 預設／kawaii 風格），未收檔、色票原創、濃度收斂。比對重點：上游若新增 cute 系風格預設或改元素組合結構。"
}
```

- 驗收：JSON 合法；兩個上游條目並存。

## 任務 6：`evals/evals.json` 補兩案（id 7、8）

- `sweet-family-selection`：越南旅遊筆記做 IG 4:5 輪播 → 選 Sweet＋macaron/mint 之一（或明述不選理由）；斷定：家族選型正確、技術內容仍預設 Swiss 的邊界不破。
- `sweet-decoration-discipline`：Sweet 家族產出任一卡 → 裝飾 ≤3、不壓字、字級不低於地板、無外部資產；斷定：裝飾計數（deterministic 傾向）、壓字目視、`grep url(` 零命中（deterministic）。
- 驗收：`python3 -c "...len(d['evals'])"` → `8`。

## 任務 7：驗證＋提交

- 跑任務 1–6 全部驗收指令。
- 提交一：`git add social-card/ && git commit -m "✨ feat(social-card): 第三風格家族 Sweet——馬卡龍色盤＋貼紙塗鴉紀律＋相容表"`
- 提交二：`git add docs/specs/2026-07-02-social-card-sweet-design.md docs/plans/2026-07-02-social-card-sweet.md && git commit -m "📝 docs: social-card Sweet 家族設計＋計畫"`

## 完成定義

- [ ] style-system 三家族五色盤、相容表在檔
- [ ] template-sweet.html 自包含（零外部資源）、兩張示範卡
- [ ] SKILL.md／render-qa 同步
- [ ] attribution＋lock 兩上游並存、JSON 合法
- [ ] evals 8 案可解析
- [ ] 兩個提交合規、無 Co-Authored-By

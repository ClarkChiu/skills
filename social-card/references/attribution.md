# Attribution

## Design principles adapted from

**op7418/guizang-social-card-skill**（作者 op7418／歸藏）
- 儲存庫：https://github.com/op7418/guizang-social-card-skill
- 評估紀錄：`research/audits/2026-06-08-guizang-social-card-skill.md`、`research/skill-index.md`

## 取了什麼

只取**設計系統的原則**，不是檔案：
- 「一卡一想法」「先砍字、不縮字」的版面紀律。
- 固定尺寸 frame、安全邊距、標題字數上限、CJK 行高的作法。
- 截圖處理：UI/密集文字用 `object-fit:contain`、物件用 `cover`，依內容設 `object-position`。
- Swiss（紀律）與 Editorial（雜誌）雙風格系統的概念。
- 版面 QA 規則的構想（溢出、字級地板、標題上限）——重寫成 `scripts/qa-rules.js`。

## 改了什麼

- **未收任何上游檔案。** 原作授權**不一致**（repo metadata 標 AGPL-3.0、`package.json` 標 ISC），
  為避免授權污染，一律不收檔；所有模板、色盤、背景皆原創（本技能掛 MIT）。
- **平台改寫**：從小紅書 3:4 / 微信公眾號 21:9+1:1，改成 **IG 4:5 / 1:1 / 9:16 與
  LinkedIn 1:1 / 1.91:1**（FB 降級為單張）。長寬比、安全區、命名全部重定。
- **渲染管線改寫**：原作用 **playwright**（`validate-social-deck.mjs`）渲染與 QA；
  本技能改用 **agent-browser**——`screenshot "#<id>" <path>` 取精確尺寸 PNG（已實測：
  1080×1350 元素截圖正好 1080×1350），QA 規則重寫成餵 `agent-browser eval --stdin` 的
  `scripts/qa-rules.js`。不引入 playwright/chromium。
- **撰寫語言**：英文（工程／工具技能，照本專案「語言看主題」慣例）；description 帶中文觸發語。

## 反預設清單（principles.md §7）

`principles.md` 的「避開 LLM 預設」一節屬通用設計常識（與 `slide-deck` 既有的 anti-slop 同類），
撰寫時受 **Leonxlnx/taste-skill**（MIT）的 anti-default 紀律啟發。該技能的完整裁決與三點吸收的
**權威來源追蹤**放在 `ui-design-advisor`（`references/anti-default.md` ＋ `sources.lock`），
此處不重複釘鎖，只註明出處。評估紀錄：`research/audits/2026-06-08-taste-skill.md`。

## 授權

原作授權不一致，故不收錄其檔案；本技能為原則的原創重述，掛 MIT。

`sources.lock` 釘住上游基準，供 `skill-evolve` 日後比對；上游若改動設計系統或新增版式，回看是否值得吸收。

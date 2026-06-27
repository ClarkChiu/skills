# daily-brief — 任務計畫

- 日期：2026-06-28
- 設計文件：`docs/specs/2026-06-28-daily-brief-design.md`（已核准）
- 內容真相來源：引擎提示終版（draft B）見對話與設計文件 §2；本計畫負責建構順序、登記、驗證。
- 建構工具：`skill-creator`（起草 SKILL.md／evals／優化 description 觸發）。

執行順序：先技能本體（SKILL＋references＋evals＋attribution＋lock）→ 登記三處 → symlink → 驗證 → 提交。

---

## 任務 1 — daily-brief/SKILL.md
- 英文。frontmatter：`name: daily-brief`、`description`（帶觸發語：每日日報/排今天待辦/daily brief/
  把 email 整理成今天該做的；並標 do-NOT vs decision-lens/to-issues）、`allowed-tools: Read`。
- 內文：Role → Inputs → Method(7 步) → Output(含盤古之白規則＋八區塊＋時間軸表選項) → Guardrails，
  即設計文件 §2 的 draft B 終版。另加「Delivery」一節：用內建 `schedule` 定時觸發＋寄送，本技能不自建。
- 驗證：`grep -c "盤古之白\|Eisenhower\|YESTERDAY\|schedule" daily-brief/SKILL.md` 皆 ≥1。

## 任務 2 — daily-brief/references/prioritization.md
- 一頁框架速查（英文）：艾森豪四象限、Eat-the-Frog、1-3-5、減法、負荷檢查；供引擎引用、不重複貼。
- 驗證：檔案存在、含四個框架關鍵字。

## 任務 3 — daily-brief/references/attribution.md
- 來龍去脈（英文）：公開方法（Eisenhower/GTD/Ivy Lee/1-3-5，principles only、無檔案收錄）；提示範式
  （AI Chief of Staff／CEO brief）；多語設計（NirDiamant/Prompt_Engineering）；繁中在地化來源
  （bnext/technice/playpcesor，敘述）。授權、注意事項。
- 驗證：含「principles only」「Eisenhower」「multilingual」字樣。

## 任務 4 — daily-brief/sources.lock
- skill-evolve 基準：釘可追蹤的 GitHub 源（`NirDiamant/Prompt_Engineering`、`0x2e-Tech/awesome-ai-prompts`）
  的 commit/date；公開方法與部落格不放（非 GitHub 可追蹤）。`checked_at: 2026-06-28`。
- 驗證：`python3 -c "import json;json.load(open('daily-brief/sources.lock'))"` → ok。

## 任務 5 — daily-brief/evals/evals.json
- 測意圖（設計文件 §6）：觸發案（排今天待辦/每日日報/email→今天該做的）、不誤觸（純決策→decision-lens；
  發 issue→to-issues）、行為意圖（亂序→艾森豪＋Frog＋若只做一件事；YESTERDAY 反覆未竟→逼決定；
  中文輸入→中文輸出且盤古之白；newsletter email→不當任務）。可確定性判斷者標 `deterministic: true`。
- 驗證：`python3 -c "import json;json.load(open('daily-brief/evals/evals.json'))"` → ok；含 ≥6 案。

## 任務 6 — 登記三處
- `apm.yml`：在 `- ./html-diagram/` 後加 `- ./daily-brief/`。
- `README.md`：自建技能表加一列（中文描述，比照 decision-lens 列風格）。
- `skill-curator/references/skill-map.md`：Standalone tools 加 daily-brief 條目＋邊界（vs decision-lens
  Crux／to-issues／solo-think／內建 schedule）。
- 驗證：三處各 `grep -c daily-brief` ≥1。

## 任務 7 — symlink 全域
- `ln -s /mnt/d/project/skills/daily-brief ~/.claude/skills/daily-brief`
- 驗證：`ls -ld ~/.claude/skills/daily-brief` 為 symlink 指向 repo。

## 任務 8 — 整體驗證
- 所有 JSON 合法；SKILL.md frontmatter 完整（name/description/allowed-tools）；evals 可解析。
- `GITHUB_TOKEN=$GITHUB_TOKEN python3 /root/.claude/skills/skill-evolve/scripts/check_updates.py daily-brief`
  → 能讀 sources.lock、列出源（首次可能顯示 NEW/unchanged，正常）。

## 任務 9 — 提交
- `✨ feat(daily-brief): 每日待辦優先級日報引擎（自製，build-your-own）`，含技能本體＋登記＋設計文件/計畫。

---

## 完工定義
- [ ] daily-brief/ 五檔到位（SKILL/prioritization/attribution/sources.lock/evals）。
- [ ] 登記三處＋symlink 完成。
- [ ] 所有 JSON 合法、frontmatter 完整、evals ≥6 案且測意圖。
- [ ] 一個 commit 落地。

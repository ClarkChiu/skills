# decision-lens — 實作計畫

依 `docs/specs/2026-06-08-decision-lens-design.md`（已核准）。任務循環：先寫失敗測試 →
跑確認失敗 → 最小實作 → 跑確認通過 → 提交。腳本純標準函式庫，測試用 `python3 -m pytest`
（或無 pytest 時用內建 `assert` 腳本）。

## 任務序列

### T1 — bayes_update.py + 測試
- 建 `decision-lens/scripts/bayes_update.py`：兩模式 `odds`（先驗機率 × 概似比串 → 後驗）
  與 `beta`（Beta 先驗 + 成功/失敗 → 後驗均值與近似 95% 區間）。讀 stdin/`--json`，印 JSON。
- 建 `decision-lens/scripts/test_decision_lens.py`（共用測試檔，先放 bayes 案）：
  - `odds`：prior_p=0.5、LR=[2,3] → posterior_odds=6、posterior_p≈0.8571。
  - `beta`：alpha=1,beta=1,successes=8,failures=2 → posterior_alpha=9、posterior_beta=3、
    posterior_mean=0.75。
  - 邊界：prior_p=0 或 1 拋 ValueError；LR≤0 拋 ValueError。
- 驗證：`python3 -m pytest decision-lens/scripts/test_decision_lens.py -q` 全綠。
- 提交：`✨ feat(decision-lens): bayes_update.py — odds 更新 + Beta-Binomial 共軛`

### T2 — kelly_size.py + 測試
- 建 `decision-lens/scripts/kelly_size.py`：`binary`（f*=(b·p−q)/b）與 `scenarios`
  （格點極大化 E[log(1+f·r)]）；分數 Kelly（fraction）與上限（cap）；負期望回「不下注」。
- 測試加案：
  - `binary` b=1,p=0.5 → full_kelly=0、edge=false、recommendation="no edge — do not allocate"。
  - `binary` b=2,p=0.6 → full_kelly=0.4；fraction=0.5 → sized=0.2。
  - `binary` b=2,p=0.6、cap=0.1 → sized=0.1。
- 驗證：pytest 全綠。提交：`✨ feat(decision-lens): kelly_size.py — Kelly f* + 對數成長 + 分數 Kelly`

### T3 — crux_score.py + 測試
- 建 `decision-lens/scripts/crux_score.py`：對每個候選問題評三判準（decisiveness/leverage/
  stage，各 0–1），加權排序，首位＝主要問題。
- 測試加案：
  - 兩問題，A decisiveness=0.9 / B decisiveness=0.2，其餘相同 → primary=A、ranked[0].name=A。
  - 判準值超出 [0,1] 拋 ValueError。
- 驗證：pytest 全綠。提交：`✨ feat(decision-lens): crux_score.py — 主次問題優先級評分`

### T4 — references（四個協定檔，英文）
- `routing.md`：訊號 → 透鏡決策樹；「需澄清」「多重透鏡」分支。
- `bayesian.md`：先驗衛生、概似比分級（要使用者給或標假設）、呼叫 bayes_update.py、行動門檻、敏感度、brief 結構。
- `crux.md`：三判準定義（中性化，無毛澤東品牌）、呼叫 crux_score.py、突破口、監測門檻、brief 結構。
- `kelly.md`：邊際輸入來源紀律、呼叫 kelly_size.py、分數 Kelly 預設、上限與誤用防呆、brief 結構。
- 驗證：四檔存在、互相引用正確。提交：`📝 docs(decision-lens): 四個透鏡協定 references`

### T5 — SKILL.md（路由器，英文，frontmatter 帶中文觸發語）
- frontmatter：name=decision-lens、description（含「幫我決策」「該不該」「先打哪個」「投入多少」
  「決策分析」觸發語 + 邊界）、`allowed-tools: Read, Write, Edit, Bash`（Bash 跑計算腳本）。
- 本體：一句話問題判讀 → routing → 透鏡協定 → 腳本算數 → Markdown brief；輸出語言跟提問走、
  不瞎掰先驗、無 subprocess/網路/金鑰。
- 驗證：frontmatter 合法、與 references 連結一致。提交：`✨ feat(decision-lens): SKILL.md 路由器`

### T6 — evals/evals.json
- 案：①不確定型→Bayesian 且後驗正確（deterministic）②糾纏排序→Crux 點出主問題③「投入多少」
  →Kelly 給分數而非全 Kelly、負期望說不下注④輸出 Markdown 非簡體 HTML、不瞎掰先驗
  ⑤無 subprocess/外部工具。
- 驗證：`python3 -c 'import json;json.load(open("decision-lens/evals/evals.json"))'`。
  提交：`✅ test(decision-lens): evals 五案`

### T7 — attribution.md + sources.lock
- `references/attribution.md`：方法/協定改寫自 yao-bayesian/crux/kelly，數學為公開公式、零檔案收錄、
  Crux 去政治化、MIT。
- `sources.lock`：釘三源（取各自最新 commit 與日期，標 PRINCIPLES ONLY）。
- 驗證：JSON 合法、兩檔成對。提交：`📝 docs(decision-lens): attribution + sources.lock 釘 yao 三源`

### T8 — 登錄三處 + 全域 symlink
- `apm.yml` 加 `- ./decision-lens/`；README 自建表一列；`skill-curator/references/skill-map.md`
  新增條目（分析/決策類，附與 roleplay-coach/systematic-debugging/tutor 邊界）。
- `ln -s` 進 `~/.claude/skills/decision-lens`。
- 驗證：三處有記、symlink 存在。提交：`📝 chore(decision-lens): 登錄 apm.yml/README/skill-map + 全域 symlink`

### T9 — apm install + 收尾
- 跑 `apm install` 部署到專案範圍副本、更新 lock。提交 lock。

## 完成定義
九個任務全綠；三腳本數學正確（已知輸入→已知輸出）；無 subprocess/網路/金鑰；登錄齊全；
輸出為精簡 Markdown、語言跟提問走。

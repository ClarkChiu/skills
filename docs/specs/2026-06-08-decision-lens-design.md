# decision-lens — 設計文件

- 日期：2026-06-08
- 狀態：**已核准**（使用者拍板四點設計決定，2026-06-08）
- 參考來源：yaojingang/yao-open-skills 的決策簇（yao-bayesian-skill / yao-crux-skill /
  yao-kelly-skill）；取方法與協定結構，不收檔。研究見
  `research/audits/2026-06-08-yao-open-skills.md`。

## 1. 目的與範圍

**做什麼**：一個技能，讀進一個決策問題 → 自動選對「決策透鏡」→ 用真數學計算 →
輸出一份精簡 Markdown 決策摘要。三個透鏡：

| 訊號 | 透鏡 | 解什麼 |
|---|---|---|
| 不確定、要不要相信某假設、有證據要消化 | **Bayesian** | 先驗 → 概似比分級 → 後驗 → 行動門檻 → 敏感度 |
| 一堆糾纏問題、資源有限、不知先打哪個 | **Crux** | 主要／次要問題診斷 → 突破口 → 監測門檻 |
| 有優勢、要決定投入多少 | **Kelly** | 邊際 → 配置比例 → 分數 Kelly／上限 |

**不做什麼（範圍外）**：
- HTML/PDF 多格式匯出、報告排版（yao 的 subprocess + pandoc/weasyprint 管線一律不引入）。
- 簡體中文預設輸出。
- 取代 `roleplay-coach`（談判演練）或 `systematic-debugging`（除錯流程）——本技能是決策**判斷**，不是演練或除錯。

## 2. 已核准的四點決定

1. **Crux 去政治化**：拿掉「毛澤東矛盾論」品牌，只留分析方法——主要／次要問題，加
   決定性／牽引性／階段性三道判準，講成通用的優先級診斷。
2. **語言**：SKILL.md 與 `references/` 用**英文**（流程／工具技能，照本專案「語言看主題」
   房規，也利於 `skill-evolve` 比對上游）；**輸出語言跟著使用者的提問走**——中文提問就出
   臺灣繁體 brief，絕不簡體（這就是「去掉 CN 預設輸出」的落實）。
3. **數學是公開公式**（貝氏 odds 更新、Beta-Binomial 共軛、Kelly 準則皆不可著作權化）→
   原創重寫；只有「工作流／協定結構」算改寫自 yao。掛 MIT、零上游檔案收錄。
4. **技能名**：`decision-lens`。

## 3. 架構

```
decision-lens/
  SKILL.md                 # 路由器：分類問題 → 透鏡；呼叫對應 reference + script
  references/
    routing.md             # 分類決策樹：訊號 → 透鏡（含「需澄清／多重透鏡」分支）
    bayesian.md            # 證據更新協定：先驗衛生、概似比分級、後驗、行動門檻、敏感度
    crux.md                # 主／次問題優先級：三道判準、突破口、監測門檻（中性化）
    kelly.md               # Kelly 配置：邊際→比例、分數 Kelly、上限、誤用防呆
    attribution.md         # 改寫自 yao 三源（方法/協定，非檔）
  scripts/
    bayes_update.py        # 純計算器：odds 更新 + Beta-Binomial 共軛 → 印 JSON
    kelly_size.py          # 純計算器：Kelly f* + 對數成長極大化 + 分數 Kelly → 印 JSON
    crux_score.py          # 純計算器：主次問題的優先級評分 → 印 JSON
  evals/evals.json
  sources.lock             # 釘 yao-bayesian/crux/kelly 三源基準
```

**腳本設計原則**：純計算器——吃命令列／stdin 的結構化輸入，吐 JSON 數字，**不排版、不
匯出、不連網、不讀環境變數/金鑰**（如 yao 那三個計算腳本一樣乾淨）。模型負責把數字嵌進
Markdown brief。腳本只用 Python 標準函式庫（`math`、`json`、`argparse`），無第三方相依。

**路由器設計**：SKILL.md 先做一句話的「問題判讀」（這是什麼決策、賭注多大），再依
`routing.md` 的訊號選透鏡。允許「需澄清」（缺關鍵輸入時問一個問題）與「多重」（一個問題
跨兩個透鏡，例如先 Crux 定優先級再對主問題跑 Bayesian）。

## 4. 三個透鏡的數學核心（要實作的真東西）

- **bayes_update.py**：
  - odds 更新：`posterior_odds = prior_odds × Π(likelihood_ratio_i)`，
    `prior_odds = p/(1−p)`，`posterior_p = odds/(1+odds)`。
  - Beta-Binomial 共軛：`posterior_α = α + successes`、`posterior_β = β + failures`，
    回報後驗均值與可信區間端點。
  - 敏感度：對每個概似比給一個 `lr_power` 旋鈕，輸出後驗對證據強度的敏感度。
- **kelly_size.py**：
  - 二元 Kelly：`f* = (b·p − q) / b`（`b`=淨賠率、`p`=勝率、`q=1−p`）。
  - 多情境：在格點上極大化 `E[log(1 + f·r)]`。
  - 分數 Kelly（half/quarter）與單筆上限；負期望時回報「不下注」。
- **crux_score.py**：
  - 對每個候選問題評三道判準分數——決定性、牽引性、階段性（各 0–1 加權），
    輸出排序與主問題，附「為何是它」的分項分數。

## 5. 輸出：精簡 Markdown 決策摘要

依透鏡略有不同，但都是一份結構化 Markdown：
- **Bayesian**：問題 → 先驗（來源/假設標註）→ 證據表（每條的概似比與理由）→ 後驗 →
  行動門檻 → 敏感度 → 建議。
- **Crux**：問題群 → 候選矛盾 → 三判準評分表 → 主要問題 → 突破口 → 監測門檻。
- **Kelly**：機會 → 邊際輸入（勝率/賠率，標來源）→ 建議配置（分數 Kelly）→ 上限與前提 →
  反向風險。

模型不自己瞎掰先驗/勝率：缺的要嚮使用者問，或明確標為「假設」並做敏感度。

## 6. 與既有技能的邊界

| | 別的技能 | decision-lens |
|---|---|---|
| 演練一場對話 | `roleplay-coach` | 不演練，做決策判斷 |
| 找 bug 根因 | `systematic-debugging` | 不除錯，但 Bayesian 透鏡可診斷「哪個假設最被證據支持」 |
| 寫程式前的設計＋計畫 | `design-gate` | 非工程設計，是一般決策 |
| 教學/真懂一個主題 | `tutor` | 不教方法，直接套方法出決策 |

## 7. 撰寫語言

英文（工程／流程技能，照房規，同 design-gate／systematic-debugging）；description 帶中文
觸發語（「幫我決策」「該不該」「先打哪個」「投入多少」「決策分析」）。輸出語言跟提問走。

## 8. 登錄（建置後）

`apm.yml` 加 `- ./decision-lens/`、README 自建表一列、`skill-curator/references/skill-map.md`
（新群組或歸入分析類，附與既有技能邊界）、全域 symlink 進 `~/.claude/skills/`。

## 9. 成功標準（驗證用）

1. 不確定型問題 → 路由到 Bayesian，`bayes_update.py` 給出正確後驗（確定性可測：已知
   先驗+概似比 → 已知後驗）。
2. 糾纏排序問題 → 路由到 Crux，點出主要問題 + 突破口。
3. 「投入多少」型 → 路由到 Kelly，給分數 Kelly 而非全 Kelly；負期望時說「不下注」。
4. 輸出是 Markdown brief，不是簡體 HTML；模型不瞎掰先驗（要使用者給或標假設）。
5. 全程無 subprocess、無外部工具相依、無網路、無金鑰讀取。
6. 三個腳本各有單元測試，驗證數學正確（已知輸入 → 已知輸出）。

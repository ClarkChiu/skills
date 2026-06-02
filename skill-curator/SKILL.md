---
name: skill-curator
description: >-
  研究 Skill 大師 (external-skill research & decision orchestrator). Given an
  external agent skill — by name, GitHub/skills.sh URL, or a whole curated list —
  this runs the full evaluation pipeline and returns a verdict: 相關性 (does it
  help THIS user) → 重複性 (does it duplicate built-ins/existing skills) → 資安
  (delegates to skill-auditor) → 來源 (provenance) → 裁決 (直接裝 / 參考自製 /
  vendor / 跳過) → 記錄 (writes research/<date>-skill-research-log.md + audits/). USE THIS
  SKILL whenever the user wants to research, evaluate, vet, or decide on an external
  skill — phrases like 「研究這個 skill」「這個 skill 該不該裝」「評估一下」「值不值得裝」
  「幫我看看這個 skill」「install or build my own」, or pastes a list of recommended
  skills to assess. It ORCHESTRATES skill-finder (discovery) and skill-auditor
  (security) — it does not re-implement them. Discovery/decision only; never installs.
---

# skill-curator — 研究 Skill 大師

評估一個外部 skill「**該不該用、怎麼用**」並留下決策軌跡。你是策展者：問的不是
「這 skill 好不好」，而是「**對這個使用者的工作/生活有沒有用、裝它還是自己寫**」。

這個 skill 是**編排層**，明確**不重做**既有工具：

| 既有 skill | 角色 | 本 skill 怎麼用它 |
|---|---|---|
| `skill-finder` | 發現（skills.sh 唯讀） | 找 canonical 來源、抓 SKILL.md |
| `skill-auditor` | 資安裁決 | 取得 SAFE/⚠️/❌ 與安全執行計畫 |
| `skill-evolve` | 追自寫 skill 上游 | 自製/vendor 後把上游記入 attribution |

完整判準在 **`references/criteria.md`** —— 動手前先讀它，那是本 skill 的大腦。

## 出發點：以使用者定位為錨

先讀 **repo 根 `CLAUDE.md` 的「使用者定位」段**（可攜真相來源、跨機隨 git/APM 自動載入；
machine-local memory `user-profile` 只是本機快取，移機不依賴它）。評估一律從「對**這個人**
的情境有沒有用」出發，不是泛泛的好壞。沒有定位資訊時，先問使用者：主要工作是什麼、想用
skill 解決什麼。

## 五步流程

對每一個 skill 走一遍。多個 skill（或一條清單）就逐一跑、最後彙整成表。

```
[0] 相關性  → 對使用者情境（dev/系統/PM/寫作/研究/生活）有用嗎？無 → 標「跳過」、停。
[1] 重複性  → 重複內建或現有 skill 嗎？是 → 建議用既有/擴充自己的，而非新裝。
[2] 資安    → 跑 skill-auditor（靜態、不執行）。非 SAFE → 停或限沙箱。
[3] 來源    → 作者可信？有維護？或個人低星/單一 fork/repo 內兩份不一致/無 frontmatter？
[4] 裁決    → 用 references/criteria.md 的判準表：直接裝 / 參考自製 / vendor＋客製 / 跳過。
[5] 記錄    → 本機詳細（gitignored）：research/audits/<date>-<skill>.md ＋ 當日工作日誌；
              公開：research/skill-index.md 補中性一列（日期/skill/url/作者/重複/裁決）。
```

### 步驟細節

- **[0]+[1] 先做，便宜**：先用既有知識與 `skill-finder` 抓描述，判相關性與重複性。
  不相關或純重複的，不必勞動完整稽核——標掉、說明理由即可（省 token）。
- **[2] 資安交給 skill-auditor**：不要在這裡重寫稽核邏輯。把 auditor 的 SKILL AUDIT
  REPORT 原樣收進 `audits/`。auditor 說非 SAFE，本 skill 的裁決不得蓋過它。
- **[3] 來源訊號**：星數無 API auth 會誤讀/灌水 → 標「未驗證」，別當事實。高星 + 少
  commit + 短歷史 = SEO-sprint 樣式，低信任。
- **[4] 裁決**：見 `references/criteria.md`。一句心法——**能下載的工程就裝，能寫的文字
  就自己寫成你要的樣子**。
- **[5] 記錄**：研究 ≠ 安裝。每個評估都留軌跡，避免重複研究、讓裝/不裝可追溯。

## 多來源清單的處理

使用者常貼一條第三方推薦清單。注意：

- **一條列 ≠ 一個 skill**（`minimax-docx、pdf、xlsx` 一行其實 3 個）→ 展開再算數量。
- **清單來源信任度低**：會把不同作者、不同品質的 skill 湊一起。
- **同名不同物**：對 canonical repo 交叉比對，別信 listing 的配對。
- 平行研究多個時，可派子代理分頭蒐證（抓檔 + 位元掃描），**裁決自己下**。

## 輸出格式

研究單一 skill → 一份 SKILL AUDIT REPORT（auditor 格式）＋ 一段裁決與理由。
研究一份清單 → 先逐項，最後一張彙整表：

```
| Skill | 相關 | 重複內建? | 資安 | 來源 | 裁決 | 一句理由 |
```

裁決四選一：**🟩 直接裝** / **🟦 參考自製** / **🟨 vendor＋客製** / **🟥 跳過**。
每個都要附「為什麼是這個裁決」（扣回 criteria 的訊號）。

## 落地動作

記錄分兩層（research/ 除 `skill-index.md` 外都 gitignored、不進公開 repo）：
- **本機詳細（不公開）**：每個深審過的寫 `research/audits/YYYY-MM-DD-<skill>.md`（完整 SKILL
  AUDIT REPORT）＋**當日**工作日誌 `research/<YYYY-MM-DD>-skill-research-log.md`（理由、第三方
  資安細節、措辭都留這裡）。新的一天開新檔。
- **公開索引**：把一列**中性**摘要同步到 `research/skill-index.md`（committed）——只放 日期／
  skill／url／作者／重複內建?／裁決，**不放**資安細節、漏洞揭露、對第三方的評語。理由是公開
  repo 不該點名批評別人的 skill；裁決寫成「對本專案的適配決定」，非品質評斷。
- 裁決「直接裝」→ 提醒：pin commit、**裝後複審本機版本**（v1.0 安全 ≠ 你抓的那版）。
- 裁決「參考自製/vendor」→ 可接著用 `skill-creator` 起草，並把上游記入新 skill 的
  `references/attribution.md`（之後 `skill-evolve` 會追）。

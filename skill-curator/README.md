# skill-curator — 研究 Skill 大師

評估外部 agent skill「**該不該用、怎麼用**」並留下決策軌跡的編排型 skill。

一句話：丟一個 skill（名稱／URL／一整份推薦清單）→ 跑完整評估 → 給裁決
（🟩 直接裝 / 🟦 參考自製 / 🟨 收錄＋客製 / 🟥 跳過）＋ 寫進 `research/` 決策日誌。

## 定位（不重造輪子）

| Skill | 角色 |
|---|---|
| `skill-finder` | 發現（skills.sh 唯讀） |
| `skill-auditor` | 資安裁決 |
| **`skill-curator`** | **相關性 + 裝/自製決策 + 記錄**（呼叫上面兩個） |
| `skill-evolve` | 追自寫 skill 的上游 |

## 五步流程

`相關性 → 重複性 → 資安(skill-auditor) → 來源 → 裁決 → 記錄`

完整判準與心法見 [`references/criteria.md`](./references/criteria.md)——那是這個 skill 的大腦。
心法：**能下載的工程就裝，能寫的文字就自己寫成你要的樣子。**

## 產出

- `research/<YYYY-MM-DD>-skill-research-log.md` — 當日工作日誌，每個評估一列（日期/名稱/URL/作者/重複/資安/裁決）。
- `research/audits/YYYY-MM-DD-<skill>.md` — 完整 SKILL AUDIT REPORT。

## 注意

- **發現與決策，不安裝**。研究 ≠ 安裝。
- 資安裁決一律以 `skill-auditor` 為準，本 skill 不得蓋過。
- 裁決「直接裝」→ pin commit、裝後複審本機版本。
- 需本機可上網（抓 SKILL.md 做靜態分析）。

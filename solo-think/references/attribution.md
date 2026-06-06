# 來源與授權 (Attribution)

## 改寫自

**loryoncloud/Heartbeat-Like-A-Man**（MIT 授權）
- 儲存庫：https://github.com/loryoncloud/Heartbeat-Like-A-Man
- 原作是 OpenClaw 專用的 cron 包：讓代理在使用者離線時「沒事找事」，含微觸發管理、做夢思考、思考佇列、自主探索、社群巡邏。

## 取了什麼

只取**對內**那半的構想：做夢式反思、思考佇列（累積待想的問題、之後接續咀嚼）、把想法寫進記憶。

## 改了什麼

- **整段砍掉對外動作**：原作的「自主對外探索」與「社群巡邏（自動參與社群討論）」全部移除。solo-think 只對內、不對外動作、不通知、不呼叫網路。經使用者明確決定（2026-06-06）。
- **平臺改寫**：從 OpenClaw（`~/.openclaw/`、`openclaw cron add`）移植到 **Hermes Agent**（`~/.hermes/`、`hermes heartbeat create`）。改用 Hermes 的 heartbeat 原語，並以 `--toolsets file` 在工具面結構性強制「只對內」。
- **成本與時段控制**：觸發節奏交給 Hermes heartbeat 頻率（不靠它自己估算用量），加一個自足的時段限制 `active_hours`，並用 `focus` 錨定反思方向。把頻率壓低是為了不跟使用者互動時搶速率額度。原作的「閒置才動」對只對內的反思沒有意義（反思本來就不打擾），而且它得先取得「使用者當前是否在線上」這個資訊，但系統裡沒有任何元件負責提供，故移除。
- **語言改寫**：原作核心是簡體中文，全部改寫成清楚的臺灣繁體中文。
- 原作沒有 SKILL.md（是 cron payload + config）；本技能補上 agentskills.io 開放標準的 SKILL.md、evals 與設定範本。

## 授權

原作 MIT，可自由改寫。本技能沿用 MIT。

`sources.lock` 釘住上游基準，供 `skill-evolve` 日後比對更新。

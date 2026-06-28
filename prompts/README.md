# prompts/ — 存起來的薄提示（非技能）

這裡放**輕量、可複製貼上的提示**：價值是純文字、不值得做成完整技能（無 `SKILL.md`／`evals`），
但值得固化、隨 git／APM **跨機帶著走**。和技能的差別：技能是觸發式、有 frontmatter、會被 APM
部署；這些只是存起來的提示，手動貼或由內建 `schedule` 週期跑。

> 為什麼不放 `~/.claude/`：那是機器本地、不隨 git 走，換機器就遺失。放這裡才可攜。

## 目錄

| 提示 | 軸 | 用途 | 預定排程 |
|---|---|---|---|
| [`claude-md-audit.md`](./claude-md-audit.md) | 規則衛生 | 揪出可刪規則／衝突／冗餘／模糊指令，只回報待核可 | 每週一 09:00 |
| [`claude-md-context-budget.md`](./claude-md-context-budget.md) | 載入成本／結構 | 量化 CLAUDE.md 臃腫，標出該移到 path-scoped rules／子目錄／skill 的部分 | 每月／按需 |

## 接 schedule（這份 index 的重點：知道哪些提示要掛排程、怎麼掛）

排程是 Claude Code／Cowork **內建**能力（網頁版不支援，需改手動）。設定時，把提示檔的內容當任務
內容，並**務必加「只輸出報告、不修改任何檔案」**。範例接線（用內建 `schedule`／`/loop` 或對話直接
要求建立週期任務）：

**claude-md-audit（每週一 09:00）：**
```
建立一個名為「claude-md-audit」的每週排程任務，每週一早上 9 點執行。
任務內容：讀取並執行 repo 中 prompts/claude-md-audit.md 的提示——完整讀我的 CLAUDE.md／全域設定／
所有 skill／context，照該檔的 7 條判準審查，輸出建議刪除清單＋衝突清單＋健康摘要。
不要修改任何檔案，僅輸出報告。
```

**claude-md-context-budget（每月一次或按需）：**
```
建立一個名為「claude-md-context-budget」的每月排程任務。
任務內容：讀取並執行 repo 中 prompts/claude-md-context-budget.md 的提示——量化 CLAUDE.md 載入成本、
標出該移到 path-scoped rules／子目錄／skill 的部分。不要修改任何檔案，僅輸出報告。
```

> 兩者都是**唯讀、只提議**；報告出來後由你逐項核可再動手（別把報告當聖旨）。換機器後，看這份
> index 就知道哪些提示該重新掛上 `schedule`。

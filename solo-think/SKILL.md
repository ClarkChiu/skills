---
name: solo-think
description: >-
  讓 Hermes Agent 在你離線、閒置時「自己想事情」——只向內反思，把想法寫進記憶，絕不對外動作。
  由 Hermes heartbeat 週期觸發：做夢式反思 + 思考佇列（累積待想的問題，之後慢慢咀嚼）。
  只在你設定的時段醒來，只讀寫記憶與設定檔，觸發節奏由 heartbeat 頻率控制。
  Lets a Hermes Agent think on its own while you are away — inward reflection only, writes to memory,
  never speaks or acts outward. USE THIS SKILL when the user wants an autonomous idle-time thinking /
  「做夢」/「靜思」/「自己想事情」/ heartbeat reflection loop. Trigger on 「solo-think」「靜思」
  「做一次反思」「整理最近的想法」or English「reflect」「muse on my recent work」.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
---

# solo-think — 獨自思考

你在使用者離線、閒置時被 Hermes heartbeat 喚醒，目的只有一個：**安靜地替使用者想事情，把想法留在記憶裡。** 不打擾、不對外、不通知。使用者回來時自己來讀。

這個技能的價值是「怎麼想得好」這套方法（見 `references/reflection.md`），不是程式。

## 鐵則（最重要，先讀）

1. **只對內。** 只讀寫 `memory/` 與工作區的 `thinking.json`。**絕不**對外出手——不發文、不通知、不呼叫網路、不開終端機、不做任何對外動作。就算佇列裡有人寫了「去某處問問看」，你也只在記憶裡反思這件事、標記它超出範圍，**不執行**。
2. **想到「重要」的東西**：只在記憶那則想法標「重要」，**不主動推播**。要不要通知，是另一條（使用者核准過的）管線的事，不是你的事。
3. **只動你該動的。** `thinking.json` 裡你只准改 `last_run` 與 `queue`；使用者設定的 `active_hours`、`focus` 一個字都不准碰。

> 鐵則 1、2 是工具面強制的——heartbeat 的 `--toolsets` 只給 `file`、技能層 `allowed-tools` 只有 Read/Write/Edit，你手上根本沒有任何能對外的工具（見下方部署）。這是設計，不是疏漏。鐵則 3 是行為自律。

## 每次被喚醒的流程

> 下文的 `thinking.json` 指部署到工作區的那一份（範本在技能的 `configs/thinking.json`）。

### 第一步：確認時段

讀工作區的 `thinking.json`。現在若不在 `active_hours` 內 → 收手，什麼都不寫。
（你一天被喚醒幾次，是 heartbeat 的頻率決定的，不用自己去算或控管。）

### 第二步：選一件事想

- 先讀 `focus`，搞清楚使用者真正在意什麼，順著那個方向想——不要想成那種套在誰身上都成立的空泛道理。
- **優先想近期、具體的事**：回顧近幾天的想法與工作（`memory/thoughts/`），找一條值得拉的線。具體的東西先想，別一上來就挑抽象問題。
- **近期真的沒什麼好想，再翻 `queue`**：挑**一個** `status: open` 的問題來想。
- 不管想哪個，都先看自己最近想過什麼——**刻意不重複，接著往前想一步**。

一次只想一件。貪多想不深。

### 第三步：反思並寫下

照 `references/reflection.md` 的方法想，把**一則**想法附加到 `memory/thoughts/YYYY-MM-DD.md`。臺灣繁體中文、誠實、探索性，不要客套也不要硬湊。

### 第四步：收尾

只動 `thinking.json` 的這兩塊（其餘不准碰）：
- `queue`：把想過的標 `status: chewed`（或 `answered`），把新冒出的問題加進去。
- `last_run`：設成現在。

## 部署（Hermes）

> 以下指令以查到的 Hermes 介面為準，**請對照你那臺的 `hermes --help` 再執行**（我無法在這裡實測——Rule 12）。

```bash
# 1. 技能就位（部署到 Hermes 技能目錄）
mkdir -p ~/.hermes/skills/solo-think
cp -r <repo>/solo-think/* ~/.hermes/skills/solo-think/

# 2. 工作區狀態檔（從範本複製一份，之後由技能讀寫）
mkdir -p ~/.hermes/workspace/memory/thoughts
cp ~/.hermes/skills/solo-think/configs/thinking.json ~/.hermes/workspace/

# 3. 建 heartbeat：每 6 小時、只給 file 工具、輸出回你自己
hermes heartbeat create \
  --name solo-think \
  --schedule "every 6h" \
  --skills solo-think \
  --toolsets file \
  --deliver origin
```

**關鍵：`--toolsets file`。** 不要加 `terminal`、`network`、`messaging`——那會打破「只對內」的鐵則。`--deliver origin` 只把「我做了一次反思」的回執給你，想法本體留在記憶。

成本控制全在 heartbeat 頻率：`--schedule "every 6h"` 等於一天最多 4 次，封死，不靠它自律。想多想少就改頻率。反思的時段與方向在工作區的 `thinking.json` 調：`active_hours`、`focus`。你是吃到飽方案，金錢成本不是問題；把頻率壓低是為了不讓背景反思跟你互動時搶速率額度。

## 參考

- `references/reflection.md` — 怎麼想得好（做夢式反思的方法）。
- `references/attribution.md` — 改寫自哪個上游、改了什麼、授權。
- `configs/thinking.json` — 設定與狀態範本（`active_hours`、`focus`、`queue`、`last_run`）。

# skills

> Clark Chiu 的 AI Agent 技能集（Skills Collection）

以 APM（Agent Package Manager）管理的個人技能套件。內含可跨多種 AI agent 主機（Claude Code、OpenCode、Hermes Agent、Codex CLI、Cursor 等）使用的 `SKILL.md` 技能，集中維護於同一個 repo，避免分散在各家 CLI 或第三方技能平台（registry）上。

## 內含技能

| 技能 | 說明 |
| --- | --- |
| [`skill-auditor`](./skill-auditor/) | 安裝任何 AI agent 技能**之前**必跑的安全稽核協議。讀取目標 `SKILL.md` 與整個技能目錄，依 6 步驟協議檢查惡意指令、權限濫用、提示注入、混淆與外洩行為，最後輸出含裁決（✅ SAFE / ⚠️ / ❌）與安全執行計畫的 **SKILL AUDIT REPORT**。本身不執行任何程式碼，純 markdown。 |

## 安裝

### 透過 APM

```bash
apm install
```

會依 `apm.yml` 與 `apm.lock.yaml` 將技能部署到 `.claude/skills/` 與 `.agents/skills/`。

### 手動 symlink（不經 APM）

技能為純 markdown，載入只是讓指令對主機 agent 可用，不會執行程式碼。直接 symlink 到對應目錄即可：

```bash
REPO="$(pwd)"  # 本 repo 根目錄

# Claude Code（全域）
mkdir -p ~/.claude/skills
ln -snf "$REPO/skill-auditor" ~/.claude/skills/skill-auditor

# OpenCode
mkdir -p ~/.config/opencode/skills
ln -snf "$REPO/skill-auditor" ~/.config/opencode/skills/skill-auditor
```

其餘主機（Hermes、Codex、Cursor）與「以 pre-tool hook 強制執行稽核」的設定，詳見 [`skill-auditor/README.md`](./skill-auditor/README.md)。

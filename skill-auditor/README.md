# skill-auditor

A self-maintained security audit skill, kept in dotfiles so it can be symlinked
into any host agent's skills directory without going through a third-party
CLI or registry. Runs on Claude Code, Hermes Agent, OpenCode, Codex CLI,
Cursor, and anything else that reads SKILL.md.

## Provenance

Hand-merged from the sources below. Every line was re-read; nothing is a
transitive dependency. Each section inside `SKILL.md` carries an inline
`<!-- source tag -->` showing which upstream it came from.

**Upstream skills:**

- **[A]** `sundial-org/awesome-openclaw-skills/skills/skill-vetter` — broadest
  red-flag list
  https://github.com/sundial-org/awesome-openclaw-skills/tree/main/skills/skill-vetter
- **[B]** `UseAI-pro/openclaw-skills-security/skills/skill-vetter` — structured
  permission table, frontmatter format
  https://github.com/UseAI-pro/openclaw-skills-security/blob/main/skills/skill-vetter/SKILL.md
- **[C]** `UseAI-pro/openclaw-skills-security/skills/skill-auditor` — 6-step
  protocol, zero-width character detection, named exfiltration patterns,
  SAFE-RUN PLAN output
  https://github.com/UseAI-pro/openclaw-skills-security/blob/main/skills/skill-auditor/SKILL.md

**Research reports (empirical data, IOCs, bypass techniques):**

- **[D]** Snyk ToxicSkills (Feb 2026) — 3,984 skills scanned, 36.82% flawed;
  candid disclosure of pattern-matcher limits
  - https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/
  - https://labs.snyk.io/experiments/skill-scan/
- **[E]** OWASP Agentic Skills Top 10 — AST01 Malicious Skills
  https://owasp.org/www-project-agentic-skills-top-10/ast01
- **[F]** dev.to (Apr 2026) — observed obfuscation bypass techniques
  (`c${u}rl`, etc.) and reputable-publisher list
  https://dev.to/harivenkatakrishnakotha/your-claude-code-skills-might-be-stealing-your-credentials-right-now-2d0h
- **[G]** Cato Networks (Mar 2026) — Weaponizing Claude Skills with
  MedusaLocker: "additional operations may run under a single approval"
  https://www.catonetworks.com/blog/cato-ctrl-weaponizing-claude-skills-with-medusalocker/
- **[H]** Agensi (Mar 2026) — ToxicSkills + ClawHavoc summary:
  1,184 malicious skills sharing C2 IP `91.92.242.30`
  https://www.agensi.io/learn/toxicskills-clawhavoc-agent-skills-security-crisis-2026

**Evaluated but not integrated:**

- `trailofbits/skills` (5.3k stars, the largest security-skill collection) —
  Scope doesn't overlap. Their `agentic-actions-auditor` audits GitHub
  Actions workflow YAML for AI-agent integration risks (CI/CD scenarios),
  not SKILL.md content itself.
  https://github.com/trailofbits/skills

> Re-diff against upstream periodically. Don't auto-sync — keeping this in
> dotfiles is the whole point of staying in the loop.

## Installation (symlink into host agents)

The skill is plain markdown. Loading it just makes its instructions available
to a host agent — it runs no code. Symlink wherever needed:

```bash
DOTFILES="$HOME/dotfiles"  # adjust to your dotfiles root

# Claude Code (global)
mkdir -p ~/.claude/skills
ln -snf "$DOTFILES/skills/skill-auditor" ~/.claude/skills/skill-auditor

# Claude Code (per-project)
mkdir -p .claude/skills
ln -snf "$DOTFILES/skills/skill-auditor" .claude/skills/skill-auditor

# Hermes Agent
mkdir -p ~/.hermes/skills
ln -snf "$DOTFILES/skills/skill-auditor" ~/.hermes/skills/skill-auditor

# OpenCode
mkdir -p ~/.config/opencode/skills
ln -snf "$DOTFILES/skills/skill-auditor" ~/.config/opencode/skills/skill-auditor

# Codex CLI
mkdir -p ~/.codex/skills
ln -snf "$DOTFILES/skills/skill-auditor" ~/.codex/skills/skill-auditor

# Cursor (per-project)
mkdir -p .cursor/skills
ln -snf "$DOTFILES/skills/skill-auditor" .cursor/skills/skill-auditor
```

## Making it enforce, not just exist

SKILL.md is read by the model — it's a request, not a guarantee. To force
this audit to run before any install action, pair it with a deterministic
pre-tool hook in your host agent. The skill provides policy; the hook
provides enforcement.

### Claude Code (`~/.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$HOME/dotfiles/hooks/audit-skill-install.sh" }
        ]
      }
    ]
  }
}
```

### Hermes Agent (`~/.hermes/config.yaml`)

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "~/dotfiles/hooks/audit-skill-install.sh"
      timeout: 10
```

### Shared hook script (`~/dotfiles/hooks/audit-skill-install.sh`)

```bash
#!/usr/bin/env bash
# Intercept skill-install commands and force the model to run skill-auditor first.
# Compatible with the shell-hook JSON wire protocols of both Claude Code and Hermes Agent.
set -euo pipefail
payload="$(cat -)"
cmd=$(printf '%s' "$payload" | jq -r '.tool_input.command // .params.command // empty')

case "$cmd" in
  *"npx skills add"*|*"npx sundial-hub add"*|*"npx clawhub add"*|\
  *"hermes skills install"*|*"claude skills install"*|\
  *"git clone "*skills*|\
  *"cp "*/.claude/skills/*|*"cp "*/.hermes/skills/*|\
  *"cp "*/.codex/skills/*|\
  *"ln -s"*"/.claude/skills/"*|*"ln -s"*"/.hermes/skills/"*|\
  *"ln -s"*"/.codex/skills/"*)
    jq -nc --arg cmd "$cmd" '{
      decision: "block",
      reason: ("Skill installation detected: " + $cmd +
               "\n\nYou MUST invoke the skill-auditor skill on the source BEFORE installing. " +
               "Read the target SKILL.md and every other file in the skill directory, " +
               "walk Step 0 + all 6 steps, and produce a SKILL AUDIT REPORT. " +
               "Only re-issue this install command if the verdict is ✅ SAFE.")
    }'
    ;;
  *)
    printf '{}\n'
    ;;
esac
```

Don't forget `chmod +x ~/dotfiles/hooks/audit-skill-install.sh`.

## Update policy

Periodically diff upstream (especially Snyk, OWASP, Trail of Bits) and
hand-merge any new IOCs or attack patterns. **No auto-sync** — keeping this
file in dotfiles is what keeps you in the loop.

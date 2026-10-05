# Attribution

## Adapted from

Three prompt templates out of a 20-prompt productivity roundup:

- Original: a public X (Twitter) thread by **@AnatoliKopadze** — "20 Claude prompts"
  (no stable per-prompt URL captured; thread surfaced via the translation below).
- Translation read during evaluation: BlockTempo,
  《這 20 個提示詞教你深度使用 Claude》
  https://www.blocktempo.com/20-claude-prompts-productivity/

Taken: **#9 Salary Negotiation Roleplay**, **#10 Interview Simulator**, and
**#12 Difficult Conversation Prep**. What earns these a skill is not the personas but
the **structure that survives contact with a capable model's bad habits**: realistic
objection lists, one-turn-at-a-time discipline (models love to simulate both sides),
the honesty gate on unrealistic goals, and a mandatory debrief that names what the
user left on the table.

## What changed

- **Merged three prompts into one skill** with a shared hard-rule core (one turn at a
  time, realistic resistance, honesty gate, mandatory debrief, sayable words) and
  thin per-scenario sections — the originals repeat most of this per template.
- **#12 restructured as playbook-first, rehearsal-second.** The original is pure prep
  (no roleplay); this version delivers the four-part playbook, then offers to rehearse
  it against a deliberately non-reasonable counterpart — prep and practice belong
  together.
- **Promoted "if my goal is unrealistic, tell me before I walk in"** from a buried
  rule in #12 to a shared hard rule for all scenarios — it matters most in
  negotiation, where the original lacks it.
- **Added a language rule**: rehearse in the language the real conversation will
  happen in (for this user, usually Taiwan Mandarin).
- **Debrief unified** across scenarios, with "what you left on the table" as the
  centerpiece — the one thing a real counterpart will never tell you.
- Dropped the fill-in-the-blank forms in favor of intake checklists that skip
  anything already given. Added evals and this attribution. Of the remaining 17
  prompts, two (#18/#20) became the sibling skill `tutor` and fifteen were skipped —
  verdict in `research/skill-index.md`.

## Later addition — goutoujunshi (狗頭軍師), MIT since 2026-08-17 (was PolyForm Noncommercial 1.0.0)

Added 2026-08-05: the **one-move-per-line** rule and the **three-branch follow-up**
(positive / non-committal / refusal), both reimplemented from scratch.

- Repo: https://github.com/powerycy/goutoujunshi (a Chinese-language relationship
  advisor — the domain is irrelevant; two of its conversation disciplines are not).
- Its 話術編排器 makes the speaker pick exactly one move per turn from a fixed set,
  on the grounds that a line which comforts, flirts, invites, and asks for an
  explanation at once loses its point — and it pre-writes what to do for each of three
  replies. That is the same failure this skill sees in rehearsals: a coached line doing
  three jobs, and a user with no plan for "let me check with the team."
- **Ours is a re-expression for high-stakes professional conversations**: a seven-move
  table (anchor / hold / probe / concede / reframe / close / exit) retargeted from
  upstream's seven relationship moves, and a branch taxonomy tied to the
  negotiation-specific distinction between a no-to-this-ask and a no-to-the-whole-thing.
  Be honest about what carried over: the *structure* is the same shape — seven moves,
  pick one per turn, three branches — and one entry (`close` ≈ upstream's 收線) is a
  direct counterpart. The move set is otherwise ours and the domain is different, but
  "shares no entries" would overstate it.
- **No upstream text enters the skill itself.** At adoption the license was non-commercial
  and this repo is publicly redistributed via APM, so that was a hard restriction; upstream
  switched to MIT on 2026-08-17 (commit 8d30c86), and the method-only rewrite stands for
  the audit's other reasons (context and maintenance). The short paraphrase above is confined to this
  attribution file, where recording what was adopted is the point. Methods are not
  copyrightable; its prose is. Evaluation: `research/audits/2026-08-05-goutoujunshi.md`.

## License

Two upstreams, two situations:

- **The 20-prompt roundup** (prompts #9/#10/#12) — a public article/thread with no stated
  license (NOASSERTION). Nothing is copied verbatim; mock interviews, negotiation
  rehearsal, and conversation prep are generic coaching practice.
- **powerycy/goutoujunshi** (the one-move-per-line rule and the branch tree, added
  2026-08-05) — **MIT since 2026-08-17**; the version adopted from was **PolyForm
  Noncommercial 1.0.0**. Ideas only; no upstream text in the skill itself — see the
  section above for why that still holds after the license change.

This skill is MIT. `sources.lock` pins **both** upstream baselines for `skill-evolve`.

## Coupling with `relationship-counsel` (change one, check the other)

The same two disciplines from goutoujunshi also went into the self-built
`relationship-counsel` (Chinese, romantic situations). The two are **the same structure
used twice** — seven moves, pick one per turn, plus a three-branch follow-up — with
disjoint move sets:

| | here (English, professional) | `relationship-counsel` (Chinese, romantic) |
|---|---|---|
| Moves | anchor / hold / probe / concede / reframe / close / exit | 回應／讓路／拋接／邀約／問一件事／表明／收手 |
| Axis | what this line is doing in a negotiation | what this message asks the other person to do |

The reason for two copies is not that they are unrelated — it is that cross-language
cross-referencing would make both unreadable. **The maintenance cost is real: when you
change the one-move-per-line rule or the branch taxonomy here, go look at whether
`relationship-counsel` needs the same change.** The same note is in that skill's
attribution file.

Division of labour: `relationship-counsel` reads the situation and drafts **one**
message; this skill **rehearses** a whole exchange turn by turn. Romantic rehearsal is
in scope here (see the romantic intake branch); romantic *analysis* is not.

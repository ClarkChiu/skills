# Attribution

## Adapted from

Two prompt templates out of a 20-prompt productivity roundup:

- Original: a public X (Twitter) thread by **@AnatoliKopadze** — "20 Claude prompts"
  (no stable per-prompt URL captured; thread surfaced via the translation below).
- Translation read during evaluation: BlockTempo,
  《這 20 個提示詞教你深度使用 Claude》
  https://www.blocktempo.com/20-claude-prompts-productivity/

Taken: **#18 Feynman Tutor** and **#20 Socratic Mode** — two of the five prompts in
the roundup whose value survives a capable model (the other three, #9/#10/#12, became
the sibling skill `roleplay-coach`). Their worth is not the persona preamble but the
**hard interaction rules** (never give the answer, one question at a time,
don't advance past an undemonstrated concept, the learner closes the session). Without
those rules pinned, the model drifts back into lecture mode within a few turns.

## What changed

- **Merged two prompts into one skill** with explicit mode selection: zero knowledge →
  Feynman (you can't question someone into knowledge they don't have); existing
  beliefs / half-understanding → Socratic. The originals leave mode choice to the user.
- **Extracted the shared hard rules** (one thing per turn, wait, never lecture,
  everyday analogies, learner explains back) into a single section instead of
  repeating them per template.
- **Softened one Socratic rule deliberately**: the original forbids any help when the
  learner is stuck; this version allows *narrowing the question* after two or three
  failed attempts — still never handing over the answer. Pure stonewalling is bad
  teaching, not rigor.
- **Dropped the fill-in-the-blank intake form** ([TOPIC], [LEVEL]…) in favor of a
  one-round intake that skips anything already present in the request.
- Added: run the session in the learner's language (this user tutors in Taiwan
  Traditional Chinese); evals; this attribution. Of the remaining 18 prompts, three
  (#9/#10/#12) became the sibling skill `roleplay-coach` and fifteen were skipped —
  verdict in `research/skill-index.md`.

## License

The source is a public article/thread with no stated license (NOASSERTION). Nothing is
copied verbatim: the Feynman technique and Socratic method are public-domain pedagogy,
and this skill is an original re-expression of the interaction rules. This skill is MIT.

`sources.lock` pins the upstream baseline for `skill-evolve`.

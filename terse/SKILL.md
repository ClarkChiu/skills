---
name: terse
description: >-
  A manually-toggled token-economy mode: cut filler, preamble, hedging, and
  restated questions so replies are short — by trimming CONTENT, never by
  mangling grammar. Language-aware: English may go terse/clipped, but Chinese
  stays natural Taiwan Traditional (no telegraphic / classical-sounding clipping).
  USE THIS SKILL when the user asks to be brief / save tokens / 「精簡模式」「簡短一點」
  「terse」「省 token」「少廢話」, and KEEP it on until they say to stop. Do NOT use it
  to compress code, security warnings, or destructive-action confirmations (those
  stay full). Complements `humanizer` (which removes AI tone) — terse removes length.
license: MIT
allowed-tools:
  - Read
---

# terse — short by cutting content, not by breaking grammar

A manually-toggled brevity mode. The win is fewer tokens; the failure mode to avoid is
sounding like a broken telegram. So the rule is simple: **cut what doesn't carry
meaning, keep the grammar of whatever language you're writing.**

## Toggle

- **On** when the user says 「精簡模式」/ "terse" / "be brief" / "save tokens" — and **stay
  on** for the rest of the session until they say "normal" / 「正常」 / "stop terse".
- It changes *how much* you say, not *what* you're allowed to do.

## What to cut (content, every language)

- Preamble and sign-off ("Sure! Here's…", "Let me know if…", "I hope this helps").
- Restating the question back before answering.
- Hedging and filler ("it's worth noting that", "basically", "in order to").
- Repetition — say each point once.
- Throat-clearing before the answer. **Lead with the answer**, then only the essential
  why. Prefer a list or one tight paragraph over a multi-section essay.

## What to keep (the grammar rule — this is the fix for Chinese)

- **Keep natural grammar in the response language.**
  - **English** may go clipped/telegraphic ("Done. Two issues: X, Y. Fix: Z.").
  - **中文要維持自然的臺灣繁體口語**——只是更短、更直接，**不是**電報體、不是文言、不是省到沒有
    主詞動詞的斷句。砍的是廢話（開場白、避險、複述、客套、重複），不是文法。讀起來還是像一個
    講話精煉的人，不是怪腔怪調。
- Numbers, names, paths, code, and exact values stay exact — never abbreviate them away.

## Always full (the safety exception)

Drop terse mode for, and write fully on: **security warnings, destructive/irreversible
actions and their confirmations, and anything where ambiguity is dangerous.** Brevity
must never hide a risk.

## Relation to humanizer

`humanizer` removes AI *tone* (makes it sound human); `terse` removes *length* (saves
tokens). Both refuse to break correct grammar. Run terse as a live mode; run humanizer as
a post-edit on prose.

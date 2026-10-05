# Crux lens — find the primary problem to break first

For "where do I start?" decisions with several interlocking problems and limited
resources. Identify the **primary problem** (the one whose resolution most unblocks the
rest) vs the secondary ones, and pick a breakthrough action.

> This is a general prioritization method — primary vs secondary problems, scored on three
> tests. No ideology attached; it is just "which lever moves the most, that we can actually
> pull, now."

## Protocol

1. **List the candidate problems** as concrete tensions, e.g. "flaky CI blocks every merge"
   rather than "quality". Aim for 3–6 candidates.
2. **Score each on three tests** (0..1):
   - **decisiveness** — how much solving it unblocks or resolves the others.
   - **leverage** — how much your *available* resources actually move it (a huge problem
     you can't touch this quarter scores low).
   - **stage** — whether now is the right stage to act on it (some problems must wait for a
     precondition).
3. **Rank.** Call the script (weights default to decisiveness 0.5 / leverage 0.3 / stage 0.2;
   override if the situation justifies it):
   ```bash
   python3 scripts/crux_score.py --json '{"problems":[
     {"name":"flaky CI","decisiveness":0.9,"leverage":0.7,"stage":0.8},
     {"name":"docs debt","decisiveness":0.3,"leverage":0.6,"stage":0.4}]}'
   ```
4. **Name the primary problem** (top score) and the **breakthrough action** — the single
   move that most shifts it.
5. **Grade the scores** (A/B/C/D per `SKILL.md`) as you assign them — most are C (informed
   impression) unless measured; an assumed score is **D**, which *is* the assumption label.
6. **Close with the exit rule** — watch window, stop condition, tripwire (`SKILL.md`).
   This replaces the older "monitoring thresholds" wording; same intent, but the stop
   condition is the part that was missing. "Re-evaluate when" tells you to look again;
   a **stop condition** tells you that you picked the wrong crux and should re-rank.
   Priorities are not permanent, and neither is the diagnosis that produced them.

## Brief structure

```
## Priority — <situation>
- **Read:** priority decision, stake <…>
- **Candidates & scores:**
  | problem | decisiveness | leverage | stage | grade | score |
  |---|---|---|---|---|---|
- **Primary problem:** <name>  (why: the scores)
- **Breakthrough action:** <the one move>
- **Secondary (hold for now):** <…>
- **Fragility:** <does the ranking survive the C and D scores moving? cheapest measurement:>
- **Watch window:** <date or event when this gets re-ranked>
- **Stop condition:** <what would mean the primary problem was the wrong crux>
- **Tripwire:** <the one signal worth interrupting for early>
```

Scores are usually C-grade (informed impression) unless measured — grade them honestly;
a ranking built on four C's that flips under small changes is a ranking that has not
decided anything.

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
5. **Monitoring thresholds.** State what signal would mean the primary problem has changed
   (so the priority should be re-evaluated) — priorities are not permanent.

## Brief structure

```
## Priority — <situation>
- **Read:** priority decision, stake <…>
- **Candidates & scores:**
  | problem | decisiveness | leverage | stage | score |
  |---|---|---|---|---|
- **Primary problem:** <name>  (why: the scores)
- **Breakthrough action:** <the one move>
- **Secondary (hold for now):** <…>
- **Re-evaluate when:** <signal/threshold>
```

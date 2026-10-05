# Bayesian lens — evidence to a calibrated belief

For "should I believe X?" decisions: start from a prior, grade each piece of evidence by
its likelihood ratio, update to a posterior, and tie the posterior to an action threshold.

## Protocol

1. **State the hypothesis** precisely (X vs not-X), and the **prior** P(X). The prior must
   come from a base rate, the user, or an assumption — never invented silently. Tag it with
   its grade (`SKILL.md`); a prior you had to assume is **grade D**, which *is* the
   assumption label — don't write "assumption" as a second, separate tag.
2. **List the evidence.** For each item, assign a **likelihood ratio** LR = P(evidence | X)
   / P(evidence | not-X). LR > 1 supports X, < 1 argues against, = 1 is uninformative. Get
   these from the user or justify each from the evidence; grade each one (A/B/C/D).
3. **Update.** Call the script:
   ```bash
   python3 scripts/bayes_update.py --json '{"mode":"odds","prior_p":0.3,"likelihood_ratios":[4.0,0.5]}'
   ```
   For a success/failure count (e.g. "7 of 10 trials worked"), use the Beta mode:
   ```bash
   python3 scripts/bayes_update.py --json '{"mode":"beta","alpha":1,"beta":1,"successes":7,"failures":3}'
   ```
4. **Action threshold.** State the posterior probability at which the decision flips
   (e.g. "ship if P(works) > 0.8"), and compare.
5. **Sensitivity.** Re-run with `lr_power` < 1 (e.g. 0.5) to down-weight shaky evidence, or
   drop the weakest LR, and report whether the decision changes. A decision that flips on
   one soft LR is fragile — say so.

## Brief structure

```
## Decision — <hypothesis>
- **Read:** belief decision, stake <…>
- **Prior:** P(X) = <…>  (grade <A/B/C/D>, source)
- **Evidence:**
  | item | LR | grade | why |
  |---|---|---|---|
- **Posterior:** P(X) = <…>   (via bayes_update.py)
- **Threshold:** act if P(X) <…>; we are <above/below>
- **Sensitivity:** <survives down-weighting / dropping the weakest evidence?>
  <does it survive the C and D inputs moving? cheapest input to upgrade to A/B:>
- **Recommendation:** <…>
- **Watch window:** <date or event when this gets re-examined>
- **Stop condition:** <the observation that means this call was wrong>
- **Tripwire:** <the one signal worth interrupting for early>
```

The **grade** column is not decoration: it is what stops a measured 90-day log and a
half-remembered blog claim being multiplied together into one confident posterior. Use
each grade's own wording in the prose (`SKILL.md`).

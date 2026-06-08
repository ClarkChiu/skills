# Kelly lens — how much to commit when you have an edge

For "how much should I allocate/bet/invest?" decisions. Kelly sizes a commitment to
maximize long-run log growth given an edge — and refuses to size when there is no edge.

> Kelly is for sizing under a *real, estimated* edge. It is not investment advice, not for
> guaranteed-return claims, and not a license for martingale escalation. Default to
> **fractional Kelly** (half or quarter) because full Kelly is brutally volatile and very
> sensitive to mis-estimated odds.

## Protocol

1. **State the edge inputs** with their source: win probability `p` and net odds `b` (win
   `b` per 1 staked), or a list of outcome scenarios with probabilities and return
   multiples. These are estimates — label assumptions, and remember a wrong `p` hurts more
   than a wrong `b`.
2. **Size it.** Binary:
   ```bash
   python3 scripts/kelly_size.py --json '{"mode":"binary","b":2.0,"p":0.6,"fraction":0.5}'
   ```
   Multi-scenario (maximizes E[log(1+f·r)]):
   ```bash
   python3 scripts/kelly_size.py --json '{"mode":"scenarios","scenarios":[
     {"prob":0.6,"return_multiple":2.0},{"prob":0.4,"return_multiple":-1.0}],"fraction":0.5}'
   ```
3. **Default to fractional Kelly** (`"fraction":0.5` or `0.25`) and an absolute `"cap"` on
   any single commitment. Report both the full Kelly and the sized recommendation.
4. **No edge → no allocation.** If full Kelly ≤ 0 the script says "do not allocate" — honor
   it; do not talk yourself into a bet.
5. **Downside.** State what a losing outcome costs and whether you can survive a run of them
   (Kelly assumes you can re-bet; ruin breaks the math).

## Brief structure

```
## Allocation — <opportunity>
- **Read:** allocation decision, stake <…>
- **Edge inputs:** p = <…>, b = <…>  (source / assumption)
- **Full Kelly:** <f*>   (via kelly_size.py)
- **Recommended size:** <fractional + cap>, fraction = <0.5/0.25>
- **If no edge:** do not allocate
- **Downside / survivability:** <…>
```

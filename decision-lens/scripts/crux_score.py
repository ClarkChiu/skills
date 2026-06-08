#!/usr/bin/env python3
"""Primary/secondary problem prioritization for decision-lens — pure stdlib, deterministic.

Scores each candidate problem on three tests (each 0..1) and ranks them; the top item is
the *primary* problem to break first:
  decisiveness : how much solving it unblocks everything else
  leverage     : how much the available resources actually move it now
  stage        : whether this is the right stage to act on it

Weighted sum -> ranking. Reads JSON from --json or stdin, prints JSON. No net/env/writes.

Request example:
  {"problems": [
     {"name": "flaky CI", "decisiveness": 0.9, "leverage": 0.7, "stage": 0.8},
     {"name": "docs debt", "decisiveness": 0.3, "leverage": 0.6, "stage": 0.4}],
   "weights": {"decisiveness": 0.5, "leverage": 0.3, "stage": 0.2}}
"""
import sys
import json
import argparse

DEFAULT_WEIGHTS = {"decisiveness": 0.5, "leverage": 0.3, "stage": 0.2}


def score_one(item, weights):
    s = 0.0
    for k, w in weights.items():
        v = item.get(k)
        if v is None or not (0.0 <= v <= 1.0):
            raise ValueError(f"{item.get('name')!r}: '{k}' must be a number in [0, 1]")
        s += w * v
    return s


def rank(problems, weights):
    scored = [
        {"name": p["name"], "score": score_one(p, weights),
         "decisiveness": p["decisiveness"], "leverage": p["leverage"], "stage": p["stage"]}
        for p in problems
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def main():
    ap = argparse.ArgumentParser(description="Primary/secondary problem prioritization")
    ap.add_argument("--json", help="inline JSON request; otherwise read stdin")
    args = ap.parse_args()
    req = json.loads(args.json if args.json else sys.stdin.read())
    weights = req.get("weights", DEFAULT_WEIGHTS)
    ranked = rank(req["problems"], weights)
    out = {"ranked": ranked, "primary": ranked[0]["name"] if ranked else None, "weights": weights}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Kelly allocation calculator for decision-lens — pure stdlib, deterministic.

Modes:
  binary    : net odds b, win prob p -> full Kelly fraction f* = (b*p - q)/b
  scenarios : list of {prob, return_multiple} -> fraction maximizing E[log(1+f*r)] by grid

Both apply an optional fractional-Kelly multiplier (1.0 full / 0.5 half / 0.25 quarter)
and an optional cap. A non-positive full Kelly means no edge -> size 0, "do not allocate".
Reads JSON from --json or stdin, prints JSON. No network, no env, no file writes.

Request examples:
  {"mode": "binary", "b": 2.0, "p": 0.6, "fraction": 0.5, "cap": 0.1}
  {"mode": "scenarios", "scenarios": [{"prob":0.6,"return_multiple":2.0},
                                       {"prob":0.4,"return_multiple":-1.0}], "fraction": 0.5}
"""
import sys
import json
import math
import argparse


def binary_kelly(b, p):
    """f* = (b*p - q)/b for net odds b>0, win prob p in [0,1]. May be <= 0 (no edge)."""
    if b <= 0:
        raise ValueError("net odds b must be > 0")
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must be in [0, 1]")
    q = 1.0 - p
    return (b * p - q) / b


def expected_log_growth(fraction, scenarios):
    total = 0.0
    for s in scenarios:
        w = 1.0 + fraction * s["return_multiple"]
        if w <= 0:
            return float("-inf")
        total += s["prob"] * math.log(w)
    return total


def scenario_kelly(scenarios, steps=1000):
    """Grid-search f in [0,1] maximizing E[log(1+f*r)]. Returns (f, growth)."""
    best_f, best_g = 0.0, expected_log_growth(0.0, scenarios)
    for i in range(1, steps + 1):
        f = i / steps
        g = expected_log_growth(f, scenarios)
        if g > best_g:
            best_f, best_g = f, g
    return best_f, best_g


def apply_caps(full_kelly, fraction_mult, cap):
    """Clamp to non-negative, scale by fractional Kelly, then apply optional cap."""
    sized = max(0.0, full_kelly) * fraction_mult
    if cap is not None:
        sized = min(sized, cap)
    return sized


def main():
    ap = argparse.ArgumentParser(description="Kelly allocation calculator")
    ap.add_argument("--json", help="inline JSON request; otherwise read stdin")
    args = ap.parse_args()
    req = json.loads(args.json if args.json else sys.stdin.read())
    mode = req.get("mode")
    fraction_mult = req.get("fraction", 1.0)
    cap = req.get("cap")
    if mode == "binary":
        full = binary_kelly(req["b"], req["p"])
        out = {"full_kelly": full, "sized": apply_caps(full, fraction_mult, cap),
               "edge": full > 0, "fraction": fraction_mult, "cap": cap}
    elif mode == "scenarios":
        full, growth = scenario_kelly(req["scenarios"], req.get("steps", 1000))
        out = {"full_kelly": full, "expected_log_growth": growth,
               "sized": apply_caps(full, fraction_mult, cap),
               "edge": full > 0, "fraction": fraction_mult, "cap": cap}
    else:
        raise ValueError("mode must be 'binary' or 'scenarios'")
    if not out["edge"]:
        out["recommendation"] = "no edge — do not allocate"
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

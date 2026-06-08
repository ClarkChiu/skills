#!/usr/bin/env python3
"""Bayesian decision calculator for decision-lens — pure stdlib, deterministic.

Two modes:
  odds : prior probability + a list of likelihood ratios -> posterior probability
         (posterior_odds = prior_odds * product(LR_i ** lr_power))
  beta : Beta(alpha, beta) prior + successes/failures -> posterior mean + ~95% interval

Reads a JSON request from --json or stdin, prints a JSON result to stdout.
No network, no environment reads, no file writes.

Request examples:
  {"mode": "odds", "prior_p": 0.3, "likelihood_ratios": [4.0, 0.5], "lr_power": 1.0}
  {"mode": "beta", "alpha": 1, "beta": 1, "successes": 8, "failures": 2}
"""
import sys
import json
import math
import argparse


def odds_update(prior_p, likelihood_ratios, lr_power=1.0):
    """Posterior via odds form. prior_p in (0,1); each LR > 0."""
    if not (0.0 < prior_p < 1.0):
        raise ValueError("prior_p must be strictly between 0 and 1")
    prior_odds = prior_p / (1.0 - prior_p)
    odds = prior_odds
    for lr in likelihood_ratios:
        if lr <= 0:
            raise ValueError("each likelihood ratio must be > 0")
        odds *= lr ** lr_power
    posterior_p = odds / (1.0 + odds)
    return {
        "prior_p": prior_p,
        "prior_odds": prior_odds,
        "posterior_odds": odds,
        "posterior_p": posterior_p,
        "lr_power": lr_power,
        "n_evidence": len(likelihood_ratios),
    }


def beta_update(alpha, beta, successes, failures):
    """Beta-Binomial conjugate posterior + normal-approx 95% interval."""
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be > 0")
    if successes < 0 or failures < 0:
        raise ValueError("successes and failures must be >= 0")
    a2 = alpha + successes
    b2 = beta + failures
    mean = a2 / (a2 + b2)
    var = (a2 * b2) / ((a2 + b2) ** 2 * (a2 + b2 + 1))
    sd = math.sqrt(var)
    return {
        "posterior_alpha": a2,
        "posterior_beta": b2,
        "posterior_mean": mean,
        "posterior_sd": sd,
        "approx_95_low": max(0.0, mean - 1.96 * sd),
        "approx_95_high": min(1.0, mean + 1.96 * sd),
    }


def main():
    ap = argparse.ArgumentParser(description="Bayesian decision calculator")
    ap.add_argument("--json", help="inline JSON request; otherwise read stdin")
    args = ap.parse_args()
    req = json.loads(args.json if args.json else sys.stdin.read())
    mode = req.get("mode")
    if mode == "odds":
        out = odds_update(req["prior_p"], req["likelihood_ratios"], req.get("lr_power", 1.0))
    elif mode == "beta":
        out = beta_update(req["alpha"], req["beta"], req["successes"], req["failures"])
    else:
        raise ValueError("mode must be 'odds' or 'beta'")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

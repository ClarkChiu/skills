"""Unit tests for decision-lens calculators — verify the math, not just that it runs.

Each test pins a known input to a known closed-form output, so a regression in the
formula (not just a crash) fails the test. Run: python3 -m pytest <thisfile> -q
"""
import math
import pytest

import bayes_update
import kelly_size
import crux_score


# ---- bayes_update: odds mode ----

def test_odds_update_known_posterior():
    # prior 0.5 (odds 1) times LR 2 and 3 -> odds 6 -> p = 6/7
    out = bayes_update.odds_update(0.5, [2.0, 3.0])
    assert out["posterior_odds"] == pytest.approx(6.0)
    assert out["posterior_p"] == pytest.approx(6.0 / 7.0)
    assert out["n_evidence"] == 2


def test_odds_update_lr_power_dampens():
    # lr_power 0 neutralizes evidence -> posterior == prior
    out = bayes_update.odds_update(0.3, [10.0, 0.1], lr_power=0.0)
    assert out["posterior_p"] == pytest.approx(0.3)


def test_odds_update_rejects_degenerate_prior():
    for bad in (0.0, 1.0, -0.1, 1.5):
        with pytest.raises(ValueError):
            bayes_update.odds_update(bad, [2.0])


def test_odds_update_rejects_nonpositive_lr():
    with pytest.raises(ValueError):
        bayes_update.odds_update(0.5, [2.0, 0.0])


# ---- bayes_update: beta mode ----

def test_beta_update_known_mean():
    # Beta(1,1) + 8 successes, 2 failures -> Beta(9,3), mean 9/12 = 0.75
    out = bayes_update.beta_update(1, 1, 8, 2)
    assert out["posterior_alpha"] == 9
    assert out["posterior_beta"] == 3
    assert out["posterior_mean"] == pytest.approx(0.75)
    assert 0.0 <= out["approx_95_low"] < out["approx_95_high"] <= 1.0


def test_beta_update_rejects_bad_params():
    with pytest.raises(ValueError):
        bayes_update.beta_update(0, 1, 1, 1)
    with pytest.raises(ValueError):
        bayes_update.beta_update(1, 1, -1, 1)


# ---- kelly_size: binary ----

def test_binary_kelly_no_edge_is_zero():
    # fair coin, even odds -> f* = 0
    assert kelly_size.binary_kelly(1.0, 0.5) == pytest.approx(0.0)


def test_binary_kelly_known_fraction():
    # b=2, p=0.6 -> f* = (2*0.6 - 0.4)/2 = 0.4
    assert kelly_size.binary_kelly(2.0, 0.6) == pytest.approx(0.4)


def test_binary_kelly_fractional_and_cap():
    full = kelly_size.binary_kelly(2.0, 0.6)  # 0.4
    assert kelly_size.apply_caps(full, 0.5, None) == pytest.approx(0.2)   # half Kelly
    assert kelly_size.apply_caps(full, 1.0, 0.1) == pytest.approx(0.1)    # cap binds
    assert kelly_size.apply_caps(-0.3, 1.0, None) == pytest.approx(0.0)   # no negative sizing


def test_scenario_kelly_matches_binary():
    # a binary bet expressed as scenarios should land near the closed-form f*
    scenarios = [{"prob": 0.6, "return_multiple": 2.0}, {"prob": 0.4, "return_multiple": -1.0}]
    f, growth = kelly_size.scenario_kelly(scenarios, steps=2000)
    assert f == pytest.approx(0.4, abs=0.01)


# ---- crux_score ----

def test_crux_primary_is_highest_decisiveness():
    problems = [
        {"name": "A", "decisiveness": 0.9, "leverage": 0.5, "stage": 0.5},
        {"name": "B", "decisiveness": 0.2, "leverage": 0.5, "stage": 0.5},
    ]
    out = crux_score.rank(problems, crux_score.DEFAULT_WEIGHTS)
    assert out[0]["name"] == "A"
    assert out[0]["score"] > out[1]["score"]


def test_crux_rejects_out_of_range():
    with pytest.raises(ValueError):
        crux_score.score_one({"name": "X", "decisiveness": 1.5, "leverage": 0.5, "stage": 0.5},
                             crux_score.DEFAULT_WEIGHTS)

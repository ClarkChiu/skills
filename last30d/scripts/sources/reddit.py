"""EXTRACT (not a full copy) of upstream ``skills/last30days/scripts/lib/reddit.py``.

Upstream ``reddit.py`` is the keyed ScrapeCreators Reddit path (~730 lines plus
``providers``/``query``/``signals`` deps) that this skill deliberately does not vendor.
The vendored ``reddit_search.py`` lazily imports ONE helper from it
(``from .reddit import _window_to_time_filter``) on its hot path, and swallows the
ImportError into a silent empty result if it is missing. So the two pure date helpers
it needs are copied here VERBATIM from mvanhorn/last30days-skill @ 5103ba478b38
(MIT) — byte-for-byte function bodies, nothing else. Re-sync: re-extract these
definitions, don't hand-edit. ``tests/test_vendored_symbols_resolve.py`` checks that
every name a vendored file imports from here exists.
"""
from datetime import date, datetime, timezone


def _days_to_reddit_bucket(days: float) -> str:
    """Map a day count onto the smallest Reddit rolling bucket that covers it.

    Adds one day of slack so calendar windows that cross a day boundary still
    fit inside Reddit's rolling ``t=`` buckets (a yesterday→today request needs
    ``week``, not ``day``).
    """
    covered = days + 1
    if covered <= 1:
        return "day"
    if covered <= 7:
        return "week"
    if covered <= 31:
        return "month"
    if covered <= 366:
        return "year"
    return "all"


def _window_to_time_filter(from_date: str, to_date: str) -> str:
    """Map a requested YYYY-MM-DD window onto Reddit's coarse `t` param.

    Reddit's ``t=day|week|month`` buckets are rolling windows ending *now*, not
    calendar spans and not anchored to ``to_date``. Coverage therefore needs:

    1. Span — a yesterday→today request needs more than rolling ``t=day``.
    2. Historical reach — a one-day request ending two weeks ago still needs a
       bucket that reaches ``from_date``; span-alone would pick ``week`` and
       the API would omit the entire requested range.

    Take the wider of the two; the caller then mins with the depth default.
    Phase 5 still trims to ``from_date``/``to_date``. Falls back to ``month``
    if the dates don't parse.
    """
    try:
        start = date.fromisoformat(from_date)
        end = date.fromisoformat(to_date)
    except (ValueError, TypeError):
        return "month"
    span_days = max(0, (end - start).days)
    # Age of from_date relative to "today" — Reddit always anchors to now.
    age_days = max(0, (datetime.now(timezone.utc).date() - start).days)
    return _days_to_reddit_bucket(max(span_days, age_days))

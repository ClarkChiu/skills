#!/usr/bin/env python3
"""last30d — last-30-days social-signal fetcher.

Fetches a topic's recent discussion across Reddit / X / HN / GitHub / arXiv / YouTube,
ranks each lane by its own engagement metric, and prints a per-lane digest. Synthesis is
NOT done here — hand the digest to the session model or `deep-research`.

Lanes run concurrently; a failing lane degrades to 0 results (logged), never aborts the run.
X (needs XAI_API_KEY) and YouTube (needs yt-dlp) skip visibly when unavailable.
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # so `sources` imports when run directly
from sources import reddit_lane, x_lane, hn, arxiv, github, youtube, digest  # noqa: E402

DEPTH_N = {"quick": 10, "default": 25, "deep": 50}
ALL_LANES = ["reddit", "x", "hn", "github", "arxiv", "youtube"]
_MOD = {"reddit": reddit_lane, "x": x_lane, "hn": hn, "arxiv": arxiv,
        "github": github, "youtube": youtube}


def _call(lane, topic, from_date, to_date, n, depth):
    mod = _MOD[lane]
    if lane in ("reddit", "x"):
        return mod.search(topic, from_date, to_date, limit=n, depth=depth)
    return mod.search(topic, from_date, to_date, limit=n)


def run(topic, depth="default", lanes=None, as_of=None):
    lanes = lanes or ALL_LANES
    n = DEPTH_N.get(depth, DEPTH_N["default"])
    to_dt = datetime.fromisoformat(as_of).replace(tzinfo=timezone.utc) if as_of else datetime.now(timezone.utc)
    to_date, from_date = to_dt.date().isoformat(), (to_dt - timedelta(days=30)).date().isoformat()

    results, skips = {}, {}

    def one(lane):
        try:
            return lane, _call(lane, topic, from_date, to_date, n, depth)
        except Exception as e:  # fail loud, don't abort the run
            sys.stderr.write(f"[last30d] lane {lane} failed: {type(e).__name__}: {e}\n")
            return lane, []

    with ThreadPoolExecutor(max_workers=min(len(lanes), 6) or 1) as ex:
        for lane, recs in ex.map(one, lanes):
            results[lane] = recs
    # Surface skip reasons for the optional lanes when they came back empty.
    if "x" in lanes and not results.get("x") and x_lane.SKIP.get("reason"):
        skips["x"] = x_lane.SKIP["reason"]
    if "youtube" in lanes and not results.get("youtube") and youtube.SKIP.get("reason"):
        skips["youtube"] = youtube.SKIP["reason"]
    return from_date, to_date, results, skips


def main(argv=None):
    ap = argparse.ArgumentParser(prog="last30d", description="last-30-days social-signal fetcher")
    ap.add_argument("topic")
    ap.add_argument("--depth", choices=list(DEPTH_N), default="default")
    ap.add_argument("--lanes", default=",".join(ALL_LANES),
                    help="comma-separated subset of: " + ",".join(ALL_LANES))
    ap.add_argument("--json", action="store_true", help="emit structured JSON")
    ap.add_argument("--save", metavar="PATH", help="write output to a file")
    ap.add_argument("--as-of", help=argparse.SUPPRESS)  # test hook: fixes 'today'
    a = ap.parse_args(argv)

    requested = [l.strip() for l in a.lanes.split(",") if l.strip()]
    lanes = [l for l in requested if l in ALL_LANES]
    bad = [l for l in requested if l not in ALL_LANES]
    if bad:  # fail loud (Rule 12) rather than silently dropping unknown lanes
        sys.stderr.write(f"[last30d] ignoring unknown lane(s): {', '.join(bad)}; "
                         f"valid: {', '.join(ALL_LANES)}\n")
    if not lanes:
        sys.stderr.write("[last30d] no valid lanes selected — nothing to do.\n")
        return 2
    frm, to, results, skips = run(a.topic, a.depth, lanes, a.as_of)
    render = digest.render_json if a.json else digest.render_markdown
    out = render(a.topic, frm, to, results, skips)
    if a.save:
        with open(a.save, "w", encoding="utf-8") as fh:
            fh.write(out)
        sys.stderr.write(f"[last30d] wrote {a.save}\n")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

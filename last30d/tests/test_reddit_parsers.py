"""Offline regression tests for the VENDORED Reddit parsers.

Intent (CLAUDE.md Rule 9): these fixtures are real upstream captures. If a re-sync
(re-pull from upstream) silently breaks a parser — a changed shreddit attribute name,
a different comment element — these fail loudly instead of the lane going quietly empty.
"""
import sys

import pytest
from conftest import fixture

from sources import http, reddit_listing, reddit_search, reddit_shreddit


def test_listing_cards_parse_with_real_scores():
    posts = reddit_listing.parse_cards(fixture("reddit_listing_cards_sample.html"), query="")
    assert posts, "listing parser returned no <shreddit-post> cards"
    # The listing partial is THE keyless source of real upvote scores — assert we got one.
    assert any(p["score"] > 0 for p in posts), "no post carried a real upvote score"
    assert all("/comments/" in p["url"] for p in posts), "a card lacked a valid permalink"


def test_shreddit_comments_parse_with_scores_and_authors():
    comments = reddit_shreddit.parse_comments(fixture("reddit_shreddit_comments_sample.html"))
    assert comments, "comment parser returned no <shreddit-comment> elements"
    top = comments[0]
    assert top["author"] and top["author"] not in ("[deleted]", "[removed]")
    assert top["body"], "top comment had no body text"
    # parse_comments sorts by score desc — the first must be the highest.
    assert comments == sorted(comments, key=lambda c: c["score"], reverse=True)


# ---- Site search (reddit_search) — the discovery source since Reddit's RSS shutdown ----
# Fixtures are upstream's 2026-09-30 captures (challenge is upstream's synthetic page).

def test_search_page_parses_scored_posts_and_next_cursor():
    posts, cursor = reddit_search.parse_page(fixture("reddit_search_page1.html"), query="ButcherBox")
    # Discovery and scoring now come from ONE page: if the counters stop parsing, every
    # post ranks at zero engagement and the lane silently loses its ranking signal.
    assert len(posts) == 7, "page 1 fixture has 7 post units"
    assert all("/comments/" in p["url"] and p["url"].startswith("https://www.reddit.com/r/")
               for p in posts), "a post lacked a canonical permalink"
    assert all(p["title"] and p["subreddit"] for p in posts)
    assert any(p["score"] > 0 for p in posts) and any(p["num_comments"] > 0 for p in posts)
    assert len({p["metadata"]["post_id"] for p in posts}) == 7, "post ids not unique"
    # Without the cursor, paging stops at ~7 posts and depth=deep silently means depth=quick.
    assert cursor, "next-page cursor not found"


@pytest.mark.skipif(sys.version_info < (3, 11), reason=(
    "upstream reddit_listing._to_date uses datetime.fromisoformat, which cannot parse "
    "Reddit's '+0000' offset before Python 3.11 — on 3.10 Reddit dates are blank "
    "(see SKILL.md)"))
def test_search_page_posts_are_dated():
    # reddit_lane trims to the requested window by this date; undated posts pass untrimmed.
    posts, _ = reddit_search.parse_page(fixture("reddit_search_page1.html"), query="ButcherBox")
    assert all(p["date"] and len(p["date"]) == 10 for p in posts)


def test_search_last_page_has_posts_but_no_cursor():
    posts, cursor = reddit_search.parse_page(fixture("reddit_search_last_page.html"), query="Tubi")
    assert len(posts) == 2
    # A cursor here would make _search_stream re-request forever-ish instead of stopping.
    assert cursor is None


def test_search_challenge_page_is_a_failure_not_zero_results():
    # An HTTP 200 anti-bot page must be rejected by the fetch validator — otherwise it is
    # memoized and reported as a clean "nothing was discussed", the worst silent failure.
    html = fixture("reddit_search_challenge.html")
    assert reddit_search.unrecognized_body(html), "challenge page accepted as a results page"
    assert reddit_search.parse_page(html)[0] == []


def test_search_no_results_page_is_a_clean_empty():
    # The opposite case: Reddit's explicit no-results unit is a real empty, not drift.
    html = fixture("reddit_search_no_results.html")
    assert reddit_search.unrecognized_body(html) is None
    assert reddit_search.parse_page(html) == ([], None)


def test_search_stream_pages_until_cursor_runs_out(monkeypatch):
    # End-to-end through the real fetch seam (http.reddit_keyless_get_text_retry_429),
    # offline: page 1 yields a cursor, the second request carries it, the last page stops.
    pages = [fixture("reddit_search_page1.html"), fixture("reddit_search_last_page.html")]
    urls = []

    def fake_fetch(url, **kwargs):
        urls.append(url)
        body = pages[len(urls) - 1]
        problem = kwargs["validate"](body)
        return (None, problem) if problem else (body, None)

    monkeypatch.setattr(http, "reddit_keyless_get_text_retry_429", fake_fetch)
    posts = reddit_search.search("ButcherBox", depth="default",
                                 from_date="2026-09-05", to_date="2026-10-05")
    assert len(urls) == 2 and "cursor=" in urls[1] and "cursor=" not in urls[0]
    assert all(u.startswith("https://www.reddit.com/svc/shreddit/search/?") for u in urls)
    assert len(posts) == 9 and [p["id"] for p in posts[:2]] == ["R1", "R2"]


def test_shreddit_drops_bot_comments_before_ranking():
    # reddit_lane surfaces only top_comments[0]; a stickied AutoModerator notice with the
    # highest score must not become the post's "community signal" excerpt.
    bot = ('<shreddit-comment created="2026-05-11T19:00:00.000000+0000" author="AutoModerator" '
           'thingId="t1_bot0001" depth="0" permalink="/r/Rakuten/comments/1taeiw0/comment/bot0001/" '
           'score="999" postId="t3_1taeiw0" content-type="text">\n'
           '  <div id="t1_bot0001-comment-rtjson-content" slot="comment"><div id="t1_bot0001-post-rtjson-content" '
           'dir="auto"><p dir="auto">Please read the subreddit rules before posting.</p></div></div>\n'
           '</shreddit-comment>\n')
    html = fixture("reddit_shreddit_comments_sample.html").replace(
        '<shreddit-comment-tree id="comment-tree" post-id="t3_1taeiw0">',
        '<shreddit-comment-tree id="comment-tree" post-id="t3_1taeiw0">\n' + bot, 1)
    comments = reddit_shreddit.parse_comments(html)
    assert comments, "injection broke the fixture"
    assert all(c["author"] != "AutoModerator" for c in comments)

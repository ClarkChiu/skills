"""Offline regression tests for the VENDORED Reddit parsers.

Intent (CLAUDE.md Rule 9): these fixtures are real upstream captures. If a re-sync
(re-pull from upstream) silently breaks a parser — a changed shreddit attribute name,
a different comment element — these fail loudly instead of the lane going quietly empty.
"""
from conftest import fixture

from sources import reddit_listing, reddit_shreddit, reddit_rss


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


def test_rss_feed_parse_yields_posts():
    posts = reddit_rss._parse_feed(fixture("reddit_search_rss_sample.xml"), query="")
    assert posts, "RSS parser returned no entries"
    assert all(p["url"] and "/comments/" in p["url"] for p in posts)
    assert all(p["title"] for p in posts), "an RSS entry had no title"

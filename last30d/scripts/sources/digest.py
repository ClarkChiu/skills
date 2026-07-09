"""Render the ranked lane records into a per-lane Markdown digest (or JSON).

Per-lane sections, never a merged score table — cross-platform engagement scales aren't
comparable. Reddit rows carry their single top comment. Skipped lanes render a visible
`skipped: <reason>` line (Rule 12). The header lists per-lane counts.
"""
import json

# Fixed display order + human titles.
LANES = [("reddit", "Reddit"), ("x", "X"), ("hn", "Hacker News"),
         ("github", "GitHub"), ("arxiv", "arXiv"), ("youtube", "YouTube")]


def _score_cell(rec):
    # arXiv has no engagement metric (recency-ranked) — don't show a fake 0.
    return "—" if rec.get("score_label") == "arxiv" else str(rec.get("score", 0))


def render_markdown(topic, from_date, to_date, results, skips):
    counts = " ".join(f"{k} {len(results.get(k, []))}" for k, _ in LANES if k in results)
    lines = [f'# last30days: "{topic}"  ({from_date} → {to_date})',
             f"# lanes: {counts}  |  ranked by per-lane engagement", ""]
    for key, title in LANES:
        if key in skips:
            lines += [f"## {title}", f"_skipped: {skips[key]}_", ""]
            continue
        recs = results.get(key)
        if not recs:
            continue
        label = recs[0].get("score_label", "score")
        lines += [f"## {title}", f"| # | title | {label} | meta | date | link |",
                  "|---|-------|------:|------|------|------|"]
        for i, r in enumerate(recs, 1):
            title_txt = (r.get("title") or "").replace("|", "\\|")
            lines.append(f'| {i} | {title_txt} | {_score_cell(r)} | '
                         f'{r.get("meta", "")} | {r.get("date", "")} | [↗]({r.get("url", "")}) |')
            if r.get("top_comment"):
                lines.append(f'      ↳ top comment {r["top_comment"]}')
        lines.append("")
    return "\n".join(lines)


def render_json(topic, from_date, to_date, results, skips):
    return json.dumps({"topic": topic, "from": from_date, "to": to_date,
                       "lanes": results, "skipped": skips}, ensure_ascii=False, indent=2)

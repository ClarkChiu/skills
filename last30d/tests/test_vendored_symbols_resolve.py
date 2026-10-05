"""Every attribute a vendored file reads off another vendored module must exist here.

Intent (CLAUDE.md Rule 9): the vendored Reddit/xAI files are copied verbatim from
mvanhorn/last30days-skill, but not their whole upstream closure. So a newer leaf file can
call a helper that does not exist here, and the failure only appears at fetch time, on the
network path, in production. The offline parser tests cannot see it: they call `parse_*`
directly and never enter a fetch function.

That is not hypothetical — on 2026-09-17 a re-pull of reddit_rss.py / reddit_listing.py was
rejected precisely because the new versions needed http helpers the then-held http.py did
not have. And on 2026-10-05 the new reddit_search.py lazily does
`from .reddit import _window_to_time_filter` inside a try/except that turns an ImportError
into a silent empty Reddit lane — so `from .mod import name` must resolve too.

It reads the source with `ast` rather than importing and calling, so it needs no network
and no fixtures: for every `from . import X` / `import X` in a vendored module, it collects
every `X.attr` reference and asserts `attr` exists on the local module; for every
`from .X import name` it asserts `X` exists locally and has `name`. A relative import of a
module we deliberately do not vendor must be listed in NOT_VENDORED_UNREACHED with the
reason its code path is never reached here.
"""
import ast
import importlib
import os

import conftest  # noqa: F401

SOURCES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "scripts", "sources")

# Files vendored verbatim from upstream (sources.lock `vendored`), plus our own lane
# adapters that call into them — a held http.py breaks either one the same way.
CHECKED = ["reddit_search.py", "reddit_listing.py", "reddit_shreddit.py", "reddit_enrich.py",
           "xai_x.py", "http.py", "health.py", "reddit.py", "reddit_lane.py", "x_lane.py",
           "relevance.py", "digest.py"]

# (file, missing module or module.attr) -> why that path never runs in this skill.
NOT_VENDORED_UNREACHED = {
    ("reddit_listing.py", "reddit_arctic"):
        "only fetch_discovery_listings() uses it; reddit_lane never calls that",
    ("http.py", "env"):
        "only config_secret_values() (fixture-recording redaction) uses it, inside try/except",
    ("reddit_enrich.py", "reddit.fetch_post_comments"):
        "keyed ScrapeCreators enrich path; reddit.py here is a 2-function date-helper extract",
}


def _local_modules():
    return {f[:-3] for f in os.listdir(SOURCES) if f.endswith(".py") and f != "__init__.py"}


def test_vendored_modules_only_use_symbols_that_exist_here():
    local = _local_modules()
    missing = []
    for fname in CHECKED:
        path = os.path.join(SOURCES, fname)
        assert os.path.exists(path), f"{fname} is listed as vendored but is not in scripts/sources/"
        tree = ast.parse(open(path, encoding="utf-8").read(), filename=fname)

        # Which sibling modules does this file pull in, and under what local name?
        imported = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1:
                if node.module:  # `from .mod import name` — mod must exist and have name
                    if node.module not in local:
                        if (fname, node.module) not in NOT_VENDORED_UNREACHED:
                            missing.append(f"{fname}:{node.lineno} imports unvendored .{node.module}")
                        continue
                    mod = importlib.import_module(f"sources.{node.module}")
                    for a in node.names:
                        if not hasattr(mod, a.name):
                            missing.append(f"{fname}:{node.lineno} needs {node.module}.{a.name}")
                    continue
                for a in node.names:
                    if a.name in local:
                        imported[a.asname or a.name] = a.name
                    elif (fname, a.name) not in NOT_VENDORED_UNREACHED:
                        missing.append(f"{fname}:{node.lineno} imports unvendored .{a.name}")
            elif isinstance(node, ast.Import):
                for a in node.names:
                    base = a.name.split(".")[0]
                    if base in local:
                        imported[a.asname or base] = base

        # Every `mod.attr` read on one of those modules must resolve locally.
        for node in ast.walk(tree):
            if (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
                    and node.value.id in imported):
                mod_name = imported[node.value.id]
                mod = importlib.import_module(f"sources.{mod_name}")
                if (not hasattr(mod, node.attr)
                        and (fname, f"{mod_name}.{node.attr}") not in NOT_VENDORED_UNREACHED):
                    missing.append(f"{fname}:{node.lineno} needs {mod_name}.{node.attr}")

    assert not missing, (
        "vendored file(s) reference symbols missing from the local copies — a verbatim "
        "re-pull went in without its dependency, or http.py is held too far back:\n  "
        + "\n  ".join(sorted(set(missing))))

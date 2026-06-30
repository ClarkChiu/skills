#!/usr/bin/env python3
"""lint-skills.py — 檢查自建技能是否符合本專案不變量。無第三方相依。
用法: python3 scripts/lint-skills.py  (在 repo 根目錄)；有違規則 exit 1。
規則來源與理由見 docs/skill-style-guide.md。"""
import json, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYMLINK_BASES = [".claude/skills", ".agents/skills"]  # opencode 經 .agents/skills 取用，無 repo 級 .opencode/skills
apm = (ROOT / "apm.yml").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m: return None
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_]+):\s*(.*)", line)
        if km: fm[km.group(1)] = km.group(2)
    return fm

skills = sorted(p.parent for p in ROOT.glob("*/SKILL.md"))
violations = []
for d in skills:
    name = d.name
    def bad(msg): violations.append(f"{name}: {msg}")

    ev = d / "evals" / "evals.json"
    if not ev.exists(): bad("缺 evals/evals.json")
    else:
        try: json.loads(ev.read_text(encoding="utf-8"))
        except Exception as e: bad(f"evals.json 非合法 JSON ({e})")

    fm = frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
    if fm is None: bad("SKILL.md 無 frontmatter")
    else:
        if not fm.get("name"): bad("frontmatter 缺 name")
        elif fm["name"] != name: bad(f"name='{fm['name']}' != 目錄名")
        if not fm.get("description"): bad("frontmatter 缺 description")

    has_attr = (d / "references" / "attribution.md").exists()
    has_lock = (d / "sources.lock").exists()
    if has_attr != has_lock:
        bad(f"attribution/sources.lock 未成對 (attr={has_attr} lock={has_lock})")

    if f"./{name}/" not in apm: bad("未登錄 apm.yml dependencies")
    if name not in readme: bad("README 未提及")
    for base in SYMLINK_BASES:
        if not (ROOT / base / name).exists(): bad(f"缺 symlink: {base}/{name}")

if violations:
    print(f"✗ {len(violations)} 項違規：")
    for v in violations: print("  -", v)
    sys.exit(1)
print(f"✓ {len(skills)} 個自建技能全部通過")

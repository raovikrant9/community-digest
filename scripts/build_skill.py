#!/usr/bin/env python3
"""Assemble skill/SKILL.md from the template plus the two scripts, so they stay in sync."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
template = (root / "skill" / "SKILL.template.md").read_text()
out = template.replace("{{WA_SCRIPT}}", (root / "scripts" / "wa_extract.py").read_text().rstrip()).replace(
    "{{SLACK_SCRIPT}}", (root / "scripts" / "slack_pull.js").read_text().rstrip()
)
(root / "skill" / "SKILL.md").write_text(out)
print("wrote skill/SKILL.md")

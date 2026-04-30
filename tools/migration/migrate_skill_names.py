#!/usr/bin/env python3
"""DIA migration -- Phase 6: update legacy skill name references.

Rewrites references to the old skill names:
- /business-analyse -> /business-analysis
- /v-model-workflow -> /dia-orchestrator
- skills/business-analyse/ -> skills/business-analysis/
- skills/v-model-workflow/ -> skills/dia-orchestrator/
- bare names: business-analyse -> business-analysis,
  v-model-workflow -> dia-orchestrator (skill-name only;
  "V-Model" the methodology stays untouched)

Idempotent. No-op for repos that already use the new names.

Skips the append-only handoff log
(`_devprocess/context/HANDOFFS.md`) by default to preserve audit
trail.

Usage:
    python3 migrate_skill_names.py [project_root]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

SKIP = {"_devprocess/context/HANDOFFS.md"}


def transform(content: str) -> str:
    content = content.replace("skills/business-analyse/", "skills/business-analysis/")
    content = content.replace("skills/v-model-workflow/", "skills/dia-orchestrator/")
    content = content.replace("/business-analyse", "/business-analysis")
    content = content.replace("/v-model-workflow", "/dia-orchestrator")
    content = re.sub(r"\bbusiness-analyse\b", "business-analysis", content)
    content = re.sub(r"\bv-model-workflow\b(?!-imp)", "dia-orchestrator", content)
    return content


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    targets: list[Path] = []
    for ext in ("*.md", "*.json", "*.sh", "*.py", "*.ts", "*.yml", "*.yaml"):
        targets.extend(root.rglob(ext))
    skip_full = {root / s for s in SKIP}
    skip_dirs = (root / ".git", root / "node_modules", root / "backup")

    count = 0
    for fp in targets:
        if not fp.is_file():
            continue
        if any(str(fp).startswith(str(d)) for d in skip_dirs):
            continue
        if fp in skip_full:
            continue
        try:
            original = fp.read_text(encoding="utf-8")
        except Exception:
            continue
        new = transform(original)
        if new != original:
            fp.write_text(new, encoding="utf-8")
            count += 1
    print(f"Updated {count} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""PreToolUse guard — keep viewer/ UI on its own design system.

Blocks Write/Edit on viewer style-bearing files that introduce the neo-brutalist
"bleed" the project's global rule forbids here: a squared `border-radius: 0` or a
pure black/white hex palette. The viewer is a clean dark theme with rounded
corners (var(--cb-radius*)) and a purple accent (var(--cb-primary)) — see
.claude/rules/frontend.md, which OVERRIDES the global neo-brutalist rule.

global.css is exempt (design tokens are defined there). Fast, no network/AI.
Exit 2 blocks the tool call; exit 0 allows.
"""

import json
import re
import sys

STYLE_EXTS = (".css", ".tsx", ".astro")
RADIUS0_RE = re.compile(r"border-radius\s*:\s*0(?:px)?\b")
MONO_HEX_RE = re.compile(r"#(?:fff|000|ffffff|000000)\b", re.IGNORECASE)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # never block on a parse problem

    if data.get("tool_name") not in ("Write", "Edit"):
        return 0

    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or ""

    # Only guard viewer source style-bearing files; global.css defines the tokens.
    if "/viewer/" not in path or not path.endswith(STYLE_EXTS) or path.endswith("global.css"):
        return 0

    content = tool_input.get("content") if data["tool_name"] == "Write" else tool_input.get("new_string")
    content = content or ""

    problems = []
    if RADIUS0_RE.search(content):
        problems.append("`border-radius: 0` — the viewer is rounded; use var(--cb-radius*)")
    mono = sorted(set(m.lower() for m in MONO_HEX_RE.findall(content)))
    if mono:
        problems.append(f"pure black/white hex ({', '.join(mono)}) — use var(--cb-*) surface/text tokens")

    if problems:
        sys.stderr.write(
            "Blocked by viewer design guard (.claude/rules/frontend.md):\n"
            + "".join(f"  - {p}\n" for p in problems)
            + "The viewer has its own dark+rounded+purple design system that OVERRIDES the "
            "global neo-brutalist rule. Put styles in global.css and reference --cb-* tokens.\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

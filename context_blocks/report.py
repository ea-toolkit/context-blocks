"""Generate a standalone HTML gap report from eval-results.json."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ReportData:
    total: int = 0
    clean: int = 0
    incomplete: int = 0
    missing: int = 0
    per_persona: dict[str, dict[str, int]] = field(default_factory=dict)
    per_layer: dict[str, dict[str, int]] = field(default_factory=dict)
    per_source: dict[str, dict[str, int]] = field(default_factory=dict)
    questions: list[dict] = field(default_factory=list)
    gaps: list[dict] = field(default_factory=list)
    block_name: str = ""


def load_eval_results(eval_json: Path) -> ReportData:
    with open(eval_json) as f:
        results = json.load(f)

    rd = ReportData(total=len(results), questions=results)

    seen_gaps: set[str] = set()
    for r in results:
        cls = r.get("ddc_class", "MISSING")
        if cls == "CLEAN":
            rd.clean += 1
        elif cls == "INCOMPLETE":
            rd.incomplete += 1
        else:
            rd.missing += 1

        persona = r.get("persona", "")
        if persona:
            if persona not in rd.per_persona:
                rd.per_persona[persona] = {"CLEAN": 0, "INCOMPLETE": 0, "MISSING": 0, "total": 0}
            rd.per_persona[persona][cls] = rd.per_persona[persona].get(cls, 0) + 1
            rd.per_persona[persona]["total"] += 1

        layer = r.get("layer_hint", "")
        if layer:
            if layer not in rd.per_layer:
                rd.per_layer[layer] = {"CLEAN": 0, "INCOMPLETE": 0, "MISSING": 0, "total": 0}
            rd.per_layer[layer][cls] = rd.per_layer[layer].get(cls, 0) + 1
            rd.per_layer[layer]["total"] += 1

        source = r.get("source", "")
        if source:
            if source not in rd.per_source:
                rd.per_source[source] = {"CLEAN": 0, "INCOMPLETE": 0, "MISSING": 0, "total": 0}
            rd.per_source[source][cls] = rd.per_source[source].get(cls, 0) + 1
            rd.per_source[source]["total"] += 1

        for g in r.get("gaps", []):
            key = f"{g.get('gap_type', '')}:{g.get('entity_id', '')}:{g.get('description', '')[:60]}"
            if key not in seen_gaps:
                seen_gaps.add(key)
                rd.gaps.append(g)

    return rd


def _pct(n: int, total: int) -> str:
    if total == 0:
        return "0"
    return f"{n * 100 / total:.0f}"


def _severity_order(gap: dict) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(gap.get("severity", "low"), 3)


def generate_html(rd: ReportData, block_name: str = "") -> str:
    rd.block_name = block_name or "Domain"
    title = f"Gap Report — {rd.block_name}"
    clean_pct = _pct(rd.clean, rd.total)
    incomplete_pct = _pct(rd.incomplete, rd.total)
    missing_pct = _pct(rd.missing, rd.total)

    top_gaps = [q for q in rd.questions if q.get("ddc_class") != "CLEAN"]
    top_gaps.sort(key=lambda q: (0 if q.get("ddc_class") == "MISSING" else 1, -q.get("total_ms", 0)))
    top_five = top_gaps[:5]

    persona_rows = ""
    for name, counts in sorted(rd.per_persona.items()):
        t = counts["total"]
        c = counts.get("CLEAN", 0)
        pct = _pct(c, t)
        bar_w = int(c * 100 / t) if t else 0
        persona_rows += f"""
        <tr>
          <td class="persona-name">{name}</td>
          <td class="bar-cell">
            <div class="bar-track">
              <div class="bar-fill clean-bg" style="width:{bar_w}%"></div>
            </div>
          </td>
          <td class="pct">{pct}%</td>
          <td class="count">{c}/{t}</td>
        </tr>"""

    layer_rows = ""
    for name, counts in sorted(rd.per_layer.items()):
        t = counts["total"]
        c = counts.get("CLEAN", 0)
        i = counts.get("INCOMPLETE", 0)
        m = counts.get("MISSING", 0)
        layer_rows += f"""
        <tr>
          <td>{name}</td>
          <td class="count">{c}</td>
          <td class="count">{i}</td>
          <td class="count">{m}</td>
          <td class="pct">{_pct(c, t)}%</td>
        </tr>"""

    gap_items = ""
    sorted_gaps = sorted(rd.gaps, key=_severity_order)[:20]
    for g in sorted_gaps:
        sev = g.get("severity", "low")
        sev_class = f"severity-{sev}"
        gap_items += f"""
      <div class="gap-item {sev_class}">
        <span class="gap-severity">{sev.upper()}</span>
        <span class="gap-type">{g.get('gap_type', '').replace('_', ' ')}</span>
        <p class="gap-desc">{_escape(g.get('description', ''))}</p>
      </div>"""

    top_five_items = ""
    for q in top_five:
        cls = q.get("ddc_class", "MISSING")
        cls_lower = cls.lower()
        question_text = _escape(q.get("question", ""))
        persona = q.get("persona", "")
        source = q.get("source", "")
        label = persona if persona else source
        top_five_items += f"""
      <div class="question-item {cls_lower}">
        <span class="q-badge {cls_lower}">{cls}</span>
        <span class="q-label">{label}</span>
        <p class="q-text">{question_text}</p>
      </div>"""

    question_rows = ""
    for i, q in enumerate(rd.questions, 1):
        cls = q.get("ddc_class", "MISSING")
        cls_lower = cls.lower()
        persona = q.get("persona", "")
        source = q.get("source", "")
        label = persona if persona else source
        question_rows += f"""
        <tr class="{cls_lower}-row">
          <td class="count">{i}</td>
          <td><span class="badge {cls_lower}">{cls}</span></td>
          <td class="q-source">{label}</td>
          <td>{_escape(q.get('question', ''))}</td>
          <td class="count">{q.get('entities_retrieved', 0)}</td>
          <td class="count">{len(q.get('gaps', []))}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_escape(title)}</title>
<style>
:root {{
  --bg: #0f1117;
  --surface: #161922;
  --surface-raised: #1e2130;
  --border: rgba(255,255,255,0.08);
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --text-faint: #64748b;
  --clean: #22c55e;
  --clean-bg: rgba(34,197,94,0.15);
  --incomplete: #f59e0b;
  --incomplete-bg: rgba(245,158,11,0.15);
  --missing: #ef4444;
  --missing-bg: rgba(239,68,68,0.15);
  --font-body: system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}}
[data-theme="light"] {{
  --bg: #fafafa;
  --surface: #ffffff;
  --surface-raised: #f5f5f5;
  --border: rgba(0,0,0,0.1);
  --text: #1e293b;
  --text-muted: #64748b;
  --text-faint: #94a3b8;
  --clean-bg: rgba(34,197,94,0.1);
  --incomplete-bg: rgba(245,158,11,0.1);
  --missing-bg: rgba(239,68,68,0.1);
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.6;
  padding: 0;
}}
.container {{
  max-width: 960px;
  margin: 0 auto;
  padding: 40px 24px;
}}
header {{
  border-bottom: 2px solid var(--border);
  padding-bottom: 24px;
  margin-bottom: 32px;
}}
header h1 {{
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}}
header .subtitle {{
  color: var(--text-muted);
  font-size: 14px;
}}
.theme-toggle {{
  position: fixed;
  top: 16px;
  right: 16px;
  background: var(--surface-raised);
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 6px 12px;
  cursor: pointer;
  font-size: 13px;
  border-radius: 0;
}}
h2 {{
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  margin-top: 40px;
  color: var(--text);
}}
h2:first-of-type {{ margin-top: 0; }}

/* Score cards */
.score-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}}
.score-card {{
  background: var(--surface);
  border: 2px solid var(--border);
  padding: 20px;
}}
.score-card .number {{
  font-size: 36px;
  font-weight: 700;
  font-family: var(--font-mono);
}}
.score-card .pct {{
  font-size: 14px;
  color: var(--text-muted);
  margin-left: 4px;
}}
.score-card .label {{
  font-size: 13px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 4px;
}}
.score-card.clean .number {{ color: var(--clean); }}
.score-card.incomplete .number {{ color: var(--incomplete); }}
.score-card.missing .number {{ color: var(--missing); }}

/* Coverage bar */
.coverage-bar {{
  height: 32px;
  display: flex;
  margin-bottom: 32px;
  border: 2px solid var(--border);
  overflow: hidden;
}}
.coverage-bar .seg {{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  font-family: var(--font-mono);
  color: #fff;
}}
.clean-bg {{ background: var(--clean); }}
.incomplete-bg {{ background: var(--incomplete); }}
.missing-bg {{ background: var(--missing); }}

/* Persona table */
table {{
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 8px;
}}
th, td {{
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
  font-size: 14px;
}}
th {{
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  font-weight: 600;
  border-bottom: 2px solid var(--border);
}}
.persona-name {{
  font-weight: 600;
  text-transform: capitalize;
}}
.bar-cell {{ width: 40%; }}
.bar-track {{
  height: 20px;
  background: var(--surface-raised);
  border: 1px solid var(--border);
}}
.bar-fill {{ height: 100%; transition: width 0.3s; }}
.pct {{
  font-family: var(--font-mono);
  font-weight: 600;
  text-align: right;
  width: 60px;
}}
.count {{
  font-family: var(--font-mono);
  text-align: center;
  color: var(--text-muted);
}}

/* Top unanswered */
.question-item {{
  background: var(--surface);
  border: 2px solid var(--border);
  padding: 16px;
  margin-bottom: 8px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex-wrap: wrap;
}}
.q-badge, .badge {{
  display: inline-block;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 700;
  font-family: var(--font-mono);
  letter-spacing: 0.05em;
  flex-shrink: 0;
}}
.q-badge.missing, .badge.missing {{ background: var(--missing-bg); color: var(--missing); border: 1px solid var(--missing); }}
.q-badge.incomplete, .badge.incomplete {{ background: var(--incomplete-bg); color: var(--incomplete); border: 1px solid var(--incomplete); }}
.q-badge.clean, .badge.clean {{ background: var(--clean-bg); color: var(--clean); border: 1px solid var(--clean); }}
.q-label {{
  font-size: 12px;
  color: var(--text-faint);
  flex-shrink: 0;
  padding-top: 3px;
}}
.q-text {{
  flex: 1 1 100%;
  margin-top: 4px;
}}
.q-source {{
  font-size: 13px;
  color: var(--text-muted);
}}

/* Question table */
.missing-row {{ background: var(--missing-bg); }}
.incomplete-row {{ background: var(--incomplete-bg); }}

/* Gaps */
.gap-item {{
  background: var(--surface);
  border: 2px solid var(--border);
  border-left: 4px solid var(--text-faint);
  padding: 12px 16px;
  margin-bottom: 6px;
}}
.gap-item.severity-high {{ border-left-color: var(--missing); }}
.gap-item.severity-medium {{ border-left-color: var(--incomplete); }}
.gap-item.severity-low {{ border-left-color: var(--text-faint); }}
.gap-severity {{
  font-size: 11px;
  font-weight: 700;
  font-family: var(--font-mono);
  margin-right: 8px;
}}
.gap-type {{
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
}}
.gap-desc {{
  margin-top: 4px;
  font-size: 14px;
}}

/* Layer table */
.layer-table td:first-child {{
  text-transform: capitalize;
  font-weight: 600;
}}

/* Footer */
footer {{
  margin-top: 48px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
  color: var(--text-faint);
  font-size: 12px;
}}

@media (max-width: 640px) {{
  .score-grid {{ grid-template-columns: 1fr; }}
  .bar-cell {{ width: 30%; }}
}}
</style>
</head>
<body>
<button class="theme-toggle" onclick="toggleTheme()">Toggle theme</button>
<div class="container">

<header>
  <h1>{_escape(title)}</h1>
  <div class="subtitle">Generated by Context Blocks &middot; {rd.total} questions evaluated</div>
</header>

<h2>Coverage Overview</h2>
<div class="score-grid">
  <div class="score-card clean">
    <div><span class="number">{rd.clean}</span><span class="pct">({clean_pct}%)</span></div>
    <div class="label">Clean &mdash; answerable from KB</div>
  </div>
  <div class="score-card incomplete">
    <div><span class="number">{rd.incomplete}</span><span class="pct">({incomplete_pct}%)</span></div>
    <div class="label">Incomplete &mdash; partial coverage</div>
  </div>
  <div class="score-card missing">
    <div><span class="number">{rd.missing}</span><span class="pct">({missing_pct}%)</span></div>
    <div class="label">Missing &mdash; not in KB</div>
  </div>
</div>

<div class="coverage-bar">
  <div class="seg clean-bg" style="width:{clean_pct}%">{clean_pct}%</div>
  <div class="seg incomplete-bg" style="width:{incomplete_pct}%">{incomplete_pct}%</div>
  <div class="seg missing-bg" style="width:{missing_pct}%">{missing_pct}%</div>
</div>

<h2>Coverage by Persona</h2>
<table>
  <thead><tr>
    <th>Persona</th>
    <th>Coverage</th>
    <th>CLEAN</th>
    <th>Score</th>
  </tr></thead>
  <tbody>{persona_rows}
  </tbody>
</table>

<h2>Coverage by Knowledge Layer</h2>
<table class="layer-table">
  <thead><tr>
    <th>Layer</th>
    <th>Clean</th>
    <th>Incomplete</th>
    <th>Missing</th>
    <th>CLEAN %</th>
  </tr></thead>
  <tbody>{layer_rows}
  </tbody>
</table>

<h2>Top Unanswered Questions</h2>
<p style="color:var(--text-muted);font-size:13px;margin-bottom:12px">
  Questions your AI agents cannot fully answer from the current knowledge base.
</p>
{top_five_items if top_five_items else '<p style="color:var(--text-muted)">All questions are fully answerable.</p>'}

<h2>Knowledge Gaps Detected</h2>
{gap_items if gap_items else '<p style="color:var(--text-muted)">No structural gaps detected.</p>'}

<h2>All Questions</h2>
<table>
  <thead><tr>
    <th>#</th>
    <th>Class</th>
    <th>Source</th>
    <th>Question</th>
    <th>Entities</th>
    <th>Gaps</th>
  </tr></thead>
  <tbody>{question_rows}
  </tbody>
</table>

<footer>
  Generated by <strong>Context Blocks</strong> &mdash; gap analysis for AI agents
</footer>

</div>
<script>
function toggleTheme() {{
  const html = document.documentElement;
  html.dataset.theme = html.dataset.theme === 'light' ? 'dark' : 'light';
}}
</script>
</body>
</html>"""


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_report(eval_json: Path, output_path: Path, block_name: str = "") -> dict:
    rd = load_eval_results(eval_json)
    html = generate_html(rd, block_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return {
        "total": rd.total,
        "clean": rd.clean,
        "incomplete": rd.incomplete,
        "missing": rd.missing,
        "personas": len(rd.per_persona),
        "gaps": len(rd.gaps),
        "output": str(output_path),
    }

from __future__ import annotations

from pathlib import Path

from ..scenario_library import load_scenario_files


ROOT = Path(__file__).resolve().parents[3]
PREVIEW_DIR = ROOT / "demo-kit" / "preview_assets"


def write_preview(name: str, title: str, body: list[str]) -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    y = 40
    for index, line in enumerate(body):
        lines.append(f'<text x="28" y="{y + index * 34}" fill="#d9e8ff" font-size="20">{line}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="0 0 1200 700">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1b2a" />
      <stop offset="100%" stop-color="#102a43" />
    </linearGradient>
  </defs>
  <rect width="1200" height="700" rx="32" fill="url(#g)"/>
  <rect x="24" y="24" width="1152" height="652" rx="28" fill="none" stroke="#38bdf8" stroke-width="2" opacity="0.55"/>
  <text x="28" y="68" fill="#ffffff" font-size="34" font-weight="700">{title}</text>
  {''.join(lines)}
</svg>'''
    (PREVIEW_DIR / name).write_text(svg)


def main() -> None:
    scenarios = load_scenario_files()
    write_preview("voice_workspace_preview.svg", "Voice Workspace", [scenarios[0].title, "live transcript rail", "escalation lane", "handoff packet", "QA score preview"])
    write_preview("supervisor_board_preview.svg", "Supervisor Board", ["total calls", "active calls", "escalated calls", "intent mix", "quality trend"])
    write_preview("call_review_preview.svg", "Call Review", ["call summary", "redacted transcript", "timeline", "QA score", "export"])
    write_preview("escalation_queue_preview.svg", "Escalation Queue", ["priority", "recommended queue", "handoff packet", "resolution action"])


if __name__ == "__main__":
    main()

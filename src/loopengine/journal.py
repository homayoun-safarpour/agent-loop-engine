"""Append-only journal: the loop's memory between ticks.

Every tick writes one entry. History is never rewritten — the same rule as a
lab notebook. When an agent (or a human) wants to know why the project is in
its current state, the journal answers without any chat-log archaeology.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from loopengine.decide import Decision
from loopengine.gates import GateResult


def append_entry(
    journal_path: str | Path,
    decision: Decision,
    gate_results: list[GateResult],
    now: datetime | None = None,
) -> str:
    """Append one tick entry to the journal file and return the entry text."""
    now = now or datetime.now()
    path = Path(journal_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    gates_line = (
        ", ".join(f"{r.gate.name}={'PASS' if r.passed else 'FAIL'}" for r in gate_results)
        or "none"
    )
    entry = (
        f"\n## {now.strftime('%Y-%m-%d %H:%M')}\n"
        f"- gates: {gates_line}\n"
        f"- decision: **{decision.action}** -> {decision.target}\n"
        f"- reason: {decision.reason}\n"
    )
    if not path.exists():
        path.write_text("# Loop journal (append-only)\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
    return entry

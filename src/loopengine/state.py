"""Parse the loop state file: a plain-markdown backlog any human can edit.

The state file is deliberately markdown, not a database. If the human operator
cannot read and edit the queue with zero tooling, the queue dies the first week
the tooling breaks. Markdown checkboxes survive everything.

Item grammar, one line each:

    - [ ] A5 Publish to PyPI (cost: M) (touched: 2026-08-03)
    - [x] A1 Package scaffold (cost: L)

Cost is S, M, or L. `touched` is the last date anyone moved the item.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

_ITEM_RE = re.compile(
    r"^- \[(?P<done>[ xX])\]\s+(?P<title>.+?)"
    r"(?:\s+\(cost:\s*(?P<cost>[SML])\))?"
    r"(?:\s+\(touched:\s*(?P<touched>\d{4}-\d{2}-\d{2})\))?\s*$"
)

COST_ORDER = {"S": 0, "M": 1, "L": 2}


@dataclass
class BacklogItem:
    title: str
    done: bool
    cost: str = "M"
    touched: date | None = None

    def days_stale(self, today: date) -> int | None:
        """Days since the item was last touched; None when never dated."""
        if self.touched is None:
            return None
        return (today - self.touched).days


@dataclass
class LoopState:
    items: list[BacklogItem] = field(default_factory=list)

    @property
    def open_items(self) -> list[BacklogItem]:
        return [i for i in self.items if not i.done]

    @property
    def done_items(self) -> list[BacklogItem]:
        return [i for i in self.items if i.done]


def parse_state(text: str) -> LoopState:
    """Parse backlog checkbox lines out of a markdown state file.

    Non-item lines (headings, prose, tables) are ignored, so the state file
    can double as human documentation.
    """
    items: list[BacklogItem] = []
    for line in text.splitlines():
        m = _ITEM_RE.match(line.strip())
        if not m:
            continue
        touched = m.group("touched")
        items.append(
            BacklogItem(
                title=m.group("title").strip(),
                done=m.group("done").lower() == "x",
                cost=m.group("cost") or "M",
                touched=date.fromisoformat(touched) if touched else None,
            )
        )
    return LoopState(items=items)

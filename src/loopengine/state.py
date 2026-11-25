"""Parse the loop state file: a plain-markdown backlog any human can edit.

The state file is deliberately markdown, not a database. If the human operator
cannot read and edit the queue with zero tooling, the queue dies the first week
the tooling breaks. Markdown checkboxes survive everything.

Item grammar, one line each:

    - [ ] A5 Publish to PyPI (cost: M) (touched: 2026-08-03)
    - [x] A1 Package scaffold (cost: L)

Cost is S, M, or L. `touched` is the last date anyone moved the item. The
bullet may be `-`, `*`, `+` or a number (`1.` or `1)`), and the two tags may
come in either order. A checkbox line that cannot be read raises StateError,
so a typo never makes an item vanish from the queue.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

_BULLET = r"(?:[-*+]|\d+[.)])"
_CHECKBOX_RE = re.compile(rf"^{_BULLET}\s+\[[ xX]?\]")
_ITEM_RE = re.compile(rf"^{_BULLET}\s+\[(?P<done>[ xX])\]\s+(?P<rest>\S.*?)\s*$")
_TAG_RE = re.compile(r"\s+\((?P<key>cost|touched):\s*(?P<value>[^()]*?)\s*\)$")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

COST_ORDER = {"S": 0, "M": 1, "L": 2}


class StateError(ValueError):
    """A backlog line in the state file cannot be read."""


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
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not _CHECKBOX_RE.match(line):
            continue
        m = _ITEM_RE.match(line)
        if not m:
            raise StateError(f"line {lineno}: cannot read backlog item: {line}")
        items.append(_parse_item(m.group("done"), m.group("rest"), lineno, line))
    return LoopState(items=items)


def _parse_item(done: str, rest: str, lineno: int, line: str) -> BacklogItem:
    """Strip the trailing (cost: ...) and (touched: ...) tags, in any order."""
    tags: dict[str, str] = {}
    while tag := _TAG_RE.search(rest):
        key = tag.group("key")
        if key in tags:
            raise StateError(f"line {lineno}: tag '{key}' given twice: {line}")
        tags[key] = tag.group("value")
        rest = rest[: tag.start()]
    cost = tags.get("cost", "M")
    if cost not in COST_ORDER:
        raise StateError(f"line {lineno}: cost must be S, M or L, not '{cost}': {line}")
    touched = None
    if "touched" in tags:
        value = tags["touched"]
        try:
            if not _DATE_RE.fullmatch(value):
                raise ValueError("want YYYY-MM-DD")
            touched = date.fromisoformat(value)
        except ValueError as exc:
            raise StateError(f"line {lineno}: bad touched date '{value}' ({exc}): {line}") from exc
    return BacklogItem(title=rest.strip(), done=done.lower() == "x", cost=cost, touched=touched)

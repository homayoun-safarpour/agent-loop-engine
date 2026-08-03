"""The decision policy: given state and gate results, pick ONE bounded action.

The policy is small on purpose. It encodes three rules for keeping a
long-running agent-driven project alive, in priority order:

1. REPAIR beats progress. A red gate means the next action is fixing it,
   never new work. (New work on a broken base multiplies the repair cost.)
2. MOMENTUM beats order. When the head of the backlog has been stale for
   more than `stale_days`, take the cheapest open item instead of the next
   one. A moving loop survives; a stuck loop dies waiting for its hardest item.
3. One action per tick. The output is a single item, sized for one session,
   so a failed session costs one increment and never the whole day.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from loopengine.gates import GateResult
from loopengine.state import COST_ORDER, BacklogItem, LoopState


@dataclass
class Decision:
    action: str  # "repair" | "advance" | "unstick" | "close"
    reason: str
    target: str


def decide(
    state: LoopState,
    gate_results: list[GateResult],
    today: date,
    stale_days: int = 2,
) -> Decision:
    """Pick exactly one action for this tick."""
    failed = [r for r in gate_results if not r.passed]
    if failed:
        first = failed[0]
        return Decision(
            action="repair",
            reason=f"gate '{first.gate.name}' is red; no new work on a broken base",
            target=first.gate.name,
        )

    open_items = state.open_items
    if not open_items:
        return Decision(
            action="close",
            reason="backlog is empty; close this cycle and propose the next one",
            target="cycle",
        )

    head = open_items[0]
    head_stale = head.days_stale(today)
    if head_stale is not None and head_stale > stale_days:
        cheapest = _cheapest(open_items)
        if cheapest.title != head.title:
            return Decision(
                action="unstick",
                reason=(
                    f"head item stale {head_stale}d (> {stale_days}d); "
                    "momentum beats order, taking the cheapest open item"
                ),
                target=cheapest.title,
            )

    return Decision(
        action="advance",
        reason="gates green and head item fresh; take the next open item",
        target=head.title,
    )


def _cheapest(items: list[BacklogItem]) -> BacklogItem:
    return min(items, key=lambda i: COST_ORDER.get(i.cost, 1))

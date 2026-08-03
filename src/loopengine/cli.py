"""CLI: `loop-engine tick` runs one full loop iteration.

Read state -> run gates -> decide one action -> journal it -> print the order.
The engine never executes the backlog item itself; it tells the operator
(human or agent) exactly what the next bounded action is and why.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from loopengine.decide import decide
from loopengine.gates import Gate, run_gates
from loopengine.journal import append_entry
from loopengine.state import parse_state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="loop-engine")
    sub = parser.add_subparsers(dest="cmd", required=True)

    tick = sub.add_parser("tick", help="run one loop iteration")
    tick.add_argument("--state", default="LOOP_STATE.md", help="path to the markdown state file")
    tick.add_argument("--journal", default="journal/JOURNAL.md", help="append-only journal path")
    tick.add_argument(
        "--gate",
        action="append",
        default=[],
        metavar="NAME=COMMAND",
        help="quality gate, repeatable, e.g. --gate tests='pytest -q'",
    )
    tick.add_argument("--stale-days", type=int, default=2)
    tick.add_argument("--json", action="store_true", help="print the decision as JSON")

    args = parser.parse_args(argv)

    state_path = Path(args.state)
    if not state_path.exists():
        print(f"state file not found: {state_path}", file=sys.stderr)
        return 2

    state = parse_state(state_path.read_text(encoding="utf-8"))
    gates = []
    for spec in args.gate:
        name, _, command = spec.partition("=")
        if not command:
            print(f"bad --gate spec (want NAME=COMMAND): {spec}", file=sys.stderr)
            return 2
        gates.append(Gate(name=name, command=command))

    results = run_gates(gates)
    decision = decide(state, results, today=date.today(), stale_days=args.stale_days)
    append_entry(args.journal, decision, results)

    if args.json:
        print(
            json.dumps(
                {"action": decision.action, "target": decision.target, "reason": decision.reason}
            )
        )
    else:
        print(f"action : {decision.action}")
        print(f"target : {decision.target}")
        print(f"reason : {decision.reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

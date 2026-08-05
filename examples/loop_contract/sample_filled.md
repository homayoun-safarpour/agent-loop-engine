# Loop Contract  -  filled sample (this repository)

This is how `agent-loop-engine` itself is operated. Copy the blank template for new work; treat this as a reference, not a second source of truth.

## 1. Done

**Objective signal that means finished:**

```
All backlog items in LOOP_STATE.md checked; pytest -q and ruff check src tests both exit 0 on the last tick.
```

## 2. Verifier

**What checks the work that did not produce it:**

```
Quality gates before every decision:
  tests = python -m pytest -q
  lint  = python -m ruff check src tests
The decision policy never advances while a gate is red
(tests/test_decide.py::test_a_red_gate_always_beats_new_work).
```

## 3. Stop layers

| Layer | Your rule |
| --- | --- |
| Goal / done check | No open checkboxes left in `LOOP_STATE.md` → `close` |
| Max turns or ticks | One bounded action per `loop-engine tick` |
| Budget (tokens / $ / wall clock) | No LLM in the decision path; operator budget is external |
| No-progress rule | Head item stale >2 days loses priority to cheapest open item (`unstick`) |

## 4. State file

**Path to durable backlog / progress on disk:**

```
LOOP_STATE.md
examples/LOOP_STATE.md  (worked example)
```

**Journal / audit trail:**

```
examples/journal/JOURNAL.md  (append-only tick journal)
git history for code changes
```

## 5. Irreversible

**Actions that require a human yes before the loop may proceed:**

```
Force-push, deleting releases, publishing secrets, unpaid cloud spend.
The engine never executes backlog work; it only prints the next order.
```

## Loop type (pick one primary)

- [ ] Turn-based
- [x] Goal-based (backlog + gates define done)
- [ ] Time-based
- [ ] Proactive

## Operator

Who executes the bounded action after the decision?

- [x] Mix (describe): Human or coding agent executes the printed order; CI re-runs gates.

## Notes

```
Deterministic core: no LLM dependency in loopengine.
Sibling gates (optional): judge-drift-sentinel, trace-gate as exit 0/2 commands.
See docs/FIELD_GUIDE.md for the source synthesis behind this contract.
```

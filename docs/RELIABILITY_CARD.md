# Reliability card — agent-loop-engine

| Field | Value |
| --- | --- |
| **Job** | Choose one safe next action for long agent/human work sessions |
| **Primary signal** | Shell gate exit codes + markdown backlog state + journal |
| **Named decisions** | `repair` > `unstick` > `advance` > `close` |
| **Fixtures** | `examples/LOOP_STATE.md`, `examples/loop_contract/`, `examples/journal/JOURNAL.md` |
| **Central test** | `tests/test_decide.py::test_a_red_gate_always_beats_new_work` |
| **Runtime deps for core claim** | stdlib only; **no LLM dependency** in the decision layer |
| **Claim** | Repair-before-advance is enforceable and unit-testable outside the chat window |
| **Not claimed** | Replaces the agent/model; picks task content; guarantees product quality without good gates |

## Field alignment (not affiliation)

Same instinct as eval-driven / production loops (DSPy metrics, LangSmith gates, agent trajectory checks):
**policy that cannot fail a test is not a gate.** Pair with `trace-gate` and `judge-drift-sentinel` as gate commands.

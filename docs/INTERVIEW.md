# Interview talking points : agent-loop-engine

Five CLI-backed points for a technical screen (no resume recap).

- **`loop-engine tick --gate "tests=python -m pytest -q"`** : gates are arbitrary shell commands with exit codes; the engine never runs backlog work itself, it only reports what is safe next.
- **Red gate -> `action: repair`** : when lint or tests fail, decision is always repair (see `tests/test_decide.py::test_a_red_gate_always_beats_new_work`); run the worked example in the README with `--gate "lint=python -m ruff check src tests"`.
- **`--stale-days 2` unstick policy** : if the backlog head is untouched longer than the threshold, `decide` picks a cheaper open item so the loop does not freeze on one hard task.
- **`--json` for automation** : same tick prints `{"action","target","reason"}` for cron, CI wrappers, or an operator agent that only executes the printed order.
- **Journal at `--journal journal/JOURNAL.md`** : every tick appends gate results and the decision so the next session reads project state without chat archaeology (see `examples/journal/JOURNAL.md`).

## Related instruments

- [agent-loop-field-guide](https://github.com/homayoun-safarpour/agent-loop-field-guide) - fill the Loop Contract before you automate
- [judge-field-guide](https://github.com/homayoun-safarpour/judge-field-guide) - CI-tested map of the LLM-judge ecosystem
- [judge-drift-sentinel](https://github.com/homayoun-safarpour/judge-drift-sentinel) - plug as `--gate "drift=..."` for JUDGE_DRIFT fail-closed; history fixture under `examples/drifting/`



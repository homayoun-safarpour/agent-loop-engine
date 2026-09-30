# agent-loop-engine — live project state

Engineering backlog for this repository. The product loop journals ticks in
`journal/JOURNAL.md` when you run it against this file.

- [ ] B1 `loop-engine init` scaffolds LOOP_STATE.md + journal in any repo (cost: S) (touched: 2026-08-03)
- [ ] B2 `--commit` flag: auto-commit state + journal after a tick (cost: M) (touched: 2026-08-03)
- [ ] B3 GitHub Actions example: nightly tick posts the order as an issue (cost: M)
- [ ] B4 `close` action generates a cycle report from the journal (cost: M)
- [ ] B5 Publish to PyPI so `pip install agent-loop-engine` is true (cost: M)
- [ ] B6 Docs: wiring an LLM agent to execute the tick order (cost: S)

## BENCHMARK GATE (week of 2026-09-29, restyle)

Focus: first-screen restyle only. No new public repo this week.

| # | Check | Status 2026-09-30 |
| --- | --- | --- |
| 1 | CI 3.10/3.11/3.12 | existing workflow; recheck after this push |
| 2 | Named claim tests | `tests/test_readme.py::test_readme_first_screen_matches_top100_craft` plus `test_a_red_gate_always_beats_new_work` |
| 3 | Worked example | README first screen is the live red-gate output from `examples/fail_gate.py` |
| 4 | Fork / implement <30 min | clone, `pip install -e .`, one tick |
| 5 | `public_git_guard.py` | run before push |
| 6 | AI-tell README | first screen has no em-dash, no interview pack |
| 7 | Interview pack | `docs/INTERVIEW.md` (below the first screen) |

NEXT TICK: trace-gate first screen (clone + fail-closed check before interview links).

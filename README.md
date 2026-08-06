# agent-loop-engine

**Agent loops keep adding features while pytest is red and the hardest backlog item stalls for days—because chat prompts cannot enforce a verifiable "repair before advance" rule. One `loop-engine tick` runs your shell gates and prints a single bounded order plus an append-only journal.**

[![CI](https://github.com/homayoun-safarpour/agent-loop-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/homayoun-safarpour/agent-loop-engine/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## The problem

An agent (or a human) working a multi-week project session by session keeps making the same three mistakes:

| Failure | What it looks like | What it costs |
|---|---|---|
| New work on a broken base | Tests are red, agent adds a feature anyway | Every later change multiplies the repair cost |
| Stalling on the hardest item | Backlog head untouched for a week, nothing else moves either | The loop dies waiting for its worst task |
| No memory between sessions | "Why is the project in this state?" requires chat-log archaeology | Decisions get re-made, work gets re-done |

Schedulers run tasks on time. They do not decide *which* task is safe to run. That decision layer is what is missing, and it is small enough to be testable.

## The insight

One tick, four steps, one bounded action out:

```
read state (markdown backlog, human-editable)
        |
run quality gates (pytest, ruff, anything with an exit code)
        |
decide ONE action:   repair > unstick > advance > close
        |
journal it (append-only) and hand the order to the operator
```

The decision policy is three rules in priority order: **repair beats progress** (a red gate blocks all new work), **momentum beats order** (a head item stale >2 days loses its turn to the cheapest open item), and **one action per tick** (a failed session costs one increment, never the day).

## Install

```bash
pip install git+https://github.com/homayoun-safarpour/agent-loop-engine
# or from source
git clone https://github.com/homayoun-safarpour/agent-loop-engine && cd agent-loop-engine && pip install -e .
```

## Quickstart

Your project state is a markdown file anyone can edit with zero tooling:

```markdown
- [x] M1 Baseline model training script with fixed seed (cost: M) (touched: 2026-08-01)
- [ ] M2 Add evaluation harness with held-out split (cost: L) (touched: 2026-08-01)
- [ ] M3 Wire ruff + pytest into pre-commit (cost: S) (touched: 2026-08-02)
```

Run one tick with your gates:

```bash
loop-engine tick --state LOOP_STATE.md \
  --gate "tests=pytest -q" \
  --gate "lint=ruff check src tests"
```

For a third gate pattern (`types` / mypy) plus a sample journal REPAIR block, see
[`examples/LOOP_STATE.md`](examples/LOOP_STATE.md).

The engine prints exactly one order and why. It never executes the backlog item itself. It tells the operator (human, cron job, or LLM agent) what the next bounded action is.

## Field guide

Prompting alone fails on long work when memory is only a chat window and "done" is whatever the model claims. Use the standalone **[agent-loop-field-guide](https://github.com/homayoun-safarpour/agent-loop-field-guide)** (copy `templates/LOOP_CONTRACT.md` into your project before you automate). A copy also lives here under [`docs/FIELD_GUIDE.md`](docs/FIELD_GUIDE.md) and [`examples/loop_contract/`](examples/loop_contract/).

## What is in the box

| Module | What it does | Use it when |
|---|---|---|
| `loopengine.state` | Parses the markdown backlog (checkboxes, cost, staleness) | You want a queue humans can edit in any editor |
| `loopengine.gates` | Runs shell-command quality gates, captures pass/fail | Anything with an exit code should block bad work |
| `loopengine.decide` | The 3-rule decision policy, fully unit-tested | You need "which task is *safe*", not "which task is next" |
| `loopengine.journal` | Append-only tick journal | The project must explain its own history |
| `loopengine.cli` | `loop-engine tick`, plain or `--json` output | Wiring the loop into cron, CI, or an agent prompt |

## Worked example (real output)

This repository ran the engine on itself during its own first build. First tick: the lint gate was genuinely red:

```
$ loop-engine tick --state examples/LOOP_STATE.md --gate "tests=python -m pytest -q" --gate "lint=python -m ruff check src tests"
action : repair
target : lint
reason : gate 'lint' is red; no new work on a broken base
```

After fixing lint, the same command:

```
action : advance
target : M2 Add evaluation harness with held-out split
reason : gates green and head item fresh; take the next open item
```

The append-only journal it produced (`examples/journal/JOURNAL.md`):

```markdown
## 2026-08-03 20:13
- gates: tests=PASS, lint=FAIL
- decision: **repair** -> lint
- reason: gate 'lint' is red; no new work on a broken base

## 2026-08-03 20:15
- gates: tests=PASS, lint=PASS
- decision: **advance** -> M2 Add evaluation harness with held-out split
- reason: gates green and head item fresh; take the next open item
```

## Why this exists

Long-running agent projects fail on policy, not on capability. The agent often knows *how* to do tasks and still has no tested rule for *which* task is safe next. Encoding that policy in prompts drifts and cannot be unit-tested. So the policy became a package: three rules, sixteen tests (`tests/test_decide.py::test_a_red_gate_always_beats_new_work` is the central claim), and an append-only journal any session can read to reconstruct state.

## Design commitments

- **No LLM dependency.** The engine decides; whatever executes can be a human, cron, or an agent. Decision logic must be deterministic and testable.
- **Zero runtime dependencies.** Standard library only.
- **Human-editable state.** Markdown checkboxes, not a database. If the tooling breaks, the queue survives.
- **Every claim above is a test.** The central one: `tests/test_decide.py::test_a_red_gate_always_beats_new_work`.

## Contributing

Issues and PRs welcome. Run `pytest -q` and `ruff check src tests` before pushing. The engine itself will tell you the same thing on the next tick.

## Citation

```bibtex
@software{safarpour2026agentloopengine,
  author = {Homayoun Safarpour},
  title  = {agent-loop-engine: a self-advancing loop for AI agents},
  year   = {2026},
  url    = {https://github.com/homayoun-safarpour/agent-loop-engine}
}
```

Author: Homayoun Safarpour Â· [LinkedIn](https://www.linkedin.com/in/homayoun-safarpour/)

## License

MIT

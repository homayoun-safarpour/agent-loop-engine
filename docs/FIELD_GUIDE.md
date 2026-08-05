# Field guide: designing agent loops that stop for the right reasons

**Long work fails when the only memory is a chat window and the only stop condition is "the model feels done." This guide turns five high-signal sources into a short contract you can fill before you run a loop  -  then maps that contract onto `loop-engine tick` and exit-code gates.**

This is not a framework. It is a checklist plus attribution. The runnable policy lives in this repository.

## Sources (read these; we paraphrase, we do not copy)

| # | Source | What it contributes |
| --- | --- | --- |
| 1 | [Anthropic  -  Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflows vs agents; evaluator-optimizer; keep designs simple; invest in tool interfaces (ACI) |
| 2 | [Anthropic  -  Loop engineering](https://claude.com/blog/getting-started-with-loops) | Turn / goal / time / proactive loops; verifiable stop criteria; skills as repeatable checks |
| 3 | [Simon Willison  -  Designing agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) | Agent = tools in a loop toward a goal; sandbox; tests amplify agent value |
| 4 | [cobusgreyling/loop-engineering](https://github.com/cobusgreyling/loop-engineering) | High-star open patterns for loop readiness, audit, and durable orchestration culture |
| 5 | [Ralph pattern](https://ghuntley.com/ralph/) / [ralph-copilot](https://github.com/giocaizzi/ralph-copilot) + [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | Filesystem + git as memory; fresh context; harness around the model; reviewer separate from maker |

Honest boundary: those projects are larger than this package. This guide extracts **shared rules that survive across them**, then shows how this engine implements a small, testable slice.

## What the best sources agree on

1. **Start simple.** Add multi-step loops only when a metric says the simpler path fails (Anthropic).
2. **Done must be machine-checkable.** Tests, scores, exit codes  -  not "the model decided it was finished" (Anthropic loops + Willison).
3. **Verifier is not the maker.** A separate check, second agent, or deterministic gate reviews the result (evaluator-optimizer + loop practice).
4. **Durable state lives on disk.** Markdown / JSON / git beat chat logs for multi-session work (Ralph + harness culture + `LOOP_STATE.md` here).
5. **Stop in layers.** Goal met, max turns, budget, and no-progress  -  together, not one alone.
6. **Tool interfaces matter.** Absolute paths, clear args, scripts for deterministic steps (Anthropic tool appendix).
7. **Humans before irreversible actions.** Delete, force-push, spend, or production write needs an explicit checkpoint.

## Loop types (when to use which)

From Anthropic's loop engineering framing, compressed into operator language:

| Loop | You hand off | Use when | Stop signal |
| --- | --- | --- | --- |
| Turn-based | The verification check | Exploring or deciding | Human accepts the turn, or a skill/gate fails |
| Goal-based | The definition of done | You can write a pass/fail criterion | Goal met or turn/budget cap |
| Time-based | The trigger | Recurring work, external systems | Interval cancelled or queue empty |
| Proactive | The prompt + schedule | Well-defined streams (triage, CI fix) | Per-task goal + routine off switch |

Use the smallest loop that matches the work. A cron that re-prompts without a verifier is not a production loop.

## The five-decision Loop Contract

Before you automate, write these five decisions down. Blank template: [`examples/loop_contract/LOOP_CONTRACT.md`](../examples/loop_contract/LOOP_CONTRACT.md). Filled sample: [`examples/loop_contract/sample_filled.md`](../examples/loop_contract/sample_filled.md).

| # | Decision | Question you must answer |
| --- | --- | --- |
| 1 | **Done** | What objective signal means finished? (command, exit code, score threshold) |
| 2 | **Verifier** | What checks the work that did **not** produce it? |
| 3 | **Stop layers** | Goal check + max turns/ticks + budget and/or no-progress rule |
| 4 | **State file** | Where does progress live on disk so a crash can resume? |
| 5 | **Irreversible** | What requires a human yes before the loop may proceed? |

If any cell is empty, you are still prompting, not looping.

## Filesystem and git as memory

Chat context rot is real. Patterns that keep winning put durable artifacts in the repo:

- A human-editable backlog (`LOOP_STATE.md` here)
- An append-only journal of decisions
- Git commits as the audit trail for code changes
- Fresh context per iteration when the previous window is polluted (Ralph-style)

This engine implements the backlog + gate + one-action + journal slice. It does not replace your agent runtime; it decides **which** bounded action is safe next.

## How this maps to `agent-loop-engine`

```
Loop Contract                 This package
-------------                 ------------
Done                          your gates (pytest, ruff, sibling CLIs)
Verifier                      gates run before advance; repair beats progress
Stop layers                   one action per tick; red gate blocks new work
State file                    LOOP_STATE.md (checkbox backlog)
Irreversible                  engine never executes; operator / CI does
```

Sibling instruments that plug in as gates (exit `0` / `2`):

- [judge-drift-sentinel](https://github.com/homayoun-safarpour/judge-drift-sentinel)  -  system change vs judge drift
- [trace-gate](https://github.com/homayoun-safarpour/trace-gate)  -  trajectory regression against a frozen baseline

Central policy claim (named test): `tests/test_decide.py::test_a_red_gate_always_beats_new_work`.

## Anti-patterns

| Anti-pattern | Why it fails | Prefer |
| --- | --- | --- |
| Model is the only judge of done | Confirms its own work | Independent gate or second reviewer |
| Unbounded loop | Cost and damage grow without a stop | Turn/budget/no-progress caps |
| Relative paths in tools | Break after cwd changes | Absolute paths (Anthropic ACI lesson) |
| Memory only in chat | Cannot resume cleanly | State file + journal + git |
| New features on red tests | Compounds breakage | Repair-before-advance (this engine) |
| LLM re-derives a fixed script | Burns tokens on deterministic work | Ship a script; call it from the loop |

## Two-minute path (recruiter / stranger)

```bash
git clone https://github.com/homayoun-safarpour/agent-loop-engine
cd agent-loop-engine
pip install -e ".[dev]"   # or: pip install -e .
# 1) skim the blank contract
#    examples/loop_contract/LOOP_CONTRACT.md
# 2) run one tick on the committed example state
loop-engine tick --state examples/LOOP_STATE.md \
  --gate "tests=python -m pytest -q" \
  --gate "lint=python -m ruff check src tests"
# 3) open examples/journal/JOURNAL.md and read the decision line
```

You should see either `repair` (gate red) or `advance` / `unstick` / `close` with a one-line reason. That is the product.

## Attribution

Ideas above are synthesized from the linked Anthropic posts, Willison's essay, the loop-engineering project, and the Ralph / harness-engineering lineage. Wording here is original. Implementations in `src/loopengine/` are Homayoun Safarpour's and covered by this repository's MIT license. Upstream projects keep their own licenses; link them, do not vendor their trees into this guide.

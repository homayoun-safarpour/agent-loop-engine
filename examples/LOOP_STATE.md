# Example project state — an ML feature backlog

This file is both the demo and the documentation: the engine reads the
checkboxes below, everything else is for humans.

- [x] M1 Baseline model training script with fixed seed (cost: M) (touched: 2026-08-01)
- [ ] M2 Add evaluation harness with held-out split (cost: L) (touched: 2026-08-01)
- [ ] M3 Wire ruff + pytest into pre-commit (cost: S) (touched: 2026-08-02)
- [ ] M4 Export model card with metrics table (cost: M)

## Extra quality-gate example (docs only)

Name: `types`  
Command: `python -m mypy src`  
Pass: exit 0. Fail: any type error (exit non-zero).

Wire it beside the usual gates:

```bash
loop-engine tick --state examples/LOOP_STATE.md \
  --gate "tests=python -m pytest -q" \
  --gate "lint=python -m ruff check src tests" \
  --gate "types=python -m mypy src"
```

If `types` is red, the journal records repair-before-advance (no new backlog item):

```markdown
## 2026-08-06T12:00:00Z tick
- gates: tests=PASS, lint=PASS, types=FAIL
- decision: REPAIR
- reason: gate 'types' is red; no new work on a broken base
```

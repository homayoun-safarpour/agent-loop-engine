# Loop Contract (fill before you automate)

Copy this file into your project. Fill every section. Empty sections mean you are still prompting.

## 1. Done

**Objective signal that means finished** (command, exit code, score threshold):

```
<!-- e.g. pytest -q exits 0; Lighthouse score >= 90; drift-sentinel check exits 0 -->
```

## 2. Verifier

**What checks the work that did not produce it:**

```
<!-- e.g. pytest + ruff; second reviewer agent; trace-gate check -->
```

## 3. Stop layers

| Layer | Your rule |
| --- | --- |
| Goal / done check | |
| Max turns or ticks | |
| Budget (tokens / $ / wall clock) | |
| No-progress rule | |

## 4. State file

**Path to durable backlog / progress on disk:**

```
<!-- e.g. LOOP_STATE.md -->
```

**Journal / audit trail (if any):**

```
<!-- e.g. journal/JOURNAL.md or git history -->
```

## 5. Irreversible

**Actions that require a human yes before the loop may proceed:**

```
<!-- e.g. git push --force, rm -rf, production deploy, paid API spend above $X -->
```

## Loop type (pick one primary)

- [ ] Turn-based
- [ ] Goal-based
- [ ] Time-based
- [ ] Proactive

## Operator

Who executes the bounded action after the decision?

- [ ] Human
- [ ] CI / cron
- [ ] Coding agent
- [ ] Mix (describe):

## Notes

```
<!-- constraints, sandbox, network policy -->
```

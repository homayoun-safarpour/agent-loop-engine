# LinkedIn draft (public-safe) - loop-engine first-screen restyle 2026-09-30

Field pain first. No employer demand. No unpublished research.
Homayoun posts himself.

Paste verified 2026-09-30 on `examples/fail_gate.py`:
action : repair
target : tests
reason : gate 'tests' is red; no new work on a broken base

---

Paste block (copy from the next line to the URL):

Your agent can keep shipping while pytest is red.

That is a policy hole, not a missing model.

loop-engine reads a markdown backlog, runs your gates, and prints one next action. No LLM in the decision.

The stranger run is the red gate:

git clone https://github.com/homayoun-safarpour/agent-loop-engine
cd agent-loop-engine && pip install -e .
loop-engine tick --state examples/LOOP_STATE.md --gate "tests=python examples/fail_gate.py"

action : repair
target : tests
reason : gate 'tests' is red; no new work on a broken base

It does not execute the backlog item. It tells the operator what is safe. Green gates then advance one item and append a journal the next session can read.

The limit: it does not judge whether the work was good. It only blocks new work on a broken base.

Repo:
https://github.com/homayoun-safarpour/agent-loop-engine

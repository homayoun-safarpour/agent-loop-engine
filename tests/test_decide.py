from datetime import date

from loopengine.decide import decide
from loopengine.gates import Gate, GateResult
from loopengine.state import parse_state

TODAY = date(2026, 8, 4)


def _gates(passed: bool) -> list[GateResult]:
    return [GateResult(gate=Gate("tests", "pytest -q"), passed=passed, output="")]


def test_a_red_gate_always_beats_new_work():
    """The central claim: no new backlog work while any quality gate is red."""
    state = parse_state("- [ ] A2 Ship the feature (cost: S) (touched: 2026-08-04)")
    decision = decide(state, _gates(passed=False), today=TODAY)
    assert decision.action == "repair"
    assert decision.target == "tests"


def test_green_gates_and_fresh_head_advance_in_order():
    state = parse_state(
        "- [ ] A2 Hard head item (cost: L) (touched: 2026-08-04)\n"
        "- [ ] A3 Easy item (cost: S) (touched: 2026-08-04)"
    )
    decision = decide(state, _gates(passed=True), today=TODAY)
    assert decision.action == "advance"
    assert decision.target.startswith("A2")


def test_a_stale_head_yields_to_the_cheapest_item():
    """Momentum beats order: a head stuck >2 days loses its turn to the cheapest item."""
    state = parse_state(
        "- [ ] A2 Hard head item (cost: L) (touched: 2026-07-28)\n"
        "- [ ] A3 Easy item (cost: S) (touched: 2026-08-01)"
    )
    decision = decide(state, _gates(passed=True), today=TODAY)
    assert decision.action == "unstick"
    assert decision.target.startswith("A3")


def test_stale_head_that_is_already_cheapest_just_advances():
    state = parse_state("- [ ] A2 Only item (cost: S) (touched: 2026-07-01)")
    decision = decide(state, _gates(passed=True), today=TODAY)
    assert decision.action == "advance"


def test_empty_backlog_closes_the_cycle():
    state = parse_state("- [x] A1 Done thing (cost: S)")
    decision = decide(state, _gates(passed=True), today=TODAY)
    assert decision.action == "close"


def test_undated_head_is_never_treated_as_stale():
    state = parse_state("- [ ] A2 Head no date (cost: L)\n- [ ] A3 Easy (cost: S)")
    decision = decide(state, _gates(passed=True), today=TODAY)
    assert decision.action == "advance"

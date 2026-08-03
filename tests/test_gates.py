import sys

from loopengine.gates import Gate, run_gates

PY = sys.executable


def test_passing_gate_reports_pass():
    results = run_gates([Gate("ok", f'"{PY}" -c "print(1)"')])
    assert results[0].passed is True


def test_failing_gate_reports_fail_with_output():
    results = run_gates([Gate("bad", f'"{PY}" -c "import sys; print(\'boom\'); sys.exit(1)"')])
    assert results[0].passed is False
    assert "boom" in results[0].output


def test_gates_run_in_order_and_all_run():
    results = run_gates(
        [
            Gate("first", f'"{PY}" -c "pass"'),
            Gate("second", f'"{PY}" -c "import sys; sys.exit(1)"'),
            Gate("third", f'"{PY}" -c "pass"'),
        ]
    )
    assert [r.passed for r in results] == [True, False, True]

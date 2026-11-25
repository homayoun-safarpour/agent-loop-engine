import sys
import time

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


def test_gate_output_with_undecodable_bytes_does_not_crash():
    # Bytes that are invalid in cp1252 (0x9d) and in UTF-8 (0xff) alike.
    script = "import sys; sys.stdout.buffer.write(bytes([111, 107, 0xe2, 0x9d, 0x8c, 0xff, 10]))"
    results = run_gates([Gate("bytes", f'"{PY}" -c "{script}"')])
    assert results[0].passed is True
    assert results[0].output.startswith("ok")


def test_timeout_stops_a_hung_gate(tmp_path):
    # A compound command, so the shell cannot hand over to the child: the child
    # holds the output pipes and must be killed with the shell.
    command = f'"{PY}" -c "import time; time.sleep(30)" && "{PY}" -c "pass"'
    started = time.monotonic()
    results = run_gates([Gate("slow", command)], cwd=str(tmp_path), timeout=2)
    elapsed = time.monotonic() - started
    assert results[0].passed is False
    assert "timed out after 2s" in results[0].output
    assert elapsed < 15

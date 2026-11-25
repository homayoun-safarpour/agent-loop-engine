"""Quality gates: commands that must pass before the loop takes on new work.

A gate is any shell command with a zero/nonzero exit code (pytest, ruff, a
schema check, a citation-integrity script). The engine's rule is fixed:
no new backlog work while a gate is red. Repair comes first.
"""

from __future__ import annotations

import contextlib
import os
import signal
import subprocess
from dataclasses import dataclass


@dataclass
class Gate:
    name: str
    command: str


@dataclass
class GateResult:
    gate: Gate
    passed: bool
    output: str


def _kill_tree(proc: subprocess.Popen) -> None:
    """Kill the shell and every command it started, not only the shell."""
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True, check=False
        )
    else:
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(proc.pid, signal.SIGKILL)
    proc.kill()


def run_gates(gates: list[Gate], cwd: str | None = None, timeout: int = 600) -> list[GateResult]:
    """Run each gate command in order and capture pass/fail plus output.

    Output is read as UTF-8 with undecodable bytes replaced, so a gate that
    prints an emoji cannot crash the tick. On timeout the whole process tree
    of the gate is killed, so a hung gate cannot hold the tick open.
    """
    results: list[GateResult] = []
    for gate in gates:
        proc = subprocess.Popen(
            gate.command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
            start_new_session=os.name != "nt",
        )
        try:
            out, err = proc.communicate(timeout=timeout)
            passed = proc.returncode == 0
            output = ((out or "") + (err or "")).strip()
        except subprocess.TimeoutExpired:
            _kill_tree(proc)
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.communicate(timeout=10)
            passed = False
            output = f"timed out after {timeout}s"
        results.append(GateResult(gate=gate, passed=passed, output=output[-2000:]))
    return results

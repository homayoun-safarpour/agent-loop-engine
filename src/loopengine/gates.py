"""Quality gates: commands that must pass before the loop takes on new work.

A gate is any shell command with a zero/nonzero exit code (pytest, ruff, a
schema check, a citation-integrity script). The engine's rule is fixed:
no new backlog work while a gate is red. Repair comes first.
"""

from __future__ import annotations

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


def run_gates(gates: list[Gate], cwd: str | None = None, timeout: int = 600) -> list[GateResult]:
    """Run each gate command in order and capture pass/fail plus output."""
    results: list[GateResult] = []
    for gate in gates:
        try:
            proc = subprocess.run(
                gate.command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            passed = proc.returncode == 0
            output = (proc.stdout + proc.stderr).strip()
        except subprocess.TimeoutExpired:
            passed = False
            output = f"timed out after {timeout}s"
        results.append(GateResult(gate=gate, passed=passed, output=output[-2000:]))
    return results

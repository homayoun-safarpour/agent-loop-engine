"""agent-loop-engine: a self-advancing loop for AI agents working on long-running projects."""

from loopengine.decide import Decision, decide
from loopengine.gates import Gate, GateResult, run_gates
from loopengine.journal import append_entry
from loopengine.state import BacklogItem, LoopState, parse_state

__all__ = [
    "BacklogItem",
    "Decision",
    "Gate",
    "GateResult",
    "LoopState",
    "append_entry",
    "decide",
    "parse_state",
    "run_gates",
]

__version__ = "0.1.0"

from datetime import datetime

from loopengine.decide import Decision
from loopengine.gates import Gate, GateResult
from loopengine.journal import append_entry


def test_journal_is_append_only_and_readable(tmp_path):
    journal = tmp_path / "journal" / "JOURNAL.md"
    decision = Decision(action="advance", reason="gates green", target="A2 Ship it")
    results = [GateResult(gate=Gate("tests", "pytest -q"), passed=True, output="")]

    append_entry(journal, decision, results, now=datetime(2026, 8, 4, 7, 30))
    first = journal.read_text(encoding="utf-8")
    assert "advance" in first and "A2 Ship it" in first

    append_entry(journal, decision, results, now=datetime(2026, 8, 5, 7, 30))
    second = journal.read_text(encoding="utf-8")
    assert second.startswith(first)  # history never rewritten
    assert second.count("## 2026-08-") == 2

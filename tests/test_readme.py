import sys
from pathlib import Path

from loopengine.cli import main

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8-sig")
FAIL_GATE = ROOT / "examples" / "fail_gate.py"


def test_readme_spoken_h1_is_loop_engine():
    assert README.lstrip().startswith("# loop-engine\n")
    assert "agent-loop-engine" in README


def test_readme_first_screen_matches_top100_craft():
    pip_at = README.find("pip install")
    interview_at = README.find("Interview pack")
    problem_at = README.find("## The problem")
    assert 0 <= pip_at < interview_at
    assert 0 <= pip_at < problem_at
    head = "\n".join(README.splitlines()[:22])
    assert "# loop-engine" in head
    assert "git clone https://github.com/homayoun-safarpour/agent-loop-engine" in head
    assert "pip install -e" in head
    assert "examples/LOOP_STATE.md" in head
    assert "examples/fail_gate.py" in head
    assert "loop-engine tick" in head
    assert "action : repair" in head
    assert "gate 'tests' is red; no new work on a broken base" in head
    assert "Interview pack" not in head
    assert "\u2014" not in head


def test_readme_stranger_red_gate_is_repair(tmp_path, capsys):
    journal = tmp_path / "stranger.md"
    code = main(
        [
            "tick",
            "--state",
            str(ROOT / "examples" / "LOOP_STATE.md"),
            "--journal",
            str(journal),
            "--gate",
            f"tests={sys.executable} {FAIL_GATE}",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "action : repair" in out
    assert "target : tests" in out
    assert "gate 'tests' is red; no new work on a broken base" in out
    assert journal.exists()

import json
import sys

from loopengine.cli import main


def test_tick_end_to_end(tmp_path, capsys):
    state = tmp_path / "LOOP_STATE.md"
    state.write_text("- [ ] A2 Next thing (cost: S) (touched: 2099-01-01)\n", encoding="utf-8")
    journal = tmp_path / "journal" / "JOURNAL.md"

    code = main(["tick", "--state", str(state), "--journal", str(journal), "--json"])
    assert code == 0

    out = json.loads(capsys.readouterr().out)
    assert out["action"] == "advance"
    assert out["target"].startswith("A2")
    assert journal.exists()


def test_missing_state_file_is_a_clean_error(tmp_path, capsys):
    code = main(["tick", "--state", str(tmp_path / "nope.md")])
    assert code == 2
    assert "not found" in capsys.readouterr().err


def _tick(tmp_path, state_text, *extra):
    state = tmp_path / "LOOP_STATE.md"
    state.write_text(state_text, encoding="utf-8")
    journal = tmp_path / "JOURNAL.md"
    return main(["tick", "--state", str(state), "--journal", str(journal), *extra]), journal


def test_gate_printing_an_emoji_still_gives_a_decision_and_journal(tmp_path, capsys):
    script = "import sys; sys.stdout.buffer.write(bytes([111, 107, 32, 0xe2, 0x9d, 0x8c, 10]))"
    gate = f'tests="{sys.executable}" -c "{script}"'
    code, journal = _tick(tmp_path, "- [ ] A1 X\n", "--gate", gate)
    assert code == 0
    assert "action : advance" in capsys.readouterr().out
    assert "tests=PASS" in journal.read_text(encoding="utf-8")


def test_bad_date_in_state_file_is_exit_2_with_the_line(tmp_path, capsys):
    code, journal = _tick(tmp_path, "- [ ] A1 Thing (cost: M) (touched: 2026-02-30)\n")
    assert code == 2
    err = capsys.readouterr().err
    assert "line 1" in err
    assert "2026-02-30" in err
    assert not journal.exists()


def test_star_and_numbered_backlog_is_not_closed(tmp_path, capsys):
    code, _ = _tick(tmp_path, "* [ ] A1 Thing (cost: M)\n1. [ ] A2 Other\n")
    assert code == 0
    out = capsys.readouterr().out
    assert "action : advance" in out
    assert "target : A1 Thing" in out


def test_reversed_tags_still_unstick_a_stale_head(tmp_path, capsys):
    code, _ = _tick(
        tmp_path, "- [ ] A1 Big (touched: 2026-01-01) (cost: L)\n- [ ] A2 Small (cost: S)\n"
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "action : unstick" in out
    assert "target : A2 Small" in out


def test_empty_gate_name_is_exit_2(tmp_path, capsys):
    for spec in (f"={sys.executable} -c pass", f"  ={sys.executable} -c pass"):
        code, journal = _tick(tmp_path, "- [ ] A1 X\n", "--gate", spec)
        assert code == 2
        assert "bad --gate spec" in capsys.readouterr().err
        assert not journal.exists()

import json

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

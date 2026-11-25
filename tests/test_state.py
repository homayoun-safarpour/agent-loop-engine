from datetime import date

import pytest

from loopengine.state import StateError, parse_state

SAMPLE = """
# My project state

Some prose the parser must ignore.

- [x] A1 Scaffold the package (cost: L) (touched: 2026-08-01)
- [ ] A2 Publish to PyPI (cost: M) (touched: 2026-08-01)
- [ ] A3 Write the worked example (cost: S)
- not an item line
"""


def test_parses_items_and_ignores_prose():
    state = parse_state(SAMPLE)
    assert len(state.items) == 3
    assert [i.done for i in state.items] == [True, False, False]


def test_open_and_done_partition():
    state = parse_state(SAMPLE)
    assert len(state.open_items) == 2
    assert len(state.done_items) == 1


def test_cost_defaults_to_medium_and_touched_optional():
    state = parse_state(SAMPLE)
    a3 = state.items[2]
    assert a3.cost == "S"
    assert a3.touched is None
    assert a3.days_stale(date(2026, 8, 3)) is None


def test_days_stale_counts_from_touched():
    state = parse_state(SAMPLE)
    a2 = state.items[1]
    assert a2.days_stale(date(2026, 8, 4)) == 3


def test_impossible_touched_date_is_refused():
    with pytest.raises(StateError, match="line 1"):
        parse_state("- [ ] A1 Thing (cost: M) (touched: 2026-02-30)\n")


def test_star_plus_and_numbered_bullets_are_items():
    text = "* [ ] A1 Thing (cost: M)\n+ [x] A2 Done\n1. [ ] A3 Other\n2) [ ] A4 More\n"
    state = parse_state(text)
    assert [i.title for i in state.items] == ["A1 Thing", "A2 Done", "A3 Other", "A4 More"]
    assert [i.done for i in state.items] == [False, True, False, False]


def test_tags_in_any_order_are_parsed():
    item = parse_state("- [ ] A1 Big (touched: 2026-01-01) (cost: L)\n").items[0]
    assert item.title == "A1 Big"
    assert item.cost == "L"
    assert item.touched == date(2026, 1, 1)


def test_checkbox_line_that_cannot_be_read_is_refused():
    bad_lines = (
        "- [ ]",
        "- [x]A1 no space",
        "- [ ] A1 X (cost: XL)",
        "- [ ] A1 X (cost: S) (cost: L)",
        "- [ ] A1 X (touched: 26-1-1)",
    )
    for line in bad_lines:
        with pytest.raises(StateError):
            parse_state(line + "\n")

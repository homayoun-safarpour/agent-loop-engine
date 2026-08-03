from datetime import date

from loopengine.state import parse_state

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

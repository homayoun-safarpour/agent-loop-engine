"""Contract template presence — Field Guide claim: blank LOOP_CONTRACT has required headings."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "examples" / "loop_contract" / "LOOP_CONTRACT.md"
GUIDE = ROOT / "docs" / "FIELD_GUIDE.md"

REQUIRED_HEADINGS = [
    "## 1. Done",
    "## 2. Verifier",
    "## 3. Stop layers",
    "## 4. State file",
    "## 5. Irreversible",
]


def test_loop_contract_template_has_five_decisions():
    text = CONTRACT.read_text(encoding="utf-8")
    for heading in REQUIRED_HEADINGS:
        assert heading in text, f"missing {heading} in {CONTRACT}"


def test_field_guide_exists_and_links_contract():
    text = GUIDE.read_text(encoding="utf-8")
    assert "Loop Contract" in text
    assert "examples/loop_contract/LOOP_CONTRACT.md" in text
    assert "Building effective agents" in text or "building-effective-agents" in text

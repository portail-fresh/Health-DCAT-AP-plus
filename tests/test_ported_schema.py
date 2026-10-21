"""The generated port of HealthDCAT-AP's shapes (healthdcat_ap_non_public.yaml):
checks that need neither the official clone nor the network.

The end-to-end check against the official shapes is
tests/test_shacl_validation.py; this file pins the one thing that check can
only see through a fixture that happens to populate the property.
"""

import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SIBLING_PATH = REPO_ROOT / "src" / "health_dcat_ap_plus" / "schema" / "healthdcat_ap_non_public.yaml"
CLONE = REPO_ROOT / "repos" / "healthdcat-ap"


def _ported_commit() -> str:
    match = re.search(r"^# healthdcat-ap commit: ([0-9a-f]{40})$", SIBLING_PATH.read_text(encoding="utf-8"), re.M)
    assert match, "the generated schema's header no longer records the healthdcat-ap commit it was ported from"
    return match.group(1)


def _ported() -> dict:
    return yaml.safe_load(SIBLING_PATH.read_text(encoding="utf-8"))


def test_slots_whose_local_name_collides_with_a_dcat_ap_plus_slot_keep_their_own_predicate():
    """csvw:name / csvw:title / cv:frequency once resolved, by their snake_case
    local name, to dcat-ap-plus's foaf:name / dcterms:title /
    dcterms:accrualPeriodicity slots, so a CSVW Column's name and title and an
    opening-hours TemporalEntity's frequency came out on the wrong predicates
    (nothing populated them, so nothing noticed). The port script now names
    them apart (PROPERTY_RENAME) and refuses to generate if any other shape
    lands on a slot of a different predicate."""
    ported = _ported()
    expected = {
        "column_name": "csvw:name",
        "column_title": "csvw:title",
        "temporal_entity_frequency": "cv:frequency",
    }
    assert {name: ported["slots"][name]["slot_uri"] for name in expected} == expected
    assert {"column_name", "column_title"} <= set(ported["classes"]["Column"]["slots"])
    assert not {"name", "titles", "title"} & set(ported["classes"]["Column"]["slots"])
    assert "temporal_entity_frequency" in ported["classes"]["TemporalEntity"]["slots"]
    assert "frequency" not in ported["classes"]["TemporalEntity"]["slots"]


def test_release_8_additions_are_ported():
    """What HealthDCAT-AP release 8 added to the non-public tier: a second HDAB,
    a mandatory title on the CSVW table group, and one csvw:name per column."""
    ported = _ported()
    assert ported["slots"]["hdab_coordinator"] == {"slot_uri": "healthdcatap:hdabCoordinator", "range": "HealthAgent"}
    assert "hdab_coordinator" in ported["classes"]["HealthDataset"]["slots"]
    assert ported["classes"]["TableGroup"]["slot_usage"]["title"] == {"required": True, "multivalued": True}
    assert ported["slots"]["column_name"].get("multivalued") is None
    assert ported["slots"]["column_name"]["required"] is True


def test_vocabulary_bindings_use_the_production_base_url():
    """Release 8 moved six controlled vocabularies from the acceptance to the
    production environment of the EU health data portal."""
    assert "acceptance.data.health" not in SIBLING_PATH.read_text(encoding="utf-8")


def test_ci_fetches_the_commit_the_schema_was_ported_from():
    """CI pins repos/healthdcat-ap to a commit (upstream moves files between
    releases and edits old ones in place), and that commit has to be the one
    recorded in the generated schema's header. Bump both together: re-run the
    port script on the new commit, then change the SHA in
    .github/workflows/main.yaml (and ResHealth-DCAT-AP's)."""
    workflow = (REPO_ROOT / ".github" / "workflows" / "main.yaml").read_text(encoding="utf-8")
    assert _ported_commit() in workflow


@pytest.mark.skipif(not CLONE.exists(), reason="repos/healthdcat-ap not cloned -- see README.md")
def test_local_clone_is_at_the_commit_the_schema_was_ported_from():
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=CLONE, capture_output=True, text=True, check=True
    ).stdout.strip()
    assert head == _ported_commit(), (
        f"repos/healthdcat-ap is at {head}, the schema was ported from {_ported_commit()}: "
        f"`git -C repos/healthdcat-ap fetch --depth 1 origin {_ported_commit()} && "
        "git -C repos/healthdcat-ap checkout --detach FETCH_HEAD`, or re-run the port script."
    )

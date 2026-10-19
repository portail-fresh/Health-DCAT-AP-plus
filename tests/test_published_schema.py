"""The schema files served at the w3id permalink (docs/schema/), and whether
another schema can actually import them.

Until 2026-10-19 the permalink served gen-yaml's *merged* output: every
dcat-ap-plus class copied into the file, and the same `imports:` still there.
Any schema importing it saw each dcat-ap-plus class twice and LinkML's legacy
loader (gen-yaml, PythonGenerator, gen-project, ...) refused with "Conflicting
URIs". Nothing in this repo noticed, because nothing in this repo imports its
own published file -- ResHealth-DCAT-AP does, and papered over it with a local
importmap. These tests are the missing consumer: they publish into a scratch
folder (scripts/publish_schema.py) and import the result from a throwaway
downstream schema, exactly like ResHealth-DCAT-AP does.

The one thing a local test cannot do is reach the w3id address itself, so the
published root's absolute sibling URL is pointed at the scratch copy through
an importmap in the last test. That is the only stand-in; the real end-to-end
check (no importmap at all, through w3id) is ResHealth-DCAT-AP's
scripts/check_schema_resolves.py.
"""

import shutil
import sys
from pathlib import Path

import pytest
import yaml
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.yamlgen import YAMLGenerator

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import publish_schema  # noqa: E402

SOURCE_DIR = publish_schema.SOURCE_DIR
ROOT_FILE = "health_dcat_ap_plus.yaml"
SIBLING = "healthdcat_ap_non_public"
SIBLING_URL = f"https://w3id.org/portail-fresh/Health-DCAT-AP-plus/latest/schema/{SIBLING}"


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def published(tmp_path_factory) -> Path:
    dest = tmp_path_factory.mktemp("w3id") / "published"
    publish_schema.publish(dest)
    return dest


def test_published_root_is_the_source_with_only_the_sibling_import_rewritten(published):
    source = _load(SOURCE_DIR / ROOT_FILE)
    result = _load(published / ROOT_FILE)

    assert SIBLING in source["imports"], "source no longer imports its sibling by bare name -- update this test"
    assert result["imports"] == [SIBLING_URL if imp == SIBLING else imp for imp in source["imports"]]
    assert {k: v for k, v in result.items() if k != "imports"} == {k: v for k, v in source.items() if k != "imports"}


def test_published_root_defines_only_its_own_elements(published):
    """The defect itself: gen-yaml's merged file has 72 classes (all 51 of
    dcat-ap-plus's among them); the source has only this schema's own."""
    source = _load(SOURCE_DIR / ROOT_FILE)
    result = _load(published / ROOT_FILE)
    for section in ("classes", "slots", "enums", "types", "subsets"):
        assert set(result.get(section) or {}) == set(source.get(section) or {}), section


def test_sibling_is_published_next_to_the_root_unchanged(published):
    expected = (SOURCE_DIR / f"{SIBLING}.yaml").read_text(encoding="utf-8")
    assert (published / f"{SIBLING}.yaml").read_text(encoding="utf-8") == expected


def test_no_bare_relative_imports_are_left_in_the_published_files(published):
    """A bare import in a *nested* schema is looked up next to the downstream
    schema, not next to the file declaring it -- see scripts/publish_schema.py."""
    for name in (ROOT_FILE, f"{SIBLING}.yaml"):
        for imp in _load(published / name).get("imports") or []:
            assert ":" in imp, f"{name} still imports {imp!r} by bare name"


def test_committed_docs_schema_is_current():
    """docs/schema is committed (and rebuilt by CI before every deploy); if
    the source changed without it being regenerated, this fails -- run
    `just gen-doc`. The merged snapshot is not compared: it needs gen-yaml
    and the network, and nothing imports it."""
    stale = [
        name
        for name, text in publish_schema.render_published().items()
        if (REPO_ROOT / "docs" / "schema" / name).read_text(encoding="utf-8") != text
    ]
    assert not stale, f"docs/schema is out of date for {stale} -- run `just gen-doc`"


def test_publish_refuses_a_bare_import_without_a_sibling_file(tmp_path):
    shutil.copy(SOURCE_DIR / ROOT_FILE, tmp_path / ROOT_FILE)  # no sibling copied next to it
    with pytest.raises(SystemExit, match=SIBLING):
        publish_schema.render_published(tmp_path)


DOWNSTREAM = """\
id: https://example.org/downstream
name: downstream
prefixes:
  downstream: https://example.org/downstream/
  linkml: https://w3id.org/linkml/
  # a nested import's CURIE is expanded with the *root* schema's prefix map,
  # so every downstream root has to declare dcat-ap-plus's label itself
  dcatap_plus: https://w3id.org/nfdi-de/dcat-ap-plus/
default_prefix: downstream
default_range: string
imports:
  - linkml:types
  - published/health_dcat_ap_plus
classes:
  DownstreamStudy:
    is_a: HealthDataset
"""


@pytest.fixture(scope="module")
def downstream(published) -> tuple[str, dict]:
    path = published.parent / "downstream.yaml"
    path.write_text(DOWNSTREAM, encoding="utf-8")
    # The sibling's absolute URL can't be fetched from w3id here (the files
    # being tested are not deployed yet); this is the only stand-in.
    return str(path), {SIBLING_URL: str(published / SIBLING)}


def test_downstream_schema_can_generate_python_from_the_published_root(downstream):
    """Legacy loader: before the fix, "Conflicting URIs ... for item: Activity"."""
    schema, importmap = downstream
    code = PythonGenerator(schema, importmap=importmap).serialize()
    assert "class DownstreamStudy(HealthDataset)" in code
    assert "class Activity(" in code, "dcat-ap-plus classes should come through the published root's own import"


def test_downstream_schema_can_merge_the_published_root_with_gen_yaml(downstream):
    schema, importmap = downstream
    merged = yaml.safe_load(YAMLGenerator(schema, importmap=importmap).serialize())
    assert {"DownstreamStudy", "HealthDataset", "Activity"} <= set(merged["classes"])

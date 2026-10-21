#!/usr/bin/env python
"""Regenerate examples/HealthDataset-full-example.ttl from
tests/data/problem/valid/HealthDataset-shacl-full.yaml, via the same
tests/test_shacl_validation.py::_build_test_dataset_graph() path the real
SHACL tests use -- see that function's own docstring for how the dataclasses
are constructed, why the dataset's dct:source is described in the same graph,
and which external terms are typed inline (OFFICIAL_CONVENTION_TERM_TYPES,
matching HealthDCAT-AP's own worked example,
examples/reference/example-healthdcat-dataset.ttl).

The output is serialized with scripts/gen_merged_shacl.py's blank-node
relabelling, so regenerating an unchanged example gives an identical file.

Run directly: `.venv/Scripts/python scripts/gen_example.py`. Re-run after
changing the fixture YAML or the schema.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tests"))
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from gen_merged_shacl import serialize_canonical  # noqa: E402
from test_shacl_validation import ELI, _build_test_dataset_graph  # noqa: E402

OUTPUT_PATH = REPO_ROOT / "examples" / "HealthDataset-full-example.ttl"

HEADER = """\
# Full worked HealthDataset example: a cancer registry dataset with
# agents, activities, entities, dataset-level attribution, and (on the
# DataGeneratingActivity) three qualified_association entries -- PI,
# sponsor, funder, real ISO 19115 CI_RoleCode roles, not invented. See
# docs/architecture-verification.md sections 5-6 for the full narrative.
#
# Source: tests/data/problem/valid/HealthDataset-shacl-full.yaml.
# Regenerate with `.venv/Scripts/python scripts/gen_example.py` (see that
# script's own docstring) after changing the fixture or schema.
#
# A self-contained document in HealthDCAT-AP's own style (release 8):
#   * the dataset's dct:source is a second dataset described in the same
#     graph, because DCAT-AP's shape wants a dct:source value to be a
#     dcat:Dataset (and so to satisfy the dataset shapes itself);
#   * every external term whose shape checks a plain class is typed inline
#     (`<term> a dct:Frequency .` and so on, at the end of the file), as the
#     official example does -- the official validator's vocabulary catalogue
#     does not supply those types. Terms checked through skos:inScheme are
#     not typed, as in the official example.
#
# Every external vocabulary/ontology term below was checked against its own
# real source, not assumed -- see the fixture YAML's comments and
# tests/data/real_vocabulary_terms.ttl for what was verified and how.
# applicable_legislation points at the real ELI for Regulation (EU) 2025/327,
# the EHDS Regulation itself. The personal-data term is not a DPV IRI: see the
# fixture's comment on has_personal_data.
#
# Validated against the merged shapes graph by
# tests/test_shacl_validation.py::test_published_example_conforms_to_merged_shacl
# (walked through in examples/HealthDataset-validation-check.ipynb): no
# violation, and warnings only for recommended properties this example leaves
# out. See the "thirteenth" and "fourteenth" findings of
# docs/architecture-verification.md.
"""


def main() -> None:
    g = _build_test_dataset_graph()
    g.bind("eli", ELI)
    OUTPUT_PATH.write_text(HEADER + "\n" + serialize_canonical(g), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({len(g)} triples)")


if __name__ == "__main__":
    sys.exit(main())

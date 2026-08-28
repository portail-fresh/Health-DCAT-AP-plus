#!/usr/bin/env python
"""Regenerate examples/HealthDataset-full-example.ttl from
tests/data/problem/valid/HealthDataset-shacl-full.yaml, via the same
tests/test_shacl_validation.py::_build_test_dataset_graph() path the real
SHACL tests use -- see that function's own docstring for the dataclass
construction details.

Also merges in a small set of external-term "stub" triples
(EXTERNAL_TERM_STUBS below) before serializing, matching the real,
official convention confirmed directly in HealthDCAT-AP's own worked
example (examples/reference/example-healthdcat-dataset.ttl, vendored in
this repo): a self-contained example carries a bare `<term> a <Class> .`
triple for each external term it references whose real shape checks a
simple sh:class constraint, so the file validates standalone without a
live vocabulary server. Confirmed which terms actually need this by
checking dcat-ap-plus's own declared ranges directly (access_rights ->
RightsStatement, language -> LinguisticSystem, frequency -> Frequency,
applicable_legislation -> LegalResource) and HealthDCAT-AP's own range.ttl
(hasCodingSystem -> Standard) -- not by copying the official example's
choices blindly. Deliberately does NOT add stubs for theme/type (both
range: Concept, class_uri skos:Concept) even though they're also
externally referenced: the official example doesn't either, for the same
reason skos:Concept-based checks in mdr-vocabularies.shape.ttl work
differently (skos:inScheme membership, not a bare class assertion) --
matching the official convention's own choices exactly, not going beyond
them.

Run directly: `.venv/Scripts/python scripts/gen_example.py`. Re-run after
changing the fixture YAML or the schema.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tests"))
sys.path.insert(0, str(REPO_ROOT / "src"))

from rdflib import RDF, Graph, Namespace, URIRef  # noqa: E402
from test_shacl_validation import _build_test_dataset_graph  # noqa: E402

OUTPUT_PATH = REPO_ROOT / "examples" / "HealthDataset-full-example.ttl"

DCT = Namespace("http://purl.org/dc/terms/")
ELI = Namespace("http://data.europa.eu/eli/ontology#")

# (external term URI, real class it's a member of) -- see this module's
# own docstring for how each entry was confirmed, not assumed.
EXTERNAL_TERM_STUBS: list[tuple[str, URIRef]] = [
    ("http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC", DCT.RightsStatement),
    ("http://publications.europa.eu/resource/authority/language/ENG", DCT.LinguisticSystem),
    ("http://publications.europa.eu/resource/authority/frequency/ANNUAL", DCT.Frequency),
    ("http://data.europa.eu/eli/reg/2025/327/oj", ELI.LegalResource),
    (
        "https://hdeu-dcat.acceptance.data.health.europa.eu/resource/authority/standard/FHIR",
        DCT.Standard,
    ),
    (
        "https://hdeu-dcat.acceptance.data.health.europa.eu/resource/authority/coding-system/ICD-O-3",
        DCT.Standard,
    ),
]

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
# Every external vocabulary/ontology term below was checked directly
# against its own real source, not assumed -- see the fixture YAML's own
# comments and tests/data/real_vocabulary_terms.ttl for exactly what was
# verified and how. applicable_legislation points at the real ELI for
# Regulation (EU) 2025/327, the EHDS Regulation itself.
#
# This exact file was manually pasted into Sciensano's own official
# HealthDCAT-AP validator (https://healthdcat-validator.sciensano.be) on
# 2026-08-26 as a real-world cross-check, not just our own pyshacl run --
# see tests/test_shacl_validation.py's KNOWN_REAL_SHAPES_VIOLATIONS comment
# for what that surfaced: five term references below were invented/wrong,
# not just unverifiable (healthcategories/ONCOLOGY, health-theme/CANCER,
# coding-system/ICD_O_3, dataset-type/EXPLOITABLE, and conformsTo's own
# local schema URI, replaced with a real standard-vocabulary member,
# .../authority/standard/FHIR), and all five are now fixed to real
# vocabulary codes (or, for conformsTo, a real vocabulary member entirely).
#
# dct:source is a bare URI reference (not nested/inlined) -- confirmed
# directly against examples/reference/example-healthdcat-dataset.ttl
# (HealthDCAT-AP's own official worked example) and the release-7 spec's
# own usage note ("the source Dataset must be fully described" separately,
# not embedded here). Getting this far needed a real port-script fix
# (scripts/port_healthdcat_ap_shacl_to_linkml.py's
# _FORCE_NON_INLINED_ON_RECOVERED_RANGE) plus a real gap fix in
# scripts/patch_post_init_shielding.py's own shield-map computation.
#
# dqv:hasQualityAnnotation's own value is now a real, correctly-typed
# QualityCertificate object (see below), not a bare reference either --
# the earlier "single-slot stub classes always collapse" diagnosis was
# imprecise; the real, narrower cause was specifically that
# has_quality_annotation never had inlined_as_list: true set on it at
# all. Fixed the same way as qualified_attribution already was, in
# port_healthdcat_ap_shacl_to_linkml.py.
#
# The bare `<term> a <Class> .` triples at the end of this file (before the
# blank-node stub resources) mirror HealthDCAT-AP's own official worked
# example's convention exactly -- see scripts/gen_example.py's own
# docstring for which terms get one and why.
#
# See examples/HealthDataset-validation-check.ipynb, next to this file, for
# a runnable walkthrough of exactly how this file gets validated (the same
# check tests/test_shacl_validation.py::test_dataset_conforms_to_merged_shacl
# runs in CI) and what the few remaining, deliberate known violations are.
"""


def main() -> None:
    g = _build_test_dataset_graph()
    g.bind("eli", ELI)
    for term, cls in EXTERNAL_TERM_STUBS:
        g.add((URIRef(term), RDF.type, cls))
    ttl = g.serialize(format="turtle")
    OUTPUT_PATH.write_text(HEADER + "\n" + ttl, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({len(g)} triples)")


if __name__ == "__main__":
    sys.exit(main())

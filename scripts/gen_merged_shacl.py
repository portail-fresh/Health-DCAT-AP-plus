#!/usr/bin/env python
"""Generate docs/schema/health_dcat_ap_plus.merged-shacl.ttl: ONE SHACL
shapes graph combining HealthDCAT-AP's real, official upstream shapes with
this schema's own generated shapes for everything the real shapes don't
cover (the Activity/Association/Attribution/Entity side).

Why not just union the two generated-SHACL graphs naively: HealthDataset
(and every other Health<X> profile class) deliberately shares its class_uri
with dcat-ap-plus's own base class (dcat:Dataset, dcat:Distribution,
foaf:Agent -- "same real-world type, tighter shape"). Generating SHACL from
*our own* schema for those classes therefore produces a second, divergent
sh:property set for the same predicates HealthDCAT-AP's real shapes already
define (e.g. dct:accessRights: bare IRI per the real spec vs. object-shaped
RightsStatement per dcat-ap-plus's own generic convention) -- one value
can't satisfy both at once. Confirmed directly, not assumed: this conflict
exists between our own generated shapes and dcat-ap-plus's own generated
shapes; it does NOT exist between our own generated shapes and HealthDCAT-AP's
*real* official ones, which are already self-sufficient and never unioned
with plain DCAT-AP's generic shapes in the real world.

The fix: drop our own generated NodeShapes for any class the real shapes
already own (via sh:targetClass, or -- for foaf:Agent specifically -- via
sh:node references from Dataset's own hdab/custodian/publisher property
shapes, confirmed directly by grepping non-public-shapes.ttl), plus a
second, separately-motivated exclusion for classes whose real-world
instances are always externally-authored controlled-vocabulary/standard
terms (skos:Concept, dct:Standard, dpv:LegalBasis, ...) -- our own
sh:closed shapes for those exist only to type-check an *inline stub* we
might construct ourselves, and produce dozens of false ClosedConstraintComponent
violations against real, richly-labeled external vocabulary content
(confirmed directly: merging HealthDCAT-AP's own real vocabulary catalogue
in as validation data violates our own skos:Concept shape's narrow
allowlist). This is genuinely the same category as the Dataset/Distribution/
Agent case (a class we don't author real instances of), just not detected
by the sh:targetClass-overlap scan, so listed explicitly like foaf:Agent.

Since specialization work (ResHealth-DCAT-AP and siblings) only ever adds
new classes on the Activity/Association side and never touches Dataset/
Distribution/Agent/Catalog, this exclusion set is stable by construction --
it tracks what HealthDCAT-AP's real shapes (and reality's own vocabulary
authorities) already own, not our own schema's ever-growing class list.

The generic half of "drop shapes for excluded target classes" (walking a
shape's own blank-node structure to remove it cleanly) lives in
linkml-merge-toolkit (https://github.com/portail-fresh/linkml-merge-toolkit)
now, not here -- it had nothing to do with health data or dcat-ap-plus.
What stays here is genuinely project-specific: which files to load, the
two upstream bug workarounds below, and which classes to exclude beyond
plain sh:targetClass overlap (EXTERNAL_VOCABULARY_STUB_CLASSES, foaf:Agent).

Requires the sibling HealthDCAT-AP shapes clone (see README.md).

HealthDCAT-AP's own real shapes are Copyright (c) 2025 European Union,
published under CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/) --
confirmed directly in the release-7 spec's own License section, not
assumed. This script includes them (with two small, already-documented
upstream bug fixes -- a missing trailing slash in the dcatap: prefix, and
one malformed sh:property triple with no sh:path dropped) inside the merged
output below, with that attribution preserved in the generated file's own
header -- see LICENSE_HEADER.
"""
from __future__ import annotations

import sys
from pathlib import Path

from linkml.generators.shaclgen import ShaclGenerator
from linkml_merge_toolkit.shacl_merge import filtered_shapes_graph, targeted_classes
from rdflib import Graph, Namespace, URIRef

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "src" / "health_dcat_ap_plus" / "schema" / "health_dcat_ap_plus.yaml"
HEALTHDCATAP_SHACL_DIR = (
    REPO_ROOT / "repos" / "healthdcat-ap" / "public" / "releases" / "release-7" / "html" / "shacl"
)
OUTPUT_PATH = REPO_ROOT / "docs" / "schema" / "health_dcat_ap_plus.merged-shacl.ttl"

SH = Namespace("http://www.w3.org/ns/shacl#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

# Same real upstream typo fix and malformed-triple workaround as
# tests/test_shacl_validation.py's own _real_healthdcat_ap_shapes_graph --
# duplicated deliberately (scripts/ and tests/ aren't set up as a shared
# importable package here) rather than coupling the generation pipeline to
# the test suite's own layout. Keep both in sync if the upstream fix ever
# needs updating.
_BROKEN_DCATAP_PREFIX = "@prefix dcatap: <http://data.europa.eu/r5r> ."
_FIXED_DCATAP_PREFIX = "@prefix dcatap: <http://data.europa.eu/r5r/> ."
_REAL_SHAPE_FILES = [
    "non-public-shapes.ttl",
    "non-public-shapes_recommended.ttl",
    "range.ttl",
    "mdr-vocabularies.shape.ttl",
    "deprecateduris.ttl",
]

# Classes whose real-world instances are always externally-authored
# vocabulary/standard/codelist terms (EU MDR, DPV, SPDX, QUDT/schema.org
# DefinedTerm...), never something this schema or a downstream
# specialization constructs itself -- see this module's own docstring for
# the full diagnosis. Not detected by the targetClass-overlap scan (the
# real shapes don't targetClass these either -- they reach the ones they do
# cover via sh:node from named restriction shapes), so listed explicitly.
EXTERNAL_VOCABULARY_STUB_CLASSES = [
    "http://www.w3.org/2004/02/skos/core#Concept",
    "http://www.w3.org/2004/02/skos/core#ConceptScheme",
    "http://purl.org/dc/terms/Standard",
    "http://purl.org/dc/terms/Frequency",
    "http://purl.org/dc/terms/LinguisticSystem",
    "http://purl.org/dc/terms/RightsStatement",
    "http://purl.org/dc/terms/MediaType",
    "http://purl.org/dc/terms/MediaTypeOrExtent",
    "https://w3id.org/dpv#LegalBasis",
    "https://w3id.org/dpv#PersonalData",
    "https://w3id.org/dpv#Purpose",
    "http://www.w3.org/ns/dcat#Role",
    "http://spdx.org/rdf/terms#ChecksumAlgorithm",
    "http://www.w3.org/ns/locn#Geometry",
    "http://schema.org/DefinedTerm",
]


def require_sibling_shacl_checkout() -> None:
    if not HEALTHDCATAP_SHACL_DIR.exists():
        raise SystemExit(
            f"expected HealthDCAT-AP's real shapes at {HEALTHDCATAP_SHACL_DIR} -- see "
            "README.md's 'git clone --depth 1 "
            "https://code.europa.eu/healthdataeu/healthdcat-ap.git repos/healthdcat-ap' "
            "for how to fetch it"
        )


def load_real_shapes_graph() -> Graph:
    """Load HealthDCAT-AP's own real, official upstream SHACL shapes (non-public tier)."""
    require_sibling_shacl_checkout()
    g = Graph()
    for fname in _REAL_SHAPE_FILES:
        text = (HEALTHDCATAP_SHACL_DIR / fname).read_text(encoding="utf-8")
        if _BROKEN_DCATAP_PREFIX in text:
            text = text.replace(_BROKEN_DCATAP_PREFIX, _FIXED_DCATAP_PREFIX)
        g.parse(data=text, format="turtle")

    # Real bug in HealthDCAT-AP's own non-public-shapes.ttl -- see
    # tests/test_shacl_validation.py's own comment on this same fix for the
    # full diagnosis (Dataset_Shape's hasStructuredData/hasVariables sh:or
    # used directly as an sh:property value, with no sh:path).
    removed = [(s, p, o) for s, p, o in g.triples((None, SH.property, None)) if (o, SH.path, None) not in g]
    assert len(removed) == 1, (
        f"expected exactly 1 malformed sh:property in non-public-shapes.ttl, "
        f"found {len(removed)} -- upstream shapes changed, re-diagnose before trusting this workaround"
    )
    for triple in removed:
        g.remove(triple)
    return g


def load_own_shapes_graph() -> Graph:
    ttl = ShaclGenerator(str(SCHEMA_PATH)).serialize()
    g = Graph()
    g.parse(data=ttl, format="turtle")
    return g


def excluded_target_classes(real_graph: Graph) -> set:
    """Every class our own generated shapes should NOT independently
    target: whatever the real shapes already own (sh:targetClass), plus
    foaf:Agent (owned via sh:node, not sh:targetClass -- see this module's
    docstring), plus the external-vocabulary-stub classes above. The
    "whatever real shapes already own" part is generic (linkml-merge-toolkit's
    own targeted_classes); the two additions are this schema's own
    knowledge, not something a generic toolkit could guess -- see
    linkml-merge-toolkit's own README for why that split exists.
    """
    classes = targeted_classes(real_graph)
    classes.add(FOAF.Agent)
    classes.update(URIRef(c) for c in EXTERNAL_VOCABULARY_STUB_CLASSES)
    return classes


def build_merged_shapes_graph() -> Graph:
    real = load_real_shapes_graph()
    own = load_own_shapes_graph()
    filtered_own = filtered_shapes_graph(own, excluded_target_classes(real))
    return filtered_own + real


LICENSE_HEADER = """\
# health_dcat_ap_plus.merged-shacl.ttl -- GENERATED FILE, do not edit by
# hand. Regenerate with `just gen-shacl` (see scripts/gen_merged_shacl.py's
# own docstring for the full mechanism and why a naive union of every
# generated shape doesn't work).
#
# This file combines two things:
#
#   1. HealthDCAT-AP's own real, official upstream SHACL shapes (release 7,
#      non-public tier: deprecateduris.ttl, range.ttl,
#      mdr-vocabularies.shape.ttl, non-public-shapes.ttl,
#      non-public-shapes_recommended.ttl), Copyright (c) 2025 European
#      Union, published under CC-BY 4.0
#      (https://creativecommons.org/licenses/by/4.0/) -- see
#      https://code.europa.eu/healthdataeu/healthdcat-ap. Included here
#      with two small upstream bug fixes applied (a missing trailing slash
#      in the dcatap: prefix declaration; one malformed sh:property triple
#      with no sh:path removed) -- see scripts/gen_merged_shacl.py for both.
#
#   2. This schema's own generated SHACL for everything the real shapes
#      above don't cover -- the Activity/Association/Attribution/Entity
#      side (DataGeneratingActivity, AgenticEntity, Plan, and their
#      subclasses) -- with NodeShapes for Dataset/Distribution/Agent/
#      Catalog/vocabulary-stub classes deliberately excluded, since the
#      real shapes above already own those.
#
# Source: src/health_dcat_ap_plus/schema/health_dcat_ap_plus.yaml
"""


def main() -> None:
    g = build_merged_shapes_graph()
    ttl = g.serialize(format="turtle")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(LICENSE_HEADER + "\n" + ttl, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({len(g)} triples)")


if __name__ == "__main__":
    sys.exit(main())

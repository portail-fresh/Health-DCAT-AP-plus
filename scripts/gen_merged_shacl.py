#!/usr/bin/env python
"""Generate docs/schema/health_dcat_ap_plus.merged-shacl.ttl: ONE SHACL
shapes graph for validating data against this schema, combining what the
official HealthDCAT-AP validator checks with this schema's own generated
shapes for everything that validator doesn't cover (the Activity/
Association/Attribution/Entity side).

What the official validator checks (HealthDCAT-AP's own tier files, read from
config.properties and the shape files themselves, release 8):

  * the tier's shape files -- shapes/non-public-shapes.ttl, the recommended/,
    ranges/ and controlled-vocabularies/ files and deprecated/deprecateduris.ttl
    (OFFICIAL_SHAPE_FILES). These are a DELTA: they reuse the IRIs of DCAT-AP
    3.0.0's own shapes (Dataset_Shape, Distribution_Shape, ...) and add to them.
  * the DCAT-AP 3.0.0 shapes they owl:import (shapes.ttl, shapes_recommended.ttl,
    range.ttl). The validator resolves each import URL to a copy under its
    catalogue/ folder (owlImportMapping in config.properties) and loads it into
    the shape graph. Without them dct:title and dct:description of a dataset,
    the sh:class checks on dct:accessRights, dct:language, dct:source, ... and
    the shapes for Agent, Location, Identifier, CatalogRecord, Concept are
    simply absent -- a bare `a dcat:Dataset` gets 41 results from the delta and
    45 with the base, and the hosted release-8 validator rejects it for the
    missing title. load_official_shapes_graph() follows the imports the same way
    and refuses to continue if one has no mapping.
  * shapes/graph-guard.ttl (release 8): a SPARQL check that the graph contains
    a dcat:Dataset. NOT included here: it guards the hosted service against
    non-dataset documents, it is not a constraint on dataset metadata, and a
    shapes graph used on a fragment would fail it for no reason.
  * the vocabulary catalogue (health-theme.rdf, ...) is DATA that the validator
    adds to the graph being validated, not shapes; tests/ does the same.

Why not just union that with our own generated shapes: HealthDataset (and every
other Health<X> profile class) deliberately shares its class_uri with a
dcat-ap-plus class ("same real-world type, tighter shape"), so shapes generated
from OUR schema for dcat:Dataset, dcat:Distribution, foaf:Agent, ... carry a
second, divergent sh:property set for predicates the official shapes already
define; one value cannot satisfy both. So build_merged_shapes_graph():

  1. generates our shapes OPEN (closed=False). LinkML closes them by default, and
     a closed shape for a class the official shapes only require as an sh:class
     value (prov:Activity, dqv:QualityCertificate, eli:LegalResource, ...) rejects
     the properties the official example puts on those nodes (hasBody,
     hasTarget, label, motivatedBy). The official shapes are open.
  2. drops every NodeShape of ours whose class the official shapes already
     target (computed from the official graph, foaf:Agent and skos:Concept
     included now that DCAT-AP's own shapes are loaded), plus the classes of
     EXTERNAL_VOCABULARY_STUB_CLASSES -- terms authored in external vocabularies
     (EU authority tables, DPV, SPDX, ...), whose real, language-tagged content
     fails our datatype constraints on them (dct:title is xsd:string here).
  3. applies GENERATOR_WORKAROUNDS to what is left; each one raises when it
     finds nothing to change, so the day LinkML fixes the bug (or the schema
     changes) it has to be deleted, not carried silently.
  4. adds the official graph.

Specialization work (ResHealth-DCAT-AP and siblings) adds classes on the
Activity/Association side and never touches Dataset/Distribution/Agent/Catalog,
so this stays stable by construction: it tracks what the official shapes own,
not our schema's ever-growing class list. ResHealth-DCAT-AP calls
build_merged_shapes_graph() with its own schema.

The generic half of "drop shapes for excluded target classes" lives in
linkml-merge-toolkit (https://github.com/portail-fresh/linkml-merge-toolkit);
what stays here is project-specific: which files to load, the workarounds, and
which classes to leave to the vocabularies.

Requires the HealthDCAT-AP clone at the pinned commit (see README.md).

HealthDCAT-AP's own shapes are Copyright (c) 2025 European Union, published
under CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/) -- confirmed
in the release-8 spec's License section and the repository's LICENSE file.
This script includes them (with one small, already-documented upstream bug fix
-- one malformed sh:property triple with no sh:path dropped, still open
upstream as healthdataeu/healthdcat-ap#43) inside the merged output, with that
attribution in the generated file's header -- see LICENSE_HEADER.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from linkml.generators.shaclgen import ShaclGenerator
from linkml_merge_toolkit.shacl_merge import blank_closure, filtered_shapes_graph, targeted_classes
from rdflib import BNode, Graph, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "src" / "health_dcat_ap_plus" / "schema" / "health_dcat_ap_plus.yaml"

# The one place that says which HealthDCAT-AP release the shapes (and the
# validator's vocabulary catalogue) are read from: tests/ and ResHealth-DCAT-AP
# take these constants from here rather than spelling the paths out again, so
# the next release is a change to this block and to the port script's
# TIER_FILES. Release 8 ships the shape files only inside the official
# validator's config tree (`ehds`), one sub-folder per kind of file; release 7
# also had flat copies in html/shacl/. The clone is pinned by commit in CI
# (.github/workflows/main.yaml) and recorded in the generated schema's header.
HEALTHDCATAP_RELEASE = "release-8"
HEALTHDCATAP_SHACL_DIR = (
    REPO_ROOT
    / "repos"
    / "healthdcat-ap"
    / "public"
    / "releases"
    / HEALTHDCATAP_RELEASE
    / "html"
    / "shacl"
    / "HealthDCAT-AP_validator"
    / "config"
    / "rdf-validator"
    / "ehds"
)
# The validator's preloaded vocabulary catalogue (health-theme.rdf, ...), and
# where it keeps the copies of the DCAT-AP shapes the official files import.
OFFICIAL_VOCABULARY_CATALOGUE_DIR = HEALTHDCATAP_SHACL_DIR / "catalogue"
OUTPUT_PATH = REPO_ROOT / "docs" / "schema" / "health_dcat_ap_plus.merged-shacl.ttl"

SH = Namespace("http://www.w3.org/ns/shacl#")
PROV = Namespace("http://www.w3.org/ns/prov#")
DCT = Namespace("http://purl.org/dc/terms/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
SCHEMA_ORG = Namespace("http://schema.org/")

# The non-public tier's own shape files, relative to HEALTHDCATAP_SHACL_DIR
# (the DCAT-AP shapes they import are added by load_official_shapes_graph).
# Not listed: shapes/graph-guard.ttl (see the module docstring) and
# imports/*.ttl (owl:imports manifests of ontologies and code lists, i.e. data).
OFFICIAL_SHAPE_FILES = [
    "shapes/non-public-shapes.ttl",
    "recommended/non-public-shapes_recommended.ttl",
    "ranges/range.ttl",
    "controlled-vocabularies/mdr-vocabularies.shape.ttl",
    "deprecated/deprecateduris.ttl",
]

# Classes whose real-world instances are always externally-authored
# vocabulary/standard/codelist terms (EU authority tables, DPV, SPDX, locn,
# schema.org DefinedTerm...), never something this schema or a downstream
# specialization constructs itself -- see the module docstring (step 2). Not
# detected by the targetClass scan: the official shapes only require most of
# them as an sh:class value (range.ttl). skos:Concept, skos:ConceptScheme and
# foaf:Agent used to be listed too; the DCAT-AP shapes target them, so they
# are derived now (tests/test_shacl_validation.py checks that this list holds
# nothing the official shapes target).
EXTERNAL_VOCABULARY_STUB_CLASSES = [
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
            "README.md for how to fetch the pinned commit into repos/healthdcat-ap"
        )


def owl_import_mapping() -> dict[str, Path]:
    """The validator's own owlImportMapping (config.properties): import URL ->
    file under HEALTHDCATAP_SHACL_DIR."""
    uris: dict[str, str] = {}
    files: dict[str, str] = {}
    text = (HEALTHDCATAP_SHACL_DIR / "config.properties").read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"\s*validator\.owlImportMapping\.(\d+)\.(uri|file)\s*=\s*(\S+)", line)
        if m:
            (uris if m.group(2) == "uri" else files)[m.group(1)] = m.group(3)
    return {uris[i]: HEALTHDCATAP_SHACL_DIR / files[i] for i in uris if i in files}


def load_official_shapes_graph() -> Graph:
    """HealthDCAT-AP's own official SHACL shapes (non-public tier) as the
    official validator assembles them: OFFICIAL_SHAPE_FILES plus every shape
    file they owl:import, resolved through the validator's own mapping."""
    require_sibling_shacl_checkout()
    g = Graph()
    for fname in OFFICIAL_SHAPE_FILES:
        g.parse(HEALTHDCATAP_SHACL_DIR / fname, format="turtle")

    mapping = owl_import_mapping()
    loaded: set = set()
    pending = set(g.objects(None, OWL.imports))
    while pending:
        uri = pending.pop()
        loaded.add(uri)
        if str(uri) not in mapping:
            raise SystemExit(
                f"the official shapes owl:import <{uri}>, which config.properties has no owlImportMapping for -- "
                "a new release changed its imports; decide whether this import carries shapes before continuing"
            )
        imported = Graph()
        imported.parse(mapping[str(uri)], format="turtle")
        pending |= set(imported.objects(None, OWL.imports)) - loaded
        g += imported

    # Real bug in HealthDCAT-AP's own non-public-shapes.ttl, still there in
    # release 8 (healthdataeu/healthdcat-ap#43): Dataset_Shape's
    # hasStructuredData/hasVariables sh:or is used directly as an sh:property
    # value, with no sh:path -- not a well-formed SHACL PropertyShape, and
    # strict processors (pyshacl included) reject the whole file because of it.
    # Not our file to fix -- worked around by dropping just that one triple so
    # the rest can be checked; the conditional constraint it carried ("if
    # hasStructuredData is true, hasVariables is required") goes unenforced here
    # (the hosted validator does enforce it). If this assertion ever fires, the
    # upstream file changed shape -- re-diagnose before trusting the workaround.
    removed = [(s, p, o) for s, p, o in g.triples((None, SH.property, None)) if (o, SH.path, None) not in g]
    assert len(removed) == 1, (
        f"expected exactly 1 malformed sh:property (Dataset_Shape's "
        f"hasStructuredData/hasVariables sh:or missing sh:path) in "
        f"non-public-shapes.ttl, found {len(removed)} -- upstream shapes "
        "changed, re-diagnose before trusting this workaround"
    )
    for triple in removed:
        g.remove(triple)
    return g


def generate_own_shapes_graph(schema_path: Path = SCHEMA_PATH) -> Graph:
    """Our schema's generated SHACL, open (see the module docstring, step 1).

    as_graph(), not serialize() + re-parse: the same triples, minus a text
    round-trip and the canonicalisation LinkML 1.12 added to serialize(),
    which stalls instead of failing on an unexpanded CURIE -- see
    tests/test_shacl_validation.py's guard tests."""
    return ShaclGenerator(str(schema_path), closed=False).as_graph()


def excluded_target_classes(official: Graph) -> set:
    """Every class our own generated shapes should NOT independently target:
    whatever the official shapes (with the DCAT-AP shapes they import) target
    via sh:targetClass -- the generic part, linkml-merge-toolkit's own
    targeted_classes -- plus the externally-authored vocabulary classes,
    which are this schema's own knowledge."""
    classes = targeted_classes(official)
    classes.update(URIRef(c) for c in EXTERNAL_VOCABULARY_STUB_CLASSES)
    return classes


# ---------------------------------------------------------------------------
# Workarounds for what LinkML's ShaclGenerator emits from our schema. Each
# works in place on a copy of OUR shapes, returns how many things it changed,
# and apply_generator_workarounds() raises on zero.
# ---------------------------------------------------------------------------
def _property_shapes(g: Graph, target_class=None, path=None) -> list:
    """(node shape, property shape) pairs, optionally for shapes targeting
    `target_class` and/or property shapes with sh:path `path`."""
    out = []
    for shape, _, ps in g.triples((None, SH.property, None)):
        if target_class is not None and (shape, SH.targetClass, target_class) not in g:
            continue
        if path is not None and (ps, SH.path, path) not in g:
            continue
        out.append((shape, ps))
    return out


def drop_rdf_type_property_shapes(g: Graph) -> int:
    """dcat-ap-plus's ClassifierMixin.rdf_type slot has slot_uri rdf:type, so
    LinkML emits `sh:path rdf:type` + `sh:class schema:DefinedTerm` on every
    Activity/Entity/AgenticEntity/Plan shape. SHACL cannot tell the class-typing
    triple (`<node> a prov:Activity`) from a classifier value, so every node
    "violates" it (linkml/linkml#3931, nfdi-de/dcat-ap-plus#110)."""
    pairs = _property_shapes(g, path=RDF.type)
    for shape, ps in pairs:
        g.remove((shape, SH.property, ps))
        for b in blank_closure(g, ps):
            for t in list(g.triples((b, None, None))):
                g.remove(t)
    return len(pairs)


def relax_required_prov_value(g: Graph) -> int:
    """dcat-ap-plus's QualitativeAttribute requires `value` (prov:value) but
    shares class_uri prov:Entity with Entity, EvaluatedEntity and
    AnalysisSourceData, and LinkML merges classes sharing a class_uri into one
    NodeShape, so the minCount lands on every prov:Entity in the graph
    (linkml/linkml#3932). Only the minCount is removed; the rest of the
    property shape stays."""
    n = 0
    for _shape, ps in _property_shapes(g, target_class=PROV.Entity, path=PROV.value):
        for count in list(g.objects(ps, SH.minCount)):
            g.remove((ps, SH.minCount, count))
            n += 1
    return n


def accept_concept_as_activity_type(g: Graph) -> int:
    """dcat-ap-plus types a prov:Activity with a single schema:DefinedTerm,
    while HealthDCAT-AP types the activity of prov:wasGeneratedBy with a
    skos:Concept of its health-activity table (its mdr-vocabularies shapes
    check exactly that; its own example does it; documenting it is open
    upstream as healthdataeu/healthdcat-ap#53). A valid HealthDCAT-AP dataset
    therefore failed our shape. The class constraint becomes DefinedTerm OR
    skos:Concept -- not a binding to the health-activity table, which
    HealthDCAT-AP's own shapes already do."""
    n = 0
    for _shape, ps in _property_shapes(g, target_class=PROV.Activity, path=DCT.type):
        for cls in list(g.objects(ps, SH["class"])):
            if cls != SCHEMA_ORG.DefinedTerm:
                continue
            g.remove((ps, SH["class"], cls))
            options = []
            for accepted in (cls, SKOS.Concept):
                option = BNode()
                g.add((option, SH["class"], accepted))
                options.append(option)
            head = BNode()
            Collection(g, head, options)
            g.add((ps, SH["or"], head))
            n += 1
    return n


GENERATOR_WORKAROUNDS = [
    ("rdf:type property shapes of ClassifierMixin (linkml#3931)", drop_rdf_type_property_shapes),
    ("required prov:value on every prov:Entity (linkml#3932)", relax_required_prov_value),
    ("prov:Activity dct:type accepts skos:Concept (healthdcat-ap#53)", accept_concept_as_activity_type),
]


def apply_generator_workarounds(own: Graph) -> Graph:
    """Apply GENERATOR_WORKAROUNDS in place; a workaround that changes nothing
    means the generator or the schema changed -- if the underlying bug is
    fixed, delete it."""
    for name, workaround in GENERATOR_WORKAROUNDS:
        if not workaround(own):
            raise RuntimeError(
                f"workaround '{name}' found nothing to change in the generated shapes -- the bug it works around "
                "may be fixed, or the schema changed; check, and delete the workaround if it is no longer needed"
            )
    return own


def build_merged_shapes_graph(schema_path: Path = SCHEMA_PATH) -> Graph:
    official = load_official_shapes_graph()
    own = filtered_shapes_graph(generate_own_shapes_graph(schema_path), excluded_target_classes(official))
    return apply_generator_workarounds(own) + official


LICENSE_HEADER = """\
# health_dcat_ap_plus.merged-shacl.ttl -- GENERATED FILE, do not edit by
# hand. Regenerate with `just gen-shacl` (see scripts/gen_merged_shacl.py's
# own docstring for the full mechanism and why a naive union of every
# generated shape doesn't work).
#
# This file combines two things:
#
#   1. HealthDCAT-AP's own official upstream SHACL shapes (release 8,
#      non-public tier: deprecateduris.ttl, range.ttl,
#      mdr-vocabularies.shape.ttl, non-public-shapes.ttl,
#      non-public-shapes_recommended.ttl), Copyright (c) 2025 European
#      Union, published under CC-BY 4.0
#      (https://creativecommons.org/licenses/by/4.0/) -- see
#      https://code.europa.eu/healthdataeu/healthdcat-ap -- together with the
#      DCAT-AP 3.0.0 SHACL shapes (SEMIC, https://semiceu.github.io/DCAT-AP/;
#      shapes.ttl, shapes_recommended.ttl, range.ttl) that those files
#      owl:import and that HealthDCAT-AP's validator loads from its own copy.
#      Included with one small upstream bug fix applied (one malformed
#      sh:property triple with no sh:path removed) -- see
#      scripts/gen_merged_shacl.py. Not included: release 8's graph-guard.ttl.
#
#   2. This schema's own generated SHACL (open, not closed) for everything the
#      shapes above don't cover -- the Activity/Association/Attribution/Entity
#      side (DataGeneratingActivity, AgenticEntity, Plan, and their
#      subclasses) -- with NodeShapes for Dataset/Distribution/Agent/Catalog/
#      vocabulary-term classes deliberately excluded, since the shapes above
#      already own those, and three documented workarounds for what LinkML
#      generates (scripts/gen_merged_shacl.py, GENERATOR_WORKAROUNDS).
#
# The controlled vocabularies the shapes check against (health-theme.rdf, ...)
# are data that HealthDCAT-AP's validator adds to the graph it validates; they
# are not part of this file.
#
# Source: src/health_dcat_ap_plus/schema/health_dcat_ap_plus.yaml
"""


PREFERRED_PREFIXES = {"http://purl.org/dc/terms/": "dct"}


def relabel_blank_nodes(g: Graph) -> Graph:
    """A copy of `g` whose blank nodes are named by where they sit, not by
    rdflib's random labels, so regenerating an unchanged graph gives
    byte-identical Turtle (the random labels made every regeneration a
    ~1500-line diff).

    Blank nodes get b0, b1, ... in the order a walk from the named subjects
    meets them, siblings ordered by a hash of their own content (a Merkle hash:
    predicate and object, recursively). Nodes with identical content get
    distinct labels, so no two blank nodes are ever merged; and the labels do not
    depend on anything but the graph. (rdflib.compare.to_canonical_graph does
    this more generally but does not finish on this graph's 700+ symmetric
    blank nodes.)"""
    hashes: dict = {}

    def key(term) -> str:
        if isinstance(term, BNode):
            return "B" + node_hash(term)
        return ("U" if isinstance(term, URIRef) else "L") + term.n3()

    def node_hash(node: BNode, seen: frozenset = frozenset()) -> str:
        if node not in hashes:
            if node in seen:  # a cycle: not a shape structure; stay deterministic anyway
                return "cycle"
            content = sorted(f"{p.n3()}>{key_in(o, seen | {node})}" for p, o in g.predicate_objects(node))
            hashes[node] = hashlib.sha1("\n".join(content).encode("utf-8")).hexdigest()
        return hashes[node]

    def key_in(term, seen: frozenset) -> str:
        return ("B" + node_hash(term, seen)) if isinstance(term, BNode) else key(term)

    def ordered(node) -> list:
        return sorted(g.predicate_objects(node), key=lambda po: (str(po[0]), key(po[1])))

    labels: dict = {}

    def visit(node) -> None:
        if isinstance(node, BNode) and node not in labels:
            labels[node] = BNode(f"b{len(labels)}")
            for _p, o in ordered(node):
                visit(o)

    for subject in sorted({s for s in g.subjects() if not isinstance(s, BNode)}, key=str):
        for _p, o in ordered(subject):
            visit(o)
    for leftover in sorted({s for s in g.subjects() if isinstance(s, BNode)}, key=node_hash):
        visit(leftover)

    def relabel(term):
        return labels.get(term, term)

    # Which of several prefixes for one namespace rdflib keeps (dct from the
    # official files, dcterms from its own defaults and from LinkML) depends on
    # set order when graphs are added, so the prefix is chosen here instead.
    prefix_of: dict = {str(namespace): prefix for prefix, namespace in sorted(g.namespaces())}
    for namespace, prefix in PREFERRED_PREFIXES.items():
        if namespace in prefix_of:
            prefix_of[namespace] = prefix
    out = Graph(bind_namespaces="none")
    for namespace, prefix in sorted(prefix_of.items(), key=lambda item: item[1]):
        out.bind(prefix, namespace)
    for s, p, o in sorted(((relabel(s), p, relabel(o)) for s, p, o in g), key=lambda t: tuple(x.n3() for x in t)):
        out.add((s, p, o))
    return out


def serialize_canonical(g: Graph) -> str:
    return relabel_blank_nodes(g).serialize(format="turtle")


def main() -> None:
    g = build_merged_shapes_graph()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(LICENSE_HEADER + "\n" + serialize_canonical(g), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({len(g)} triples)")


if __name__ == "__main__":
    sys.exit(main())

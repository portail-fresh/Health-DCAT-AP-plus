"""Real SHACL validation of a comprehensive HealthDataset instance.

tests/test_data.py only checks that example data *loads* against the
generated dataclasses -- a JSON-schema-derived check that can't see most of
what real SHACL enforces (nodeKind/IRI-vs-literal, sh:class membership,
sh:hasValue, cardinality across nested shapes, ...). This module instead
dumps a comprehensive HealthDataset instance to real RDF and validates it
with pyshacl, against three shape graphs:

  * our own generated SHACL (does the schema's own SHACL hang together?)
  * HealthDCAT-AP's official shapes AS ITS VALIDATOR ASSEMBLES THEM: the
    non-public tier files plus the DCAT-AP 3.0.0 shapes they owl:import (does
    the dataset portion conform to the spec it was ported from, independent of
    the port script's choices?)
  * the ONE merged shapes graph this repo publishes (official shapes + our own
    for everything they don't cover, see scripts/gen_merged_shacl.py)

and the same two last graphs against HealthDCAT-AP's own worked example and
against the example file this repo publishes. The data graph gets what the
official validator gives it: the vocabulary catalogue (restricted to the terms
the data refers to, for speed) and the DPV terms its catalogue lacks.

Each test compares the exact set of result *signatures* (severity, constraint
component, result path) against an explicit, commented allowlist -- so a new
result fails the test (a real regression), and a known one disappearing also
fails it (a prompt to prune the allowlist), instead of either silently
passing or silently accumulating noise. See docs/architecture-verification.md
for the narrative behind each entry.
"""

import functools
import sys
from pathlib import Path
from typing import FrozenSet

import pytest
import yaml
from linkml_merge_toolkit.shacl_merge import targeted_classes
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from rdflib import FOAF, SKOS, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS

import health_dcat_ap_plus.datamodel.health_dcat_ap_plus as dm

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import gen_merged_shacl  # noqa: E402
import validation_support as vs  # noqa: E402

SCHEMA_PATH = REPO_ROOT / "src" / "health_dcat_ap_plus" / "schema" / "health_dcat_ap_plus.yaml"
FIXTURE_PATH = Path(__file__).parent / "data" / "problem" / "valid" / "HealthDataset-shacl-full.yaml"
PUBLISHED_EXAMPLE_PATH = REPO_ROOT / "examples" / "HealthDataset-full-example.ttl"
OFFICIAL_EXAMPLE_PATH = REPO_ROOT / "examples" / "reference" / "example-healthdcat-dataset.ttl"
# Where the official shapes and the validator's vocabulary catalogue live (and
# which release that is) is decided once, in scripts/gen_merged_shacl.py.
HEALTHDCATAP_SHACL_DIR = gen_merged_shacl.HEALTHDCATAP_SHACL_DIR
# Sciensano's hosted validator (https://healthdcat-validator.sciensano.be) is an
# ITB instance whose exact config is checked into the official repo, in the same
# `ehds` folder as the shapes: config.properties lists the shape files (the ones
# in gen_merged_shacl.OFFICIAL_SHAPE_FILES plus release 8's graph-guard.ttl),
# `validator.preloadOwlImports = true`, and an owlImportMapping that maps every
# owl:import -- the DCAT-AP shapes and the vocabulary catalogue below -- to a
# local file. Release 8 moved the catalogue's HealthDCAT-AP vocabularies from the
# acceptance environment to the production one (hdeu-dcat.data.health.europa.eu).
OFFICIAL_VOCABULARY_CATALOGUE_DIR = gen_merged_shacl.OFFICIAL_VOCABULARY_CATALOGUE_DIR

needs_official_clone = pytest.mark.skipif(
    not HEALTHDCATAP_SHACL_DIR.exists(),
    reason=(
        "repos/healthdcat-ap not fetched locally -- see README.md for the pinned commit to fetch into repos/healthdcat-ap"
    ),
)

DCAT = Namespace("http://www.w3.org/ns/dcat#")
Signature = vs.Signature


def _health_dataset(data: dict) -> "dm.HealthDataset":
    """Construct a HealthDataset from fixture data.

    No construction workaround needed beyond one: HealthDataset (and every
    other Health<X> class that narrows a slot's range/multivalued-ness via
    slot_usage) used to crash on construction, because the parent class's
    own generated __post_init__ unconditionally re-processed the
    already-correctly-narrowed value under its own, stale assumption.
    linkml-merge-toolkit's post_init_shielding module
    (https://github.com/portail-fresh/linkml-merge-toolkit) now fixes this
    at the generated source level, as a permanent step of `just
    gen-python`/`just gen-project`.

    The one remaining step: was_generated_by's declared range is plain
    DataGeneratingActivity (dcat-ap-plus's own class, no qualified_association
    field at all), so HealthDataset's own _normalize_inlined_as_list(slot_type=
    DataGeneratingActivity, ...) would reject the qualified_association key in
    the fixture's entries outright. Each entry is pre-constructed as a real
    AssociatedDataGeneratingActivity instance instead (a DataGeneratingActivity
    subclass defined in health_dcat_ap_plus.yaml): _normalize_inlined_as_list's
    own isinstance(list_entry, slot_type) fast path preserves an already-built
    instance as-is. That is substituting a subclass instance for a field the
    schema deliberately doesn't narrow, not a __post_init__-shielding case.
    """
    data = dict(data)
    data["was_generated_by"] = [dm.AssociatedDataGeneratingActivity(**entry) for entry in data["was_generated_by"]]
    return dm.HealthDataset(**data)


def _build_test_dataset_graph() -> Graph:
    """The fixture's RDF graph, via the real dataclass -> rdflib_dumper path,
    as a self-contained document in HealthDCAT-AP's own style:

      * the dataset's dct:source is described in the same graph. DCAT-AP's shape
        requires a dct:source value to be a dcat:Dataset (sh:class), and a
        dcat:Dataset has to satisfy the dataset shapes, so a bare URI -- what the
        spec's usage note ("the source Dataset must be fully described") suggests
        and what this fixture used to carry, when only HealthDCAT-AP's own five
        files were checked -- is not conformant in a graph on its own. The source
        dataset is a second HealthDataset built from the same fixture.
      * external terms are typed inline (vs.OFFICIAL_CONVENTION_TERM_TYPES).
    """
    data = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
    source_id = data["source"][0]
    source_data = {k: v for k, v in data.items() if k != "source"}
    source_data.update(
        id=source_id,
        title=["Hospital case reports 2024"],
        identifier=[source_id],
        description=["The hospital case reports the registry's diagnoses are collected from."],
    )

    sv = SchemaView(str(SCHEMA_PATH))
    graph = rdflib_dumper.as_rdf_graph(_health_dataset(data), schemaview=sv)
    graph += rdflib_dumper.as_rdf_graph(_health_dataset(source_data), schemaview=sv)
    return vs.add_official_convention_term_types(graph)


def _own_generated_shapes_graph() -> Graph:
    return gen_merged_shacl.generate_own_shapes_graph(SCHEMA_PATH)


# ---------------------------------------------------------------------------
# Guard: no unexpanded CURIEs in anything we generate
# ---------------------------------------------------------------------------
# LinkML's generators don't carry an imported schema's prefixes into their
# output (linkml/linkml#3574, #3933), so a prefix the root schema's own
# `prefixes:` block doesn't redeclare comes out as a raw "prefix:local"
# string used as if it were an IRI. Before LinkML 1.12 that was silent: still
# a parseable IRI, just a wrong one (our schema:DefinedTerm shape quietly
# escaped gen_merged_shacl's exclusion list, which names the real
# http://schema.org/DefinedTerm). Since 1.12 it can be loud in the worst way:
# ShaclGenerator.serialize() canonicalises through pyoxigraph, which rejects
# the IRI outright when the prefix label isn't a legal URI scheme
# (dcat-ap-plus v0.1.0rc5's dcatap_plus: -- an underscore), and the rdflib
# fallback it then drops to did not finish on this graph, so generation
# stalls instead of failing. These tests build the graph with as_graph()
# (no canonicalisation) so a regression is reported rather than hung on, and
# `just test` runs them first (_test-iris), before anything calls serialize().
_SCHEMES_WITHOUT_AUTHORITY = frozenset({"urn", "mailto", "tel"})


def _unexpanded_iris(graph: Graph) -> list:
    """Every IRI in `graph` that is a CURIE nobody expanded: a legitimate
    absolute IRI here has a `scheme://` authority part (the only exceptions
    this schema family emits are urn:/mailto:/tel: ones)."""
    bad = set()
    for triple in graph:
        for term in triple:
            if isinstance(term, URIRef):
                iri = str(term)
                if "://" not in iri and iri.split(":", 1)[0] not in _SCHEMES_WITHOUT_AUTHORITY:
                    bad.add(iri)
    return sorted(bad)


def _assert_no_unexpanded_iris(graph: Graph, what: str) -> None:
    bad = _unexpanded_iris(graph)
    assert not bad, (
        f"{what} contains {len(bad)} unexpanded CURIE(s) used as IRIs: {bad}. A prefix some imported "
        "schema declares is missing from the root schema's own prefixes: block "
        "(src/health_dcat_ap_plus/schema/health_dcat_ap_plus.yaml) -- LinkML does not propagate imported "
        "prefixes into generated output. Declare each missing prefix there (and in the PREFIXES dict of "
        "scripts/port_healthdcat_ap_shacl_to_linkml.py)."
    )


def test_own_generated_shacl_has_no_unexpanded_iris():
    _assert_no_unexpanded_iris(_own_generated_shapes_graph(), "the generated SHACL")


def test_dumped_instance_rdf_has_no_unexpanded_iris():
    # The data side of the same gap: rdflib_dumper types instances through
    # the same namespace table, so a missing prefix shows up as `a <rdfs:Resource>`.
    _assert_no_unexpanded_iris(_build_test_dataset_graph(), "the dumped example instance graph")


# ---------------------------------------------------------------------------
# What the official validator gives the data graph (scripts/validation_support.py)
# ---------------------------------------------------------------------------
REAL_VOCABULARY_TERMS_PATH = Path(__file__).parent / "data" / "real_vocabulary_terms.ttl"


@functools.cache
def _official_vocabulary_catalogue_graph() -> Graph:
    """Sciensano's cached vocabulary catalogue (see the comment on
    OFFICIAL_VOCABULARY_CATALOGUE_DIR); cached because it takes ~10 s to parse
    and tests only read it."""
    return vs.load_vocabulary_catalogue(OFFICIAL_VOCABULARY_CATALOGUE_DIR)


def _with_official_environment(document: Graph) -> Graph:
    """`document` plus what the official validator adds to it."""
    return vs.with_official_environment(document, _official_vocabulary_catalogue_graph(), REAL_VOCABULARY_TERMS_PATH)


_validate = vs.validate
_assert_known_violations = vs.assert_known_violations


def _official_shapes_graph() -> Graph:
    """HealthDCAT-AP's official shapes, assembled as its validator does (see
    gen_merged_shacl.load_official_shapes_graph)."""
    return gen_merged_shacl.load_official_shapes_graph()


def _merged_shapes_graph() -> Graph:
    """The ONE production shapes graph, rebuilt in memory so it can never
    silently go stale (test_committed_merged_shacl_is_current compares it with
    the committed file). See scripts/gen_merged_shacl.py's docstring. Built
    afresh each time: pyshacl adds triples to the shapes graph it is given, which
    would leak from one test into the next (and into the comparison with the
    committed file); it takes about a second."""
    return gen_merged_shacl.build_merged_shapes_graph()


# ---------------------------------------------------------------------------
# Allowlists
# ---------------------------------------------------------------------------
# Our own generated shapes alone (open, with none of the merge's exclusions or
# workarounds), against the dumped fixture. These are properties of what LinkML
# generates from a schema whose classes share class_uris and slot_uris -- the
# very reasons the merged shapes graph exists -- so they are expected, and each
# is neutralised in the merged graph (the "Merged:" line of each entry).
KNOWN_OWN_SHAPES_VIOLATIONS: FrozenSet[Signature] = frozenset(
    {
        # rdf:type vs the classifier slot: dcat-ap-plus's ClassifierMixin.rdf_type
        # has slot_uri rdf:type, so Activity/Entity/AgenticEntity/Plan shapes
        # carry `sh:path rdf:type; sh:class schema:DefinedTerm`, which the
        # class-typing triple of every node violates. linkml/linkml#3931,
        # nfdi-de/dcat-ap-plus#110. Merged: drop_rdf_type_property_shapes.
        ("Violation", "ClassConstraintComponent", "type"),
        # QualitativeAttribute requires `value` (prov:value) and shares class_uri
        # prov:Entity with Entity, EvaluatedEntity and AnalysisSourceData, which
        # LinkML folds into one NodeShape -- so the minCount lands on every
        # prov:Entity. linkml/linkml#3932. Merged: relax_required_prov_value.
        ("Violation", "MinCountConstraintComponent", "value"),
        # Two slots, is_about_entity and is_about_activity, share
        # slot_uri dcterms:subject, so the dcat:Dataset shape has two property
        # shapes on that path (sh:class prov:Entity, sh:class prov:Activity) that
        # no one value satisfies. Merged: not present -- dcat:Dataset's shapes are
        # the official ones.
        ("Violation", "ClassConstraintComponent", "subject"),
        # HealthAgent requires cv:contactPoint and shares class_uri foaf:Agent with
        # Agent, so the requirement lands on every foaf:Agent -- including the
        # plain Agent of a DatasetAttribution. Merged: not present -- foaf:Agent's
        # shape is DCAT-AP's, HealthAgent's rule the official dataset shape's.
        ("Violation", "MinCountConstraintComponent", "contactPoint"),
        # Test-data artifact, not a defect: dcat-ap-plus checks a dataset's theme
        # with sh:class skos:Concept, and the dump types no vocabulary term as a
        # skos:Concept (the vocabulary catalogue does, and is not loaded for this
        # test: our shapes for Concept and the like would object to its content).
        ("Violation", "ClassConstraintComponent", "theme"),
    }
)

# What is left against the official shapes, and against the merged shapes, for
# the fixture: warnings only, for RECOMMENDED properties the fixture does not
# fill (the official example fills all of these but dct:source, which it never
# uses on the dataset). No violation: this is the statement "the fixture
# conforms". The distributions lack availability, description, format and
# license (two datasets x three distributions), the datasets a publisher, the
# source dataset a dct:source of its own, and the agents (hdab, hdab coordinator,
# custodian, ...) a dct:type from the publisher-type table.
KNOWN_FIXTURE_WARNINGS: FrozenSet[Signature] = frozenset(
    {
        ("Warning", "MinCountConstraintComponent", "availability"),
        ("Warning", "MinCountConstraintComponent", "description"),
        ("Warning", "MinCountConstraintComponent", "format"),
        ("Warning", "MinCountConstraintComponent", "license"),
        ("Warning", "MinCountConstraintComponent", "publisher"),
        ("Warning", "MinCountConstraintComponent", "source"),
        ("Warning", "MinCountConstraintComponent", "type"),
    }
)

# HealthDCAT-AP's own example against its own shapes (and ours): no violation.
# The warnings are its country (Belgium, typed dct:Location) without a bounding
# box or centroid, and no dct:source on the dataset.
KNOWN_OFFICIAL_EXAMPLE_WARNINGS: FrozenSet[Signature] = frozenset(
    {
        ("Warning", "MinCountConstraintComponent", "bbox"),
        ("Warning", "MinCountConstraintComponent", "centroid"),
        ("Warning", "MinCountConstraintComponent", "source"),
    }
)


def test_dataset_conforms_to_own_generated_shacl():
    _assert_known_violations(
        _validate(_build_test_dataset_graph(), _own_generated_shapes_graph()), KNOWN_OWN_SHAPES_VIOLATIONS
    )


@needs_official_clone
def test_dataset_conforms_to_official_healthdcat_ap_shacl():
    data = _with_official_environment(_build_test_dataset_graph())
    _assert_known_violations(_validate(data, _official_shapes_graph()), KNOWN_FIXTURE_WARNINGS)


@needs_official_clone
def test_dataset_conforms_to_merged_shacl():
    """The end-to-end check: does a real HealthDataset instance conform to
    the ONE shapes graph a real downstream user would actually validate
    against, with nothing the official shapes alone don't also say?"""
    data = _with_official_environment(_build_test_dataset_graph())
    _assert_known_violations(_validate(data, _merged_shapes_graph()), KNOWN_FIXTURE_WARNINGS)


@needs_official_clone
@pytest.mark.parametrize("shapes", ["official", "merged"])
def test_official_example_conforms(shapes):
    """HealthDCAT-AP's own comprehensive example (vendored at examples/reference/)
    against the official shapes, and -- the point of the merge -- against the
    merged shapes with the same result: our additions must not reject data the
    official validator accepts."""
    document = Graph().parse(str(OFFICIAL_EXAMPLE_PATH), format="turtle")
    shapes_graph = _official_shapes_graph() if shapes == "official" else _merged_shapes_graph()
    _assert_known_violations(_validate(_with_official_environment(document), shapes_graph), KNOWN_OFFICIAL_EXAMPLE_WARNINGS)


@needs_official_clone
def test_published_example_conforms_to_merged_shacl():
    """examples/HealthDataset-full-example.ttl is what readers copy: it has to
    validate as the fixture does (regenerate it with scripts/gen_example.py)."""
    document = Graph().parse(str(PUBLISHED_EXAMPLE_PATH), format="turtle")
    _assert_known_violations(_validate(_with_official_environment(document), _merged_shapes_graph()), KNOWN_FIXTURE_WARNINGS)


@needs_official_clone
def test_committed_merged_shacl_is_current():
    """docs/schema/health_dcat_ap_plus.merged-shacl.ttl is committed (it is what
    people import); if the schema, the clone or the script changed without it
    being regenerated, this fails -- run `just gen-shacl`."""
    expected = gen_merged_shacl.LICENSE_HEADER + "\n" + gen_merged_shacl.serialize_canonical(_merged_shapes_graph())
    assert gen_merged_shacl.OUTPUT_PATH.read_text(encoding="utf-8") == expected


# ---------------------------------------------------------------------------
# The merge itself
# ---------------------------------------------------------------------------
@needs_official_clone
def test_official_shapes_include_the_imported_dcat_ap_shapes():
    """The official files are a delta: Dataset_Shape of DCAT-AP 3.0.0 is
    extended, not redefined. Loaded without the imports, a bare dcat:Dataset
    gets no dct:title requirement at all."""
    shapes = _official_shapes_graph()
    sh = Namespace("http://www.w3.org/ns/shacl#")
    required = {
        path
        for shape in shapes.subjects(sh.targetClass, DCAT.Dataset)
        for ps in shapes.objects(shape, sh.property)
        for path in shapes.objects(ps, sh.path)
        if (ps, sh.minCount, None) in shapes
    }
    assert DCTERMS.title in required and DCTERMS.description in required


@needs_official_clone
def test_exclusion_list_holds_only_judgment_calls():
    """EXTERNAL_VOCABULARY_STUB_CLASSES is what is left after everything the
    official shapes target is derived: nothing in it may already be derived (it
    would be redundant) and every entry must still be a class our shapes
    generate (else it is stale)."""
    official = _official_shapes_graph()
    derived = targeted_classes(official)
    listed = {URIRef(c) for c in gen_merged_shacl.EXTERNAL_VOCABULARY_STUB_CLASSES}
    assert not listed & derived, f"already derived from the official shapes: {sorted(listed & derived)}"
    ours = targeted_classes(_own_generated_shapes_graph())
    assert not listed - ours, f"no longer generated by the schema: {sorted(listed - ours)}"
    excluded = gen_merged_shacl.excluded_target_classes(official)
    assert {FOAF.Agent, SKOS.Concept, SKOS.ConceptScheme} <= excluded


@needs_official_clone
def test_merged_shapes_are_open():
    """LinkML closes generated shapes by default; a closed shape rejects the
    properties the official example puts on the nodes it constrains."""
    assert (None, Namespace("http://www.w3.org/ns/shacl#").closed, Literal(True)) not in _merged_shapes_graph()


def test_blank_node_relabelling_is_stable_and_lossless():
    shapes = _own_generated_shapes_graph()
    relabelled = gen_merged_shacl.relabel_blank_nodes(shapes)
    again = gen_merged_shacl.relabel_blank_nodes(relabelled)
    assert len(relabelled) == len(shapes)
    assert relabelled.serialize(format="turtle") == again.serialize(format="turtle")

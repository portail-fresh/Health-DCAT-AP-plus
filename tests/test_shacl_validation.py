"""Real SHACL validation of a comprehensive HealthDataset instance.

tests/test_data.py only checks that example data *loads* against the
generated dataclasses -- a JSON-schema-derived check that can't see most of
what real SHACL enforces (nodeKind/IRI-vs-literal, sh:class membership,
sh:hasValue, cardinality across nested shapes, ...). This module instead
dumps a comprehensive HealthDataset instance to real RDF and validates it
with pyshacl, against two different shape graphs:

  * our own generated SHACL (does the merge layer's own schema hang
    together, self-consistently?)
  * HealthDCAT-AP's real, official upstream SHACL files, cloned locally at
    repos/healthdcat-ap (does the *dataset* portion of the merge conform to
    the spec it was ported from, independent of our own port script's
    choices?)

Both runs currently produce real, already-diagnosed violations -- some are
genuine bugs in this repo's port (tracked below, to be fixed), one is a
genuine bug in HealthDCAT-AP's own upstream shapes (worked around, not
fixed -- not ours to fix), and some are artifacts of the test fixture itself
(e.g. DPV/DQV term IRIs that would need the real DPV/DQV ontologies loaded
for class-membership reasoning, which this fixture doesn't attempt). Rather
than requiring conformance outright, each test compares the exact set of
violation *signatures* (severity, constraint component, result path) against
an explicit, commented allowlist below -- so a genuinely new violation fails
the test (a real regression), and fixing a known one also fails the test
(a prompt to prune the allowlist), instead of either silently passing or
silently accumulating new noise. See docs/architecture-verification.md for
the full narrative.
"""

from pathlib import Path
from typing import FrozenSet, Tuple

import pyshacl
import pytest
import yaml
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from rdflib import Graph, Namespace

import health_dcat_ap_plus.datamodel.health_dcat_ap_plus as dm

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = (
    REPO_ROOT / "src" / "health_dcat_ap_plus" / "schema" / "health_dcat_ap_plus.yaml"
)
FIXTURE_PATH = (
    Path(__file__).parent / "data" / "problem" / "valid" / "HealthDataset-shacl-full.yaml"
)
HEALTHDCATAP_SHACL_DIR = (
    REPO_ROOT / "repos" / "healthdcat-ap" / "public" / "releases" / "release-7" / "html" / "shacl"
)

SH = Namespace("http://www.w3.org/ns/shacl#")

Signature = Tuple[str, str, str]


def _build_test_dataset_graph() -> Graph:
    """Build the fixture's RDF graph via the real dataclass -> rdflib_dumper path.

    Needs one workaround: HealthDataset.__post_init__ (in the generated
    health_dcat_ap_plus.py) correctly normalizes `frequency` as its own
    multivalued list, then unconditionally calls
    super().__post_init__(**kwargs) -- Dataset's own, still-single-valued
    frequency logic -- which re-processes the now-list value and crashes
    (TypeError: ...Frequency() argument after ** must be a mapping, not
    list). This is a real, pre-existing LinkML code-gen limitation (a
    subclass narrowing a slot's multivalued-ness via slot_usage doesn't stop
    the parent's own __post_init__ from re-applying its own, different
    assumption) -- not something this repo's schema or port script caused or
    can fix structurally, so it's worked around here at construction time:
    the generated module's `as_dict` is monkeypatched, for the duration of
    one construction call only, to treat a single-item list of an
    already-constructed object as that object's own dict -- letting
    Dataset.__post_init__'s stale single-value branch succeed as a no-op
    instead of crashing.
    """
    data = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))

    real_as_dict = dm.as_dict

    def _patched_as_dict(obj):
        if isinstance(obj, list) and len(obj) == 1 and hasattr(obj[0], "__dict__"):
            return dict(obj[0].__dict__)
        return real_as_dict(obj)

    dm.as_dict = _patched_as_dict
    try:
        obj = dm.HealthDataset(**data)
    finally:
        dm.as_dict = real_as_dict

    sv = SchemaView(str(SCHEMA_PATH))
    return rdflib_dumper.as_rdf_graph(obj, schemaview=sv)


def _own_generated_shapes_graph() -> Graph:
    ttl = ShaclGenerator(str(SCHEMA_PATH)).serialize()
    g = Graph()
    g.parse(data=ttl, format="turtle")
    return g


# Real upstream typo (confirmed via grep across every copy of these files in
# the release-7 tree): deprecateduris.ttl, range.ttl and
# mdr-vocabularies.shape.ttl all declare `dcatap: <http://data.europa.eu/r5r>`
# (missing the trailing slash), while non-public-shapes*.ttl -- and every
# copy of all three files under the vendored HealthDCAT-AP_validator/ tree --
# correctly declare `<http://data.europa.eu/r5r/>`. Same fix already applied
# in scripts/port_healthdcat_ap_shacl_to_linkml.py's
# _KNOWN_UPSTREAM_PREFIX_FIXES.
_BROKEN_DCATAP_PREFIX = "@prefix dcatap: <http://data.europa.eu/r5r> ."
_FIXED_DCATAP_PREFIX = "@prefix dcatap: <http://data.europa.eu/r5r/> ."

_REAL_SHAPE_FILES = [
    "non-public-shapes.ttl",
    "non-public-shapes_recommended.ttl",
    "range.ttl",
    "mdr-vocabularies.shape.ttl",
    "deprecateduris.ttl",
]


def _real_healthdcat_ap_shapes_graph() -> Graph:
    """Load HealthDCAT-AP's own real, official upstream SHACL shapes (non-public tier).

    imports.ttl / mdr_imports.ttl are deliberately not included -- read
    directly, they contain only owl:imports metadata triples, no sh:
    shapes at all.
    """
    g = Graph()
    for fname in _REAL_SHAPE_FILES:
        text = (HEALTHDCATAP_SHACL_DIR / fname).read_text(encoding="utf-8")
        if _BROKEN_DCATAP_PREFIX in text:
            text = text.replace(_BROKEN_DCATAP_PREFIX, _FIXED_DCATAP_PREFIX)
        g.parse(data=text, format="turtle")

    # Real bug in HealthDCAT-AP's own non-public-shapes.ttl: Dataset_Shape's
    # "if hasStructuredData is true, must have hasVariables" conditional is
    # built as a bare sh:or used directly as an sh:property value, with no
    # sh:path -- not a well-formed SHACL PropertyShape (a PropertyShape used
    # as an sh:property value MUST declare exactly one sh:path). Strict
    # processors (pyshacl included, in advanced mode) reject the *entire*
    # shapes file because of this one shape. Not our file to fix -- worked
    # around by dropping just that one triple so the rest of the real shapes
    # can still be checked; the conditional constraint it carried goes
    # unenforced by this test. If this assertion ever fires, the upstream
    # file changed shape -- re-diagnose before trusting the workaround.
    removed = [
        (s, p, o)
        for s, p, o in g.triples((None, SH.property, None))
        if (o, SH.path, None) not in g
    ]
    assert len(removed) == 1, (
        f"expected exactly 1 malformed sh:property (Dataset_Shape's "
        f"hasStructuredData/hasVariables sh:or missing sh:path) in "
        f"non-public-shapes.ttl, found {len(removed)} -- upstream shapes "
        "changed, re-diagnose before trusting this workaround"
    )
    for triple in removed:
        g.remove(triple)
    return g


def _violation_signatures(results_graph: Graph) -> FrozenSet[Signature]:
    """Reduce a pyshacl results graph to a stable (severity, component, path) set.

    Blank node identities and nested sh:detail results aren't stable across
    runs; (severity, sourceConstraintComponent, resultPath) is what's stable
    and meaningful for regression-comparing two runs of the same fixture.
    """
    query = """
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?severity ?component ?path WHERE {
        ?result a sh:ValidationResult ;
            sh:resultSeverity ?severity ;
            sh:sourceConstraintComponent ?component .
        OPTIONAL { ?result sh:resultPath ?path }
    }
    """
    sigs = set()
    for row in results_graph.query(query):
        severity = str(row.severity).rsplit("#", 1)[-1]
        component = str(row.component).rsplit("#", 1)[-1]
        path = str(row.path).rsplit("#", 1)[-1].rsplit("/", 1)[-1] if row.path else "(none)"
        sigs.add((severity, component, path))
    return frozenset(sigs)


def _assert_known_violations(actual: FrozenSet[Signature], known: FrozenSet[Signature]) -> None:
    new = actual - known
    stale = known - actual
    assert not new, (
        "New, previously unseen SHACL violation(s) -- a real regression, or "
        f"the fixture/schema changed on purpose (update the allowlist): {sorted(new)}"
    )
    assert not stale, (
        "Previously-known violation(s) no longer occur -- if a real bug got "
        f"fixed, prune these from the allowlist: {sorted(stale)}"
    )


# ---------------------------------------------------------------------------
# Violations against OUR OWN generated SHACL (src/.../healthdcat_ap_non_public.yaml
# + health_dcat_ap_plus.yaml). Found 2026-08-21, see
# docs/architecture-verification.md.
# ---------------------------------------------------------------------------
KNOWN_OWN_SHAPES_VIOLATIONS: FrozenSet[Signature] = frozenset(
    {
        # Real, structural port bug: dcterms:relation/source/conformsTo are
        # ported as plain strings, but the generated shape for each stacks
        # sh:class + sh:nodeKind + sh:datatype constraints (all three fire
        # here). Root cause: dcat-ap-plus reuses each of these predicate
        # URIs across several of its own slots (e.g. dcterms:relation alone
        # maps to has_qualitative_attribute / has_quantitative_attribute /
        # related_resource / relation), and the port script's
        # URI->slot-name resolution can only remember one candidate per
        # URI -- it picked (or fell through to) the wrong one, and SHACL's
        # shape-merging-by-predicate then surfaces the conflict between our
        # port's typing and dcat-ap-plus's own. To fix: make
        # property_name_for class-context-aware, or hand-pick the right
        # existing slot per field.
        ("Violation", "ClassConstraintComponent", "relation"),
        ("Violation", "ClassConstraintComponent", "source"),
        ("Violation", "ClassConstraintComponent", "conformsTo"),
        ("Violation", "NodeKindConstraintComponent", "relation"),
        ("Violation", "NodeKindConstraintComponent", "source"),
        ("Violation", "NodeKindConstraintComponent", "conformsTo"),
        ("Violation", "DatatypeConstraintComponent", "relation"),
        ("Violation", "DatatypeConstraintComponent", "source"),
        ("Violation", "DatatypeConstraintComponent", "conformsTo"),
        # Real, not-yet-diagnosed: EvaluatedEntity (used as is_about_entity's
        # range) requires prov:value, which the fixture's population entity
        # doesn't supply. Need to determine whether prov:value truly belongs
        # on EvaluatedEntity or bled in from a sibling class.
        ("Violation", "MinCountConstraintComponent", "value"),
        # Same predicate-URI-collision family as relation/source/conformsTo
        # above, confirmed by checking dcat-ap-plus's own schema: hasLegalBasis
        # -> dpv:hasLegalBasis, hasPersonalData -> dpv:hasPersonalData,
        # hasPurpose -> dpv:hasPurpose, hasQualityAnnotation ->
        # dqv:hasQualityAnnotation, and "type" all carry sh:class
        # constraints our port's own value (a bare term IRI, per
        # HealthDCAT-AP's real qualifiedAttribution-style usage) doesn't
        # satisfy without the real DPV/DQV ontologies loaded for
        # class-membership reasoning -- same underlying issue as the
        # test-fixture-artifact entries in KNOWN_REAL_SHAPES_VIOLATIONS
        # below, just surfacing here via our own generated shapes instead.
        ("Violation", "ClassConstraintComponent", "hasLegalBasis"),
        ("Violation", "ClassConstraintComponent", "hasPersonalData"),
        ("Violation", "ClassConstraintComponent", "hasPurpose"),
        ("Violation", "ClassConstraintComponent", "hasQualityAnnotation"),
        ("Violation", "ClassConstraintComponent", "subject"),
        ("Violation", "ClassConstraintComponent", "type"),
        # Already-known, separate, pre-existing LinkML code-gen bug (same
        # class as the frequency multivalued-narrowing crash worked around
        # in _build_test_dataset_graph): HealthDataset.temporal_resolution
        # ends up serialized as a Python list's repr baked into one
        # xsd:duration literal ("['P1D']") instead of one duration value --
        # not yet root-caused, tracked separately, not fixed here.
        ("Violation", "DatatypeConstraintComponent", "temporalResolution"),
        # Not yet independently diagnosed as a real bug vs. pyshacl/rdflib
        # strictness. Plain RDF literals are xsd:string by RDF 1.1
        # semantics, so the string-valued ones below look like they might
        # just be pyshacl being stricter than that -- but startDate/endDate/
        # hasStructuredData/maxTypicalAge/minTypicalAge/numberOfRecords/
        # numberOfUniqueIndividuals are already explicitly typed literals
        # in the dump (xsd:date/xsd:boolean/xsd:nonNegativeInteger) and
        # still fail, which is a genuine open question, not yet explained.
        ("Violation", "DatatypeConstraintComponent", "title"),
        ("Violation", "DatatypeConstraintComponent", "description"),
        ("Violation", "DatatypeConstraintComponent", "identifier"),
        ("Violation", "DatatypeConstraintComponent", "keyword"),
        ("Violation", "DatatypeConstraintComponent", "email"),
        ("Violation", "DatatypeConstraintComponent", "name"),
        ("Violation", "DatatypeConstraintComponent", "hasCodeValues"),
        ("Violation", "DatatypeConstraintComponent", "populationCoverage"),
        ("Violation", "DatatypeConstraintComponent", "prefLabel"),
        ("Violation", "DatatypeConstraintComponent", "hasEmail"),
        ("Violation", "DatatypeConstraintComponent", "startDate"),
        ("Violation", "DatatypeConstraintComponent", "endDate"),
        ("Violation", "DatatypeConstraintComponent", "hasStructuredData"),
        ("Violation", "DatatypeConstraintComponent", "maxTypicalAge"),
        ("Violation", "DatatypeConstraintComponent", "minTypicalAge"),
        ("Violation", "DatatypeConstraintComponent", "numberOfRecords"),
        ("Violation", "DatatypeConstraintComponent", "numberOfUniqueIndividuals"),
    }
)


# ---------------------------------------------------------------------------
# Violations against HealthDCAT-AP's own real, official upstream SHACL.
# Found 2026-08-21, see docs/architecture-verification.md.
# ---------------------------------------------------------------------------
KNOWN_REAL_SHAPES_VIOLATIONS: FrozenSet[Signature] = frozenset(
    {
        # Real, structural port bug (systemic): every values_from-bound slot
        # we ported (theme, health_category, health_theme, access_rights,
        # frequency, has_coding_system, language, type, conforms_to) keeps
        # its class-object range (Concept/RightsStatement/Frequency/
        # Standard/...) inherited from dcat-ap-plus or added by our own
        # port. The real shapes require bare IRI values for all of them.
        ("Violation", "NodeKindConstraintComponent", "healthCategory"),
        ("Violation", "NodeKindConstraintComponent", "hasCodingSystem"),
        ("Violation", "NodeKindConstraintComponent", "healthTheme"),
        ("Violation", "NodeKindConstraintComponent", "language"),
        ("Violation", "NodeKindConstraintComponent", "accrualPeriodicity"),
        ("Violation", "NodeKindConstraintComponent", "accessRights"),
        ("Violation", "NodeKindConstraintComponent", "conformsTo"),
        ("Violation", "NodeKindConstraintComponent", "theme"),
        ("Violation", "NodeConstraintComponent", "healthCategory"),
        ("Violation", "NodeConstraintComponent", "healthTheme"),
        ("Violation", "NodeConstraintComponent", "theme"),
        ("Violation", "NodeConstraintComponent", "accessRights"),
        ("Violation", "NodeConstraintComponent", "accrualPeriodicity"),
        ("Violation", "NodeConstraintComponent", "hasCodingSystem"),
        ("Violation", "NodeConstraintComponent", "language"),
        ("Violation", "NodeConstraintComponent", "conformsTo"),
        ("Warning", "NodeConstraintComponent", "type"),
        ("Warning", "NodeKindConstraintComponent", "type"),
        # dct:accessRights specifically: the real shape wants
        # sh:hasValue <.../access-right/NON_PUBLIC> exactly -- a fixed
        # single term, not a free RightsStatement object at all (a special
        # case beyond just "should be an IRI").
        ("Violation", "HasValueConstraintComponent", "accessRights"),
        # dcat:theme specifically: the real shape requires including the
        # fixed <.../data-theme/HEAL> term (mdr-vocabularies.shape.ttl,
        # sh:Violation severity -- required, not just recommended).
        ("Violation", "HasValueConstraintComponent", "theme"),
        # Real, structural port bug: HealthAgent / HealthPublisherAgent
        # (hdab, custodian, publisher) reuse dcat-ap-plus's own
        # contact_point slot, hardwired to dcat:contactPoint. The real
        # HealthAgent_Shape requires cv:contactPoint (the m8g Core
        # Vocabulary predicate) instead -- a different predicate for
        # Agent-typed contact points than for Dataset/Distribution's own.
        ("Violation", "NodeConstraintComponent", "hdab"),
        ("Violation", "NodeConstraintComponent", "custodian"),
        ("Violation", "ClassConstraintComponent", "hdab"),
        ("Violation", "MinCountConstraintComponent", "contactPoint"),
        # Already-known from the self-shapes pass, now independently
        # reconfirmed: the plain Dataset-level contact_point's
        # vcard:hasEmail must be an IRI (mailto:...), not a string literal.
        ("Violation", "NodeKindConstraintComponent", "hasEmail"),
        # Test-fixture artifacts, not schema bugs: dpv:hasLegalBasis /
        # hasPersonalData / hasPurpose / dqv:hasQualityAnnotation need the
        # real DPV/DQV ontologies loaded (or explicit rdf:type triples on
        # the term IRIs) for sh:class membership checks to pass -- this
        # fixture uses bare term IRIs with no inference.
        ("Violation", "ClassConstraintComponent", "hasLegalBasis"),
        ("Violation", "ClassConstraintComponent", "hasPersonalData"),
        ("Violation", "ClassConstraintComponent", "hasPurpose"),
        ("Violation", "ClassConstraintComponent", "hasQualityAnnotation"),
        # Test-fixture artifacts: the fixture's skos:Concept blank nodes
        # (theme/healthCategory/healthTheme/language/accessRights/
        # accrualPeriodicity/hasCodingSystem) don't carry real EU
        # authority-table skos:inScheme values -- expected to mostly
        # resolve once the vocab-range bug above is fixed and real
        # vocabulary term IRIs are used instead of fabricated Concept
        # objects.
        ("Violation", "MinCountConstraintComponent", "inScheme"),
        ("Violation", "HasValueConstraintComponent", "inScheme"),
    }
)


def test_dataset_conforms_to_own_generated_shacl():
    data_graph = _build_test_dataset_graph()
    shapes_graph = _own_generated_shapes_graph()
    _, results_graph, _ = pyshacl.validate(
        data_graph,
        shacl_graph=shapes_graph,
        data_graph_format="turtle",
        inference="none",
        advanced=True,
    )
    _assert_known_violations(_violation_signatures(results_graph), KNOWN_OWN_SHAPES_VIOLATIONS)


@pytest.mark.skipif(
    not HEALTHDCATAP_SHACL_DIR.exists(),
    reason=(
        "repos/healthdcat-ap not cloned locally -- see README.md's "
        "'git clone --depth 1 https://code.europa.eu/healthdataeu/healthdcat-ap.git "
        "repos/healthdcat-ap' for how to fetch it"
    ),
)
def test_dataset_conforms_to_real_healthdcat_ap_shacl():
    data_graph = _build_test_dataset_graph()
    shapes_graph = _real_healthdcat_ap_shapes_graph()
    _, results_graph, _ = pyshacl.validate(
        data_graph,
        shacl_graph=shapes_graph,
        data_graph_format="turtle",
        inference="none",
        advanced=True,
    )
    _assert_known_violations(_violation_signatures(results_graph), KNOWN_REAL_SHAPES_VIOLATIONS)

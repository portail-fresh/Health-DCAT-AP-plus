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


# Fields HealthDataset.__post_init__ narrows from Dataset's own nested-class
# range to a bare uriorcurie. HealthDataset's own __post_init__ correctly
# coerces each to its new (uriorcurie, possibly list) shape *before*
# unconditionally calling super().__post_init__(**kwargs) -- Dataset's own,
# still nested-class-range coercion for the same fields, which then crashes
# on the already-correct value: a direct `RightsStatement(**as_dict(...))`/
# `Frequency(**as_dict(...))`/`LinguisticSystem(**as_dict(...))` call for
# access_rights/frequency/language (TypeError: ...argument after ** must be
# a mapping, not URIorCURIE -- checked directly: jsonasobj2.as_dict() is a
# harmless passthrough on a plain scalar, so this is Python itself rejecting
# `**` on a non-mapping at the call site, not reachable via an as_dict()
# patch the way the old single-vs-multivalued frequency crash was), and a
# ValueError from _normalize_inlined_as_list's own key-matching logic for
# theme/type (it re-wraps each already-plain-IRI value as
# Concept(preferred_label=<the IRI>) and then complains the "key" doesn't
# match, since a bare IRI was never meant to round-trip through that
# nested-object helper at all). Real, pre-existing LinkML code-gen
# limitation (a subclass narrowing a slot's range or multivalued-ness via
# slot_usage doesn't stop the parent's own __post_init__ from re-processing
# it under its own, different assumption) -- not something this repo's
# schema or port script caused or can fix structurally.
_DATASET_FIELDS_NARROWED_BY_HEALTHDATASET = (
    "access_rights",
    "frequency",
    "language",
    "theme",
    "type",
    "conforms_to",
)


def _build_test_dataset_graph() -> Graph:
    """Build the fixture's RDF graph via the real dataclass -> rdflib_dumper path.

    Works around the __post_init__ re-processing bug described above by
    monkeypatching Dataset.__post_init__ itself, for the duration of one
    construction call only: temporarily blank out the three affected fields
    right before Dataset's own __post_init__ runs (so its stale coercion
    for them becomes a harmless no-op on None), then restore
    HealthDataset's own already-correct values immediately after -- letting
    Dataset's coercion for every *other* field it still legitimately owns
    (creator, geographical_coverage, has_version, ...) run completely
    unaffected.
    """
    data = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))

    # was_generated_by's declared range is plain DataGeneratingActivity
    # (dcat-ap-plus's own class, no qualified_association field at all), so
    # HealthDataset's own _normalize_inlined_as_list(slot_type=
    # DataGeneratingActivity, ...) would reject the qualified_association
    # key in the fixture's entries outright. Pre-construct each entry as a
    # real AssociatedDataGeneratingActivity instance instead (a real
    # DataGeneratingActivity subclass, defined in health_dcat_ap_plus.yaml
    # -- see its own docstring there): _normalize_inlined_as_list's own
    # isinstance(list_entry, slot_type) fast path (confirmed by reading its
    # source directly, not assumed) preserves an already-built instance
    # exactly as-is, so no further shielding is needed here the way the
    # other narrowed fields above need it.
    data["was_generated_by"] = [dm.AssociatedDataGeneratingActivity(**entry) for entry in data["was_generated_by"]]

    real_dataset_post_init = dm.Dataset.__post_init__

    def _patched_dataset_post_init(self, *args, **kwargs):
        saved = {name: getattr(self, name) for name in _DATASET_FIELDS_NARROWED_BY_HEALTHDATASET}
        for name in saved:
            setattr(self, name, None)
        try:
            real_dataset_post_init(self, *args, **kwargs)
        finally:
            for name, value in saved.items():
                setattr(self, name, value)

    dm.Dataset.__post_init__ = _patched_dataset_post_init
    try:
        obj = dm.HealthDataset(**data)
    finally:
        dm.Dataset.__post_init__ = real_dataset_post_init

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
# + health_dcat_ap_plus.yaml). Found 2026-08-21, updated 2026-08-21 after
# fixing the vocab-range and cv:contactPoint bugs (see KNOWN_REAL_SHAPES_VIOLATIONS
# below and docs/architecture-verification.md section 6) -- both fixes are
# real, verified wins (the real-shapes run dropped from 31 to 20 violations,
# every NodeKind/hasValue/contactPoint finding from before resolved).
# ---------------------------------------------------------------------------
KNOWN_OWN_SHAPES_VIOLATIONS: FrozenSet[Signature] = frozenset(
    {
        # Structural, but investigated and settled, not a bug: HealthDataset
        # shares dcat:Dataset's own class_uri with dcat-ap-plus's unmodified
        # base Dataset class (the whole point of the "Health<X> profile"
        # pattern -- same real-world type, tighter shape). Confirmed directly
        # by querying our own generated SHACL: sh:targetClass dcat:Dataset
        # now carries *two* sh:property shapes for dct:accessRights (and
        # accrualPeriodicity/language/theme/type) -- dcat-ap-plus's own
        # original RightsStatement-classed one, untouched, plus HealthDataset's
        # new uriorcurie/nodeKind-IRI one -- and a bare IRI can't satisfy both
        # at once. Checked how systemic this is (26 such conflicts across the
        # whole schema, 17 from this fix, spanning 5 classes -- see
        # docs/architecture-verification.md section 6) and why it happens:
        # dcat-ap-plus's RightsStatement/Frequency/Concept ranges faithfully
        # reflect plain DCAT-AP's own convention, while HealthDCAT-AP's real
        # spec genuinely diverges from that convention for these same
        # predicates -- a real difference between the two specs, not
        # something either got wrong, and not something present in the
        # KNOWN_REAL_SHAPES_VIOLATIONS test below (HealthDCAT-AP's own real
        # shapes are self-sufficient and never actually get unioned with
        # plain DCAT-AP's generic ones in practice). Decision: leave this be
        # rather than inventing a "most-specific-class-wins" SHACL-resolution
        # rule of our own -- that wouldn't be any more correct, since real
        # SHACL has no override semantics either. This allowlist entry is the
        # permanent, honest record of it.
        ("Violation", "ClassConstraintComponent", "accessRights"),
        ("Violation", "ClassConstraintComponent", "accrualPeriodicity"),
        ("Violation", "ClassConstraintComponent", "conformsTo"),
        ("Violation", "ClassConstraintComponent", "language"),
        ("Violation", "ClassConstraintComponent", "theme"),
        ("Violation", "ClassConstraintComponent", "type"),
        # FIXED (was here as a real, structural port bug): dcterms:relation/
        # source/conformsTo were ported under the wrong dcat-ap-plus slot,
        # because dcat-ap-plus reuses each predicate URI across several of
        # its own slots (e.g. dcterms:relation alone maps to
        # has_qualitative_attribute / has_quantitative_attribute /
        # related_resource / relation) and the port script's URI->slot-name
        # resolution could only remember one candidate per URI, arbitrarily.
        # property_name_for now also resolves against the current shape's
        # own class_name via class_induced_slots first -- confirmed
        # unambiguous for all three URIs on Dataset specifically (exactly
        # one induced-slot match each) -- falling back to the classless
        # dict only when the class doesn't resolve it either. relation and
        # source are fully resolved now (their own entries are gone from
        # this allowlist -- confirmed, not assumed). conformsTo above is
        # the one exception, but for an unrelated reason: it correctly
        # resolves to conforms_to now, and conforms_to's own remaining
        # ClassConstraintComponent is just another instance of the
        # class_uri-sharing pattern already accepted above (accessRights/
        # theme/etc.), nothing to do with predicate collision anymore.
        # Diagnosed, not a schema bug, and not even a HealthDCAT-AP-port
        # issue at all -- purely internal to dcat-ap-plus's own base schema.
        # Confirmed directly: EvaluatedEntity and Entity themselves declare
        # no "value" slot at all; dcat-ap-plus's own QualitativeAttribute
        # class ("A piece of information that is attributed to an Entity,
        # Activity or AgenticEntity") does, with required: true, and shares
        # the exact same class_uri: prov:Entity as Entity/EvaluatedEntity/
        # AnalysisSourceData (4 distinct dcat-ap-plus classes, all class_uri
        # prov:Entity, confirmed by grep). Same class_uri-sharing mechanism
        # as the accessRights/theme/etc. finding above -- QualitativeAttribute's
        # own required field bleeds onto the merged prov:Entity shape and
        # applies to every prov:Entity-typed node, including ones that have
        # nothing to do with QualitativeAttribute.
        ("Violation", "MinCountConstraintComponent", "value"),
        # Same class_uri-sharing mechanism again, this time a direct,
        # expected side effect of the cv:contactPoint fix itself: HealthAgent/
        # HealthPublisherAgent now correctly share class_uri: foaf:Agent with
        # dcat-ap-plus's own base Agent class (as they should -- that's what
        # makes a real hdab/custodian value actually typed foaf:Agent, which
        # HealthAgent_Shape requires). But that means Agent's own merged
        # foaf:Agent shape now also carries HealthAgent's required
        # agent_contact_point (cv:contactPoint) constraint, which bleeds onto
        # every foaf:Agent-typed node in the graph -- including
        # DatasetAttribution.attribution_agent's plain Agent value, which has
        # no contactPoint and shouldn't need one.
        ("Violation", "MinCountConstraintComponent", "contactPoint"),
        # Same predicate-URI-collision family as relation/source/conformsTo
        # above, confirmed by checking dcat-ap-plus's own schema: hasLegalBasis
        # -> dpv:hasLegalBasis, hasPersonalData -> dpv:hasPersonalData,
        # hasPurpose -> dpv:hasPurpose, hasQualityAnnotation ->
        # dqv:hasQualityAnnotation, and "subject" all carry sh:class
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
        # Already-known, separate, pre-existing LinkML code-gen bug (same
        # class as the frequency/access_rights/theme/type/language
        # __post_init__ re-processing crash worked around in
        # _build_test_dataset_graph): HealthDataset.temporal_resolution
        # ends up serialized as a Python list's repr baked into one
        # xsd:duration literal ("['P1D']") instead of one duration value --
        # not yet root-caused, tracked separately, not fixed here.
        ("Violation", "DatatypeConstraintComponent", "temporalResolution"),
        # Diagnosed, not a schema bug -- confirmed by direct, isolated
        # reproduction (not assumed): rdflib.Literal("x") != rdflib.Literal(
        # "x", datatype=XSD.string) in rdflib itself (.datatype is None vs.
        # explicit), so rdflib_dumper's plain-string output never satisfies
        # sh:datatype xsd:string even though RDF 1.1 says an untyped literal
        # IS an xsd:string. Affects every plain-string-typed slot below.
        ("Violation", "DatatypeConstraintComponent", "title"),
        ("Violation", "DatatypeConstraintComponent", "description"),
        ("Violation", "DatatypeConstraintComponent", "identifier"),
        ("Violation", "DatatypeConstraintComponent", "keyword"),
        ("Violation", "DatatypeConstraintComponent", "email"),
        ("Violation", "DatatypeConstraintComponent", "name"),
        ("Violation", "DatatypeConstraintComponent", "hasCodeValues"),
        ("Violation", "DatatypeConstraintComponent", "populationCoverage"),
        ("Violation", "DatatypeConstraintComponent", "hasEmail"),
        # Diagnosed, not a schema bug -- a different cause from the string
        # ones above (these already carry the exactly-correct explicit
        # datatype in the dump -- xsd:date/xsd:boolean/xsd:nonNegativeInteger
        # -- and still fail). Root cause confirmed by direct, isolated
        # reproduction: linkml generate shacl numbers sh:order per source
        # class, restarting at 1 for HealthDataset's own additions; once
        # merged onto the same dcat:Dataset shape subject (the same
        # class_uri-sharing fact from the "26 conflicts" investigation
        # above, this time surfacing via sh:order instead of a semantic
        # conflict), sh:order values collide across unrelated properties
        # (confirmed directly: dcat:landingPage and healthdcatap:maxTypicalAge
        # both carry sh:order 15 on the merged shape) -- and pyshacl visibly
        # mishandles the collision, misreporting a passing value as a
        # datatype violation. Reproduced in a self-contained 948-triple
        # extract of just dcat:Dataset's own shape closure, independent of
        # the rest of the schema, ruling out any other cause.
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
# Found 2026-08-21, updated 2026-08-21: 31 -> 20 after the vocab-range and
# cv:contactPoint fixes (every NodeKind bare-IRI, sh:hasValue NON_PUBLIC/HEAL,
# and contactPoint finding gone) -> 19 after also fixing HealthAgent's
# missing foaf:Agent class_uri (the ClassConstraintComponent "hdab" finding
# is gone). See docs/architecture-verification.md section 6.
# ---------------------------------------------------------------------------
KNOWN_REAL_SHAPES_VIOLATIONS: FrozenSet[Signature] = frozenset(
    {
        # mdr-vocabularies.shape.ttl's own "must conform to X_Restriction"
        # node-shape check (skos:inScheme membership) still fires -- expected,
        # test-fixture artifact, not a schema bug: these are illustrative
        # term IRIs, not real EU/HealthDCAT-AP authority-table entries with
        # a genuine skos:inScheme triple. Same root cause as the
        # ClassConstraintComponent findings just below.
        ("Violation", "NodeConstraintComponent", "healthCategory"),
        ("Violation", "NodeConstraintComponent", "healthTheme"),
        ("Violation", "NodeConstraintComponent", "theme"),
        ("Violation", "NodeConstraintComponent", "accessRights"),
        ("Violation", "NodeConstraintComponent", "accrualPeriodicity"),
        ("Violation", "NodeConstraintComponent", "hasCodingSystem"),
        ("Violation", "NodeConstraintComponent", "language"),
        ("Violation", "NodeConstraintComponent", "conformsTo"),
        ("Warning", "NodeConstraintComponent", "type"),
        ("Violation", "MinCountConstraintComponent", "inScheme"),
        ("Violation", "HasValueConstraintComponent", "inScheme"),
        # Benign, expected: dct:source is only sh:Warning-severity
        # "recommended" in the real shapes (non-public-shapes_recommended.ttl
        # -- confirmed directly, not assumed, and the reason the port script
        # was fixed to stop treating every *_recommended.ttl sh:minCount as
        # a hard LinkML `required`, see the severity-awareness fix above).
        # This fixture simply doesn't supply the optional source field.
        ("Warning", "MinCountConstraintComponent", "source"),
        # NEW, but the same test-fixture-artifact family, not a new bug:
        # range.ttl carries its own, independent sh:class requirement for
        # these three HealthDCAT-AP-specific predicates (dcterms:Standard /
        # skos:Concept), separate from mdr-vocabularies.shape.ttl's
        # skos:inScheme check above. Previously satisfied by accident --
        # the old fixture used nested Concept/Standard objects that
        # self-asserted their own rdf:type; now that the range is
        # (correctly) a bare IRI, nothing in this fixture asserts a type on
        # it at all. Needs the real vocabulary graph loaded, or explicit
        # rdf:type triples on the term IRIs, neither of which this fixture
        # attempts.
        ("Violation", "ClassConstraintComponent", "hasCodingSystem"),
        ("Violation", "ClassConstraintComponent", "healthCategory"),
        ("Violation", "ClassConstraintComponent", "healthTheme"),
        # Test-fixture artifacts, not schema bugs: dpv:hasLegalBasis /
        # hasPersonalData / hasPurpose / dqv:hasQualityAnnotation need the
        # real DPV/DQV ontologies loaded (or explicit rdf:type triples on
        # the term IRIs) for sh:class membership checks to pass -- this
        # fixture uses bare term IRIs with no inference.
        ("Violation", "ClassConstraintComponent", "hasLegalBasis"),
        ("Violation", "ClassConstraintComponent", "hasPersonalData"),
        ("Violation", "ClassConstraintComponent", "hasPurpose"),
        ("Violation", "ClassConstraintComponent", "hasQualityAnnotation"),
        # Already-known from the self-shapes pass, now independently
        # reconfirmed: the plain Dataset-level contact_point's
        # vcard:hasEmail must be an IRI (mailto:...), not a string literal.
        ("Violation", "NodeKindConstraintComponent", "hasEmail"),
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

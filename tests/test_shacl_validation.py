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

import sys
from pathlib import Path
from typing import FrozenSet, Tuple

import pyshacl
import pytest
import yaml
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from rdflib import SKOS, Graph, Namespace, URIRef

import health_dcat_ap_plus.datamodel.health_dcat_ap_plus as dm

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import gen_merged_shacl  # noqa: E402
SCHEMA_PATH = (
    REPO_ROOT / "src" / "health_dcat_ap_plus" / "schema" / "health_dcat_ap_plus.yaml"
)
FIXTURE_PATH = (
    Path(__file__).parent / "data" / "problem" / "valid" / "HealthDataset-shacl-full.yaml"
)
HEALTHDCATAP_SHACL_DIR = (
    REPO_ROOT / "repos" / "healthdcat-ap" / "public" / "releases" / "release-7" / "html" / "shacl"
)
# Sciensano's real hosted validator (https://healthdcat-validator.sciensano.be)
# is an ITB instance whose exact config is checked directly into the official
# repo at this path -- config.properties there sets `validator.shaclFile.*`
# to precisely the 5 files _REAL_SHAPE_FILES below already loads (confirmed
# directly, not assumed: same filenames, just different subdirectories under
# this same release-7 tree), plus `validator.preloadOwlImports = true` and a
# ~37-entry owlImportMapping that merges real, populated vocabulary RDF/OWL
# graphs into every validation's data graph -- including HealthDCAT-AP's own
# health-theme/healthcategories/coding-system tables, which turned out to
# have real content in this checked-in cache even where the live
# "acceptance"-environment server (see tests/data/real_vocabulary_terms.ttl's
# old comment, now corrected) currently returns empty RDF.
OFFICIAL_VOCABULARY_CATALOGUE_DIR = (
    HEALTHDCATAP_SHACL_DIR / "HealthDCAT-AP_validator" / "config" / "rdf-validator" / "ehds" / "catalogue"
)

SH = Namespace("http://www.w3.org/ns/shacl#")

Signature = Tuple[str, str, str]


def _build_test_dataset_graph() -> Graph:
    """Build the fixture's RDF graph via the real dataclass -> rdflib_dumper path.

    No construction workaround needed here anymore: HealthDataset (and every
    other Health<X> class that narrows a slot's range/multivalued-ness via
    slot_usage) used to crash on construction, because the parent class's
    own generated __post_init__ unconditionally re-processed the
    already-correctly-narrowed value under its own, stale assumption.
    scripts/patch_post_init_shielding.py now fixes this at the generated
    source level, as a permanent step of `just gen-python`/`just
    gen-project` -- see that script's own docstring for the full mechanism.
    Confirmed directly: constructing HealthDataset(**data) here needs
    nothing beyond plain dataclass construction.
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
    # exactly as-is. This one isn't a __post_init__-shielding case at all --
    # was_generated_by's own range is unchanged, this is about substituting
    # a subclass instance for a field the schema deliberately doesn't
    # narrow (see AssociatedDataGeneratingActivity's own docstring).
    data["was_generated_by"] = [dm.AssociatedDataGeneratingActivity(**entry) for entry in data["was_generated_by"]]

    obj = dm.HealthDataset(**data)

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


# Health-specific + generic MDR authority tables actually referenced by
# fields the HealthDataset fixture populates (access-right, frequency,
# language, data-theme, dataset-type, plus every HealthDCAT-AP-specific
# table). Deliberately skips the huge geographic/corporate-body tables
# (continents/countries/corporatebodies/places, tens of thousands of
# entries each) and the pure-ontology files (schema.ttl, dcat2.ttl,
# prov-o.ttl, etc.) that config.properties also preloads: those ontology
# files only declare owl:Class terms, which can't help a ClassConstraintComponent/
# skos:inScheme check without RDFS/OWL entailment -- and this project runs
# pyshacl with inference="none" deliberately (checked directly, not
# guessed: loading them changes nothing for this fixture). Revisit this
# subset if a future fixture actually populates dct:spatial or a
# corporate-body-coded field.
OFFICIAL_VOCABULARY_CATALOGUE_FILES = [
    "health-theme.rdf",
    "healthcategories.rdf",
    "coding-system.rdf",
    "health-activity.rdf",
    "standard.rdf",
    "publisher-type.rdf",
    "access-right.rdf",
    "frequencies.rdf",
    "languages.rdf",
    "data-theme.rdf",
    "dataset-types.rdf",
    "planned-availability.rdf",
    "distribution-status.rdf",
    "filetypes.rdf",
]


def _official_vocabulary_catalogue_graph() -> Graph:
    """Load Sciensano's own real, cached vocabulary catalogue (see
    OFFICIAL_VOCABULARY_CATALOGUE_DIR's own comment for what this is and
    why it exists). Each file's real serialization format is sniffed
    directly rather than assumed from its extension -- confirmed some
    catalogue files use RDF/XML despite non-`.rdf` naming conventions
    elsewhere in this tree, and vice versa.
    """
    g = Graph()
    for fname in OFFICIAL_VOCABULARY_CATALOGUE_FILES:
        text = (OFFICIAL_VOCABULARY_CATALOGUE_DIR / fname).read_text(encoding="utf-8")
        fmt = "xml" if text.lstrip().startswith("<?xml") or "<rdf:RDF" in text[:500] else "turtle"
        g.parse(data=text, format=fmt)
    return g


REAL_VOCABULARY_TERMS_PATH = Path(__file__).parent / "data" / "real_vocabulary_terms.ttl"


def _real_vocabulary_terms_graph() -> Graph:
    """Load the curated snapshot of real DPV term triples.

    See tests/data/real_vocabulary_terms.ttl's own header for what this is
    and why it's a static checked-in snapshot rather than a live fetch. DPV
    isn't one of HealthDCAT-AP's own MDR-managed authority tables (see
    OFFICIAL_VOCABULARY_CATALOGUE_DIR's own comment), so
    _official_vocabulary_catalogue_graph() above can't cover it -- this
    small hand-curated snippet is what's left after that catalogue took
    over everything it does cover. Only merged into the *real*-shapes
    validation below, not _build_test_dataset_graph()'s own output -- these
    are validation aids about external resources, not part of our own
    dataset's data, and shouldn't leak into the published example.
    """
    g = Graph()
    g.parse(str(REAL_VOCABULARY_TERMS_PATH), format="turtle")
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
# every NodeKind/hasValue/contactPoint finding from before resolved). Count
# held flat at 30 after the 2026-08-25 sh:nodeKind sh:IRI range fix -- one
# fixed (hasEmail's literal-vs-IRI quirk), one newly surfaced
# (applicableLegislation, now correctly typed enough to hit the same
# already-accepted class_uri-sharing pattern the others already do) -- see
# each entry's own comment, not a regression.
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
        # Same class_uri-sharing family as the six above, newly surfaced
        # 2026-08-25 after fixing the port script's sh:nodeKind sh:IRI gap
        # (see the parse_shapes fix and its own comment): applicable_legislation
        # was previously unranged (silently fell to the schema default,
        # string) so this ClassConstraintComponent conflict against
        # dcat-ap-plus's own class-object range for the same predicate was
        # never actually checked. Now that it's correctly uriorcurie, it's
        # checked and hits the exact same already-understood, already-accepted
        # structural pattern as the others -- not a new category of problem.
        ("Violation", "ClassConstraintComponent", "applicableLegislation"),
        # NEW 2026-08-28, expected: dct:source's recovered range
        # (HealthDataset, a real, correct constraint -- see
        # _FORCE_NON_INLINED_ON_RECOVERED_RANGE's own comment in
        # port_healthdcat_ap_shacl_to_linkml.py) requires sh:class
        # HealthDataset on the value. The fixture now populates source with
        # a bare URI (matching HealthDCAT-AP's own real convention: the
        # source dataset is described separately, not embedded here -- see
        # examples/reference/example-healthdcat-dataset.ttl), which
        # correctly has no local rdf:type triple of its own. The REAL
        # HealthDCAT-AP shapes don't have this problem at all (confirmed:
        # dct:source carries no sh:class constraint there whatsoever, only
        # a Warning-severity minCount) -- this is purely a self-testing
        # artifact of our own port recovering a technically-correct but
        # impractical-to-satisfy-inline constraint, same family as the
        # class_uri-sharing entries above.
        ("Violation", "ClassConstraintComponent", "source"),
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
        # nothing to do with QualitativeAttribute. A real LinkML
        # ShaclGenerator bug, not dcat-ap-plus's to fix -- filed as
        # https://github.com/linkml/linkml/issues/3932, standalone
        # reproduction at
        # examples/issues_for_linkml/class-uri-cardinality-bleed.ipynb.
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
        # FIXED 2026-08-28: hasQualityAnnotation used to be here too --
        # gone now that has_quality_annotation gained inlined_as_list: true
        # (port script), constructing a real QualityCertificate object
        # instead of a bare reference. See the fixture YAML's own comment.
        ("Violation", "ClassConstraintComponent", "subject"),
        # FIXED 2026-08-31 (this entry plus 16 more that used to follow it
        # here, and the merged-shapes `title` entry too -- 17 in total).
        # Every one of them carried its own separate diagnosis --
        # dcat:temporalResolution's and the date/boolean/integer group's own
        # "sh:order collision" theory, the string-typed group's own
        # "rdflib.Literal('x') != rdflib.Literal('x', datatype=XSD.string)"
        # theory -- and every one of those diagnoses turned out to be
        # wrong, the same way the earlier "single-slot stub classes always
        # collapse" belief was (see the hasQualityAnnotation finding
        # above). Root-caused for real this time, prompted by actually
        # inspecting the failing sh:datatype term directly instead of
        # reasoning about rdflib/pyshacl semantics in the abstract: every
        # one of these property shapes' own sh:datatype value was the
        # *unexpanded CURIE string* "xsd:string"/"xsd:date"/"xsd:boolean"/
        # etc. used directly as a URIRef (ten-ish characters, not the real
        # ~39-character http://www.w3.org/2001/XMLSchema# IRI) -- no
        # literal, however typed, could ever satisfy that. Cause: this
        # schema's own prefixes: block redeclares dcterms:/dcat:/prov:/etc.
        # to work around LinkML's own gen-shacl/gen-owl prefix-propagation
        # gap (imported schemas' prefixes don't reach the generated
        # Turtle -- already documented above for dcatap:), but never
        # redeclared xsd: specifically -- easy to miss since a missing
        # xsd: doesn't announce itself as a `@prefix ns1: <weird>` line the
        # way the others did; it silently produces a well-formed-looking
        # but wrong sh:datatype instead. Fixed by adding xsd: to this
        # schema's own prefixes: block (and to the port script's PREFIXES
        # dict, for healthdcat_ap_non_public.yaml's own regeneration) --
        # see docs/architecture-verification.md for the full
        # misdiagnosis-then-correction narrative.
    }
)


# ---------------------------------------------------------------------------
# Violations against HealthDCAT-AP's own real, official upstream SHACL.
# Found 2026-08-21, updated 2026-08-21: 31 -> 20 after the vocab-range and
# cv:contactPoint fixes (every NodeKind bare-IRI, sh:hasValue NON_PUBLIC/HEAL,
# and contactPoint finding gone) -> 19 after also fixing HealthAgent's
# missing foaf:Agent class_uri (the ClassConstraintComponent "hdab" finding
# is gone) -> 18 after fixing the sh:nodeKind sh:IRI range gap (hasEmail) ->
# 12 after merging in a small curated snapshot of external term triples.
#
# Updated again 2026-08-26, down to 3: prompted by manually cross-checking
# against Sciensano's own official hosted validator
# (https://healthdcat-validator.sciensano.be), which reported zero
# violations for this exact fixture (examples/HealthDataset-full-example.ttl,
# pasted in as-is) -- a real discrepancy worth resolving, not dismissing.
# Root-caused directly, not guessed: their ITB config is checked into the
# official repo itself (see OFFICIAL_VOCABULARY_CATALOGUE_DIR's own comment)
# and preloads real, populated vocabulary catalogue graphs -- confirming the
# earlier "resolves to empty RDF" belief was about the wrong thing: the
# *live* acceptance-environment server is empty, but this checked-in cache
# genuinely is not. Merging that same catalogue in here
# (_official_vocabulary_catalogue_graph) reproduced their result almost
# exactly, and also surfaced that 4 of the fixture's own term references
# were themselves invented/wrong, not just unverifiable:
#   - healthcategories/ONCOLOGY doesn't exist -- healthcategories is EHDS
#     Article 51's *data category* list (genetic data, claims data,
#     registry data, ...), not a disease/specialty list. Fixed to PHDR
#     ("data from population-based health data registries").
#   - health-theme/CANCER doesn't exist -- the real code is CANCER_DISEASE.
#   - coding-system/ICD_O_3 (underscored) doesn't exist -- the real code is
#     hyphenated, ICD-O-3.
#   - dataset-type/EXPLOITABLE doesn't exist -- fixed to STATISTICAL
#     ("Statistical data"), the real code that actually fits an aggregate
#     incidence registry.
# All four were fixed directly in the fixture (see its own comments), which
# is what actually cleared their violations -- not the catalogue merge
# alone. See docs/architecture-verification.md section 6.
#
# FIXED 2026-08-26: conformsTo's own NodeConstraintComponent + nested
# MinCount/HasValueConstraintComponent inScheme trio is gone -- the fixture
# now points dct:conformsTo at a REAL member of HealthDCAT-AP's own
# standard vocabulary (.../authority/standard/FHIR, confirmed directly
# against standard.rdf: a real skos:Concept + dct:Standard entry with its
# own skos:inScheme triple) instead of a local, instance-specific schema
# URI. Nothing added to the published example file itself for this --
# FHIR's own describing triples are supplied only at validation time, by
# _referenced_terms_closure_graph, same as every other external term.
#
# FIXED 2026-08-28: dct:source's own Warning is gone -- the fixture now
# populates it (a bare URI, matching HealthDCAT-AP's own real convention;
# see the fixture YAML's own comment). Needed two real fixes to get there,
# not a fixture-only change: port_healthdcat_ap_shacl_to_linkml.py's
# _FORCE_NON_INLINED_ON_RECOVERED_RANGE (stop forcing eager nested
# construction for a value that's meant to be an independent, separately-
# published resource) and patch_post_init_shielding.py's compute_shield_map
# gaining an inlined/inlined_as_list check it was missing entirely before
# (range/multivalued only) -- see both scripts' own docstrings.
#
# FIXED 2026-08-28: hasQualityAnnotation is gone too, the same day --
# turned out genuinely fixable, not a permanent limitation. The earlier
# "single-slot stub classes always collapse to a bare URI" diagnosis was
# imprecise: confirmed directly, in isolation, that an inlined class with
# only an identifier slot still gets its own rdf:type triple correctly
# asserted on dump. The real, narrower cause was specifically that
# has_quality_annotation's own generated slot_def never set
# inlined_as_list at all (unlike qualified_attribution, which always had
# an explicit override) -- so it defaulted to a bare-identifier reference.
# Now fixed via the exact same kind of hand-authored slot_usage override
# in port_healthdcat_ap_shacl_to_linkml.py, deliberately NOT applied to
# has_legal_basis/has_personal_data/has_purpose (the other three
# externally-referenced-but-unshaped stub ranges), which correctly stay
# bare references to real, externally-governed DPV vocabulary terms --
# inlining those would wrongly imply we're meant to locally describe
# someone else's vocabulary concept. A quality certificate is different in
# kind: the dataset publisher's own assertion about their own dataset,
# exactly the kind of thing that should be locally, richly describable.
# This also resolves the earlier "not reproduced on Sciensano's own hosted
# validator" open question -- moot now that our own construction is fixed,
# not something that needed a separate explanation after all.
#
# KNOWN_REAL_SHAPES_VIOLATIONS is empty as of this fix: the HealthDataset
# portion of this fixture now fully conforms to HealthDCAT-AP's real,
# official upstream SHACL shapes.
# ---------------------------------------------------------------------------
KNOWN_REAL_SHAPES_VIOLATIONS: FrozenSet[Signature] = frozenset(set())


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
    # Merge in the same vocabulary preloading Sciensano's own official
    # validator does (_official_vocabulary_catalogue_graph) plus the DPV
    # terms it doesn't cover (_real_vocabulary_terms_graph), so pyshacl's
    # skos:inScheme/sh:class checks have real membership triples to check
    # against, instead of failing simply because our own instance data only
    # carries a bare reference to each term, not that term's own describing
    # triples.
    data_graph = _build_test_dataset_graph() + _official_vocabulary_catalogue_graph() + _real_vocabulary_terms_graph()
    shapes_graph = _real_healthdcat_ap_shapes_graph()
    _, results_graph, _ = pyshacl.validate(
        data_graph,
        shacl_graph=shapes_graph,
        data_graph_format="turtle",
        inference="none",
        advanced=True,
    )
    _assert_known_violations(_violation_signatures(results_graph), KNOWN_REAL_SHAPES_VIOLATIONS)


def _merged_shapes_graph() -> Graph:
    """The ONE production shapes graph: HealthDCAT-AP's real official
    shapes + our own generated shapes for everything they don't cover, with
    the Dataset/Distribution/Agent/vocabulary-stub overlap filtered out --
    see scripts/gen_merged_shacl.py's own docstring for the full mechanism.

    Rebuilt fresh in-memory whenever the sibling repos/healthdcat-ap clone
    is present (so it can never silently go stale here or in CI, which
    always has that clone -- same freshness guarantee `just test`'s own
    gen-python prerequisite gives the Python dataclasses, just scoped to
    this one test instead of wired into the whole `just test` pipeline,
    since -- unlike gen-python -- this generation step has an external
    dependency not every contributor will have set up locally). Falls back
    to the committed docs/schema/health_dcat_ap_plus.merged-shacl.ttl
    (regenerate via `just gen-shacl`) when that clone is absent; skips only
    if neither is available.
    """
    if HEALTHDCATAP_SHACL_DIR.exists():
        return gen_merged_shacl.build_merged_shapes_graph()
    if gen_merged_shacl.OUTPUT_PATH.exists():
        g = Graph()
        g.parse(str(gen_merged_shacl.OUTPUT_PATH), format="turtle")
        return g
    pytest.skip(
        f"neither repos/healthdcat-ap nor the committed "
        f"{gen_merged_shacl.OUTPUT_PATH} is available -- see README.md for "
        "how to fetch the former, or run `just gen-shacl` once it's fetched"
    )


def _referenced_terms_closure_graph(data_graph: Graph, catalogue_graph: Graph) -> Graph:
    """Extract just the describing triples for external vocabulary terms
    `data_graph` actually references (any URI object that's also a subject
    in `catalogue_graph`), plus one hop out via skos:inScheme for the
    ConceptScheme membership check -- same real membership triples merging
    the whole catalogue would supply, at a fraction of the size.

    Confirmed directly, not assumed: merging the full ~208k-triple official
    catalogue as data alongside the *merged* shapes graph (real + our own
    filtered shapes, more shapes than either individual test uses) made
    pyshacl's advanced-mode validation pathologically slow -- several
    minutes, not obviously converging. This targeted extraction reaches the
    identical validation result in well under a second.
    """
    referenced = {
        o for _, _, o in data_graph if isinstance(o, URIRef) and next(catalogue_graph.triples((o, None, None)), None)
    }
    g = Graph()
    seen: set = set()
    stack = list(referenced)
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        for p, o in catalogue_graph.predicate_objects(u):
            g.add((u, p, o))
            if p == SKOS.inScheme and o not in seen:
                stack.append(o)
    return g


# ---------------------------------------------------------------------------
# Violations against the ONE merged production shapes graph (real
# HealthDCAT-AP shapes + our own filtered shapes -- see
# _merged_shapes_graph's own docstring). Found 2026-08-26, built specifically
# to confirm the filtering mechanism itself: every signature below was
# individually traced to its focus node and source shape before being
# allowlisted, not just pattern-matched against the two existing allowlists
# above.
#
# Updated 2026-08-26: conformsTo's own trio (NodeConstraintComponent +
# nested MinCount/HasValueConstraintComponent inScheme) is gone -- see
# KNOWN_REAL_SHAPES_VIOLATIONS' own comment on the same fix (FHIR, a real
# standard-vocabulary member, replaced the fixture's local schema URI).
#
# Updated 2026-08-28: dct:source's own Warning is gone too -- see
# KNOWN_REAL_SHAPES_VIOLATIONS' own comment on that fix. Doesn't newly
# surface a ClassConstraintComponent here the way KNOWN_OWN_SHAPES_VIOLATIONS
# does: our own Dataset-targeting NodeShape (the one carrying source's
# sh:class HealthDataset constraint) is exactly one of the ones filtered
# out of the merged graph, since the real shapes already own that class --
# and the real shapes never constrained dct:source's class at all.
#
# FIXED 2026-08-28: hasQualityAnnotation is gone too -- see
# KNOWN_REAL_SHAPES_VIOLATIONS' own comment on the same fix
# (has_quality_annotation gained inlined_as_list: true, constructing a
# real, correctly-typed QualityCertificate object).
# ---------------------------------------------------------------------------
KNOWN_MERGED_SHAPES_VIOLATIONS: FrozenSet[Signature] = frozenset(
    {
        # Already known from KNOWN_OWN_SHAPES_VIOLATIONS, unrelated to
        # Dataset/Distribution/Agent (so unaffected by filtering those
        # out): QualitativeAttribute's own required prov:value bleeds onto
        # every prov:Entity-typed node via the shared class_uri (see that
        # allowlist's own comment) -- fires here on the population Entity
        # node, which has no prov:value of its own. A real LinkML
        # ShaclGenerator bug (distinct classes sharing one class_uri get
        # merged into a single NodeShape, folding cardinality constraints
        # together, not just cosmetic ones) -- filed as
        # https://github.com/linkml/linkml/issues/3932, standalone
        # reproduction at examples/issues_for_linkml/class-uri-cardinality-bleed.ipynb.
        ("Violation", "MinCountConstraintComponent", "value"),
        # FIXED 2026-08-31: title used to be here too -- see
        # KNOWN_OWN_SHAPES_VIOLATIONS' own comment on the same fix (this
        # schema's own prefixes: block was missing an xsd: redeclaration,
        # a real, fixable bug, not the rdflib/pyshacl untyped-literal
        # interop quirk it was originally, wrongly, attributed to).
        # NEW finding, only visible once Dataset's own conflicting dct:type
        # shape is filtered out: dcat-ap-plus's own ClassifierMixin mixes
        # an `rdf_type` slot into every Activity/Entity/AgenticEntity/Plan/
        # Surrounding class, mapped directly to the bare rdf:type predicate
        # (slot_uri: rdf:type) -- confirmed directly by tracing this
        # violation's own focus/value nodes: the VALUE being checked
        # against `sh:class schema:DefinedTerm` is literally the node's own
        # class-typing triple (e.g. <activity> rdf:type prov:Activity),
        # not a separately-set classification value. SHACL can't tell
        # those two triples apart -- they're both just <node> rdf:type
        # <value>. A real, pre-existing dcat-ap-plus schema quirk (the
        # rdf_type slot reusing the class-typing predicate), not something
        # this filtering work introduced; simply never visible before
        # because it shared this exact (severity, component, path) triple
        # with the separate, already-diagnosed Dataset dct:type conflict
        # KNOWN_OWN_SHAPES_VIOLATIONS' own "type" entry actually names.
        # Posted to dcat-ap-plus (https://github.com/nfdi-de/dcat-ap-plus/issues/110),
        # confirmed by a maintainer, traced to a real LinkML ShaclGenerator
        # bug and filed as https://github.com/linkml/linkml/issues/3931,
        # standalone reproduction at
        # examples/issues_for_linkml/rdf-type-slot-uri-collision.ipynb.
        ("Violation", "ClassConstraintComponent", "type"),
    }
)


def test_dataset_conforms_to_merged_shacl():
    """The end-to-end check: does a real HealthDataset instance conform to
    the ONE shapes graph a real downstream user would actually validate
    against -- HealthDCAT-AP's real official shapes for the catalogue side,
    plus our own shapes for everything else, no conflicts between them?
    """
    catalogue = _official_vocabulary_catalogue_graph()
    base_data = _build_test_dataset_graph()
    data_graph = base_data + _referenced_terms_closure_graph(base_data, catalogue) + _real_vocabulary_terms_graph()
    shapes_graph = _merged_shapes_graph()
    _, results_graph, _ = pyshacl.validate(
        data_graph,
        shacl_graph=shapes_graph,
        data_graph_format="turtle",
        inference="none",
        advanced=True,
    )
    _assert_known_violations(_violation_signatures(results_graph), KNOWN_MERGED_SHAPES_VIOLATIONS)

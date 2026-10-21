"""What the SHACL tests of Health-DCAT-AP-plus and ResHealth-DCAT-AP have in
common: the data environment the official validator gives a document, the
result signatures, the allowlist comparison. Kept here, next to
gen_merged_shacl.py, so the two repos cannot drift apart (they did when each had
its own copy); ResHealth-DCAT-AP loads this file by path from its sibling
checkout, as it does gen_merged_shacl.py.

No dependency on either schema's datamodel, and no import of gen_merged_shacl
(ResHealth-DCAT-AP has a module of that name of its own): every location is
passed in.
"""
from __future__ import annotations

from pathlib import Path
from typing import FrozenSet, Tuple

import pyshacl
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, SKOS

Signature = Tuple[str, str, str]

DPV = Namespace("https://w3id.org/dpv#")
ELI = Namespace("http://data.europa.eu/eli/ontology#")

# Health-specific + generic MDR authority tables actually referenced by the
# data (access-right, frequency, language, data-theme, dataset-type, country,
# continent, plus every HealthDCAT-AP-specific table). Deliberately skips the
# corporate-body and place tables (tens of thousands of entries each; nothing
# here uses a corporate body or a place) and the pure-ontology files
# (schema.ttl, dcat2.ttl, prov-o.ttl, ...) that config.properties also
# preloads: those only declare owl:Class terms, which can't help a
# ClassConstraintComponent/skos:inScheme check without RDFS/OWL entailment --
# and these tests run pyshacl with inference="none" deliberately (checked
# directly, not guessed: loading them changes nothing here). Revisit this list
# if a fixture populates dct:spatial with a place or a corporate-body-coded field.
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
    "continents.rdf",
    "countries.rdf",
]

# External terms typed inline, the way HealthDCAT-AP's own worked example does
# (examples/reference/example-healthdcat-dataset.ttl in Health-DCAT-AP-plus): a
# bare `<term> a <Class>` for each term whose shape checks a simple sh:class
# (DCAT-AP's range.ttl and HealthDCAT-AP's own). The official validator's
# catalogue declares most terms as skos:Concept only, so a self-contained
# document has to say it itself; without these, accessRights, language,
# accrualPeriodicity, applicableLegislation and conformsTo values fail those
# class checks. Terms checked by skos:inScheme instead (healthCategory,
# healthTheme, publisher-type, dataset-type, ...) get nothing, as in the
# official example. Which terms need one was found by running the official
# shapes against the fixture, not by copying the example's choices.
OFFICIAL_CONVENTION_TERM_TYPES: list = [
    ("http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC", DCTERMS.RightsStatement),
    ("http://publications.europa.eu/resource/authority/language/ENG", DCTERMS.LinguisticSystem),
    ("http://publications.europa.eu/resource/authority/frequency/ANNUAL", DCTERMS.Frequency),
    ("http://publications.europa.eu/resource/authority/frequency/DAILY", DCTERMS.Frequency),
    ("http://data.europa.eu/eli/reg/2025/327/oj", ELI.LegalResource),
    ("https://hdeu-dcat.data.health.europa.eu/resource/authority/standard/FHIR", DCTERMS.Standard),
    ("https://hdeu-dcat.data.health.europa.eu/resource/authority/coding-system/ICD-O", DCTERMS.Standard),
    # DPV terms are typed inline in the official example too (its legal basis is
    # `a dpv:LegalBasis`, its personal data `dpvpd:Age a dpv:PersonalData`). The
    # last IRI is not DPV's own -- see the fixture YAML's comment on
    # has_personal_data.
    ("https://w3id.org/dpv#LegalObligation", DPV.LegalBasis),
    ("https://w3id.org/dpv#ScientificResearch", DPV.Purpose),
    ("https://w3id.org/dpv/dpv-pd#MedicalHealth", DPV.PersonalData),
]


def add_official_convention_term_types(graph: Graph) -> Graph:
    for term, cls in OFFICIAL_CONVENTION_TERM_TYPES:
        graph.add((URIRef(term), RDF.type, cls))
    return graph


def load_vocabulary_catalogue(catalogue_dir: Path) -> Graph:
    """Sciensano's own cached vocabulary catalogue (the `catalogue/` folder of the
    official validator's config). Each file's real serialization format is
    sniffed rather than assumed from its extension. Takes ~10 s to parse; callers
    that need it more than once should keep the result (tests only read it)."""
    g = Graph()
    for fname in OFFICIAL_VOCABULARY_CATALOGUE_FILES:
        text = (catalogue_dir / fname).read_text(encoding="utf-8")
        fmt = "xml" if text.lstrip().startswith("<?xml") or "<rdf:RDF" in text[:500] else "turtle"
        g.parse(data=text, format=fmt)
    return g


def referenced_terms_closure_graph(data_graph: Graph, catalogue_graph: Graph) -> Graph:
    """Extract just the describing triples for external vocabulary terms
    `data_graph` actually references (any URI object that's also a subject
    in `catalogue_graph`), plus one hop out via skos:inScheme for the
    ConceptScheme membership check -- same real membership triples merging
    the whole catalogue would supply, at a fraction of the size.

    Merging the full ~208k-triple catalogue made pyshacl's advanced-mode
    validation pathologically slow once combined with a merged shapes graph's
    shape count (several minutes, not obviously converging); this targeted
    extraction reaches the identical validation result in well under a second.
    (The validator's full data environment, 476k triples, does validate in about
    ten seconds on release 8 -- the earlier slowness was the unfiltered
    catalogue alongside the old, closed shapes -- but the extraction stays: it
    keeps the tests' environment small and legible.)
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


def with_official_environment(document: Graph, catalogue_graph: Graph, dpv_snapshot_path: Path) -> Graph:
    """`document` plus what the official validator adds to it: the vocabulary
    terms it references and the DPV terms the catalogue lacks (a curated
    snapshot, see Health-DCAT-AP-plus's tests/data/real_vocabulary_terms.ttl)."""
    snapshot = Graph().parse(str(dpv_snapshot_path), format="turtle")
    return document + referenced_terms_closure_graph(document, catalogue_graph) + snapshot


def violation_signatures(results_graph: Graph) -> FrozenSet[Signature]:
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


def validate(data_graph: Graph, shapes_graph: Graph) -> FrozenSet[Signature]:
    _, results_graph, _ = pyshacl.validate(
        data_graph,
        shacl_graph=shapes_graph,
        data_graph_format="turtle",
        inference="none",
        advanced=True,
    )
    return violation_signatures(results_graph)


def assert_known_violations(actual: FrozenSet[Signature], known: FrozenSet[Signature]) -> None:
    new = actual - known
    stale = known - actual
    assert not new, (
        "New, previously unseen SHACL result(s) -- a real regression, or "
        f"the fixture/schema changed on purpose (update the allowlist): {sorted(new)}"
    )
    assert not stale, (
        "Previously-known result(s) no longer occur -- if a real bug got "
        f"fixed, prune these from the allowlist: {sorted(stale)}"
    )

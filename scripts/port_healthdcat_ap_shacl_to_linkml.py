#!/usr/bin/env python
"""
Port HealthDCAT-AP's SHACL shapes to a LinkML schema fragment, the same
method NFDI4Chem used to port plain DCAT-AP's SHACL to LinkML when building
chem-dcat-ap: walk each sh:NodeShape, turn one with a sh:targetClass into a
LinkML class (preserving the target IRI verbatim as class_uri), turn its
sh:property shapes into slots (preserving sh:path verbatim as slot_uri).
HealthDCAT-AP has no JSON-LD serialization of its shapes (only Turtle), so
this reads Turtle with rdflib instead of JSON with the json module -- same
RDF graph either way, just a different upstream serialization.

Unlike plain DCAT-AP, HealthDCAT-AP's shapes constrain classes DCAT-AP+
already defines (dcat:Dataset, dcat:Catalog, foaf:Agent, ...) rather than
declaring wholly new ones, and reuse many of its properties too (tightening
cardinality, not redefining them). So a fact found while walking the shapes
lands in one of three buckets:

  1. A class whose resolved name already matches a class dcat-ap-plus (the
     imported base) defines -> this is a HealthDCAT-AP *profile* of that
     class: emit a new LinkML class named "Health<X>", is_a: <X>, with the
     SAME class_uri as <X> (this is the exact pattern chem-dcat-ap itself
     uses for e.g. SubstanceSampleCharacterizationDataset is_a Dataset,
     class_uri: dcat:Dataset -- confirmed by reading its schema, not assumed).
  2. A class with no match in the base schema (a genuinely new HealthDCAT-AP
     concept, e.g. the synthetic :HealthAgent_Shape with no sh:targetClass
     of its own) -> emit it as a new LinkML class under its own resolved name.
  3. A property whose path URI already matches a base slot -> the fact is a
     cardinality/range *tightening* of an inherited slot, expressed as
     slot_usage on the owning (possibly renamed per #1) class, not a new
     slot definition.
  4. A property whose path URI has no base match -> a genuinely new slot,
     defined once at the top level and referenced from its owning class.

Also parsed, separately from the three tier files above: mdr-vocabularies.shape.ttl,
HealthDCAT-AP's controlled-vocabulary-membership constraints (35 NodeShapes,
all named *Restriction/*ShapeCV). These don't add classes or properties of
their own -- confirmed by checking, not assumed: none of the four
externally-referenced classes this port stubs (Purpose, LegalBasis,
PersonalData, QualityCertificate; see the stub-generation code below) or
their predicates appear anywhere in this file either. What it does add is
value-set metadata on properties already ported: "dct:language's value must
be skos:inScheme <the EU language NAL>," etc. Recorded via LinkML's own
values_from slot metaslot (a value-set reference, not an expanded enum --
see its own docstring in the LinkML metamodel) rather than fetching and
inlining the actual external vocabularies, which would be a much larger,
separate undertaking. Not parsed at all: imports.ttl/mdr_imports.ttl (pure
owl:imports manifests, no shapes -- confirmed empty of sh:NodeShape content)
and deprecateduris.ttl (a URI redirect table, not shape-relevant).

Source version (record this on every re-run -- HealthDCAT-AP has no stable
"latest" pointer the way dcat-ap-plus has a w3id permalink, so the shapes
this schema was ported from need to be pinned by commit, not just by name):
see the --record-source-as-of output printed at the end of a run, and the
`source_version` line written into the generated file's header comment.
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF, SH, SKOS, XSD

# sh:extends isn't part of the SHACL vocabulary rdflib's SH namespace knows
# about (it's a non-standard term some SHACL authors use informally for
# shape inheritance) -- build the term directly rather than via SH.extends.
SH_EXTENDS = URIRef(str(SH) + "extends")

from linkml_runtime import SchemaView

# Renames dcat_ap_shacl_2_linkml.py (upstream, inside dcat-ap-plus) applied
# when it built dcat_ap_linkml.yaml, reapplied here so a HealthDCAT-AP shape
# targeting e.g. dcat:Catalog lines up with dcat-ap-plus's "Catalogue", not a
# second, differently-spelled class.
CLASS_RENAME = {
    "http://www.w3.org/ns/dcat#Resource": "CataloguedResource",
    "http://www.w3.org/ns/dcat#Catalog": "Catalogue",
    "http://www.w3.org/ns/dcat#CatalogRecord": "CatalogueRecord",
}

XSD_TYPE_NAME = {
    XSD.string: "string",
    XSD.date: "date",
    XSD.dateTime: "datetime",
    XSD.boolean: "boolean",
    XSD.decimal: "decimal",
    XSD.integer: "integer",
    XSD.nonNegativeInteger: "nonNegativeInteger",
    XSD.duration: "duration",
    XSD.anyURI: "uri",
    XSD.hexBinary: "hexBinary",
}

TIER_FILES = {
    "non-public": ["non-public-shapes.ttl", "non-public-shapes_recommended.ttl", "range.ttl"],
    "public": ["public-shapes.ttl", "public-shapes_recommended.ttl", "range.ttl"],
    "restricted": ["restricted-shapes.ttl", "restricted-shapes_recommended.ttl", "range.ttl"],
}

# Also used to render class_uri/slot_uri as CURIEs rather than raw IRIs, matching
# how the rest of this schema family (dcat-ap-plus, chem-dcat-ap, HealthStudy-DCAT-AP)
# writes them.
PREFIXES = {
    "health_dcat_ap_plus": "https://w3id.org/portail-fresh/Health-DCAT-AP-Plus/",
    "linkml": "https://w3id.org/linkml/",
    "dcatapplus": "https://w3id.org/nfdi-de/dcat-ap-plus/",
    "healthdcatap": "http://healthdataportal.eu/ns/health#",
    "dcterms": "http://purl.org/dc/terms/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "prov": "http://www.w3.org/ns/prov#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "adms": "http://www.w3.org/ns/adms#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "vcard": "http://www.w3.org/2006/vcard/ns#",
    "locn": "http://www.w3.org/ns/locn#",
    "odrl": "http://www.w3.org/ns/odrl/2/",
    "spdx": "http://spdx.org/rdf/terms#",
    "cv": "http://data.europa.eu/m8g/",
    "dqv": "http://www.w3.org/ns/dqv#",
    "dpv": "https://w3id.org/dpv#",
    "csvw": "http://www.w3.org/ns/csvw#",
    "time": "http://www.w3.org/2006/time#",
    "geodcatap": "http://data.europa.eu/930/",
}


def to_curie(uri: str) -> str:
    for prefix, ns in PREFIXES.items():
        if uri.startswith(ns):
            return f"{prefix}:{uri[len(ns):]}"
    return uri


def local_name(uri: str) -> str:
    for sep in ("#", "/"):
        if sep in uri:
            return uri.rsplit(sep, 1)[-1]
    return uri


# range.ttl and mdr-vocabularies.shape.ttl declare `@prefix dcatap:
# <http://data.europa.eu/r5r>` -- missing the trailing slash that
# non-public-shapes.ttl/non-public-shapes_recommended.ttl (and dcat-ap-plus's
# own schema: `dcatap: http://data.europa.eu/r5r/`) both have. Confirmed by
# reading all four files' own @prefix lines, not assumed -- a real
# inconsistency within HealthDCAT-AP's own release, not something this port
# introduces. Per the Turtle spec this makes every dcatap:X term in those two
# files expand to a malformed, concatenated URI (e.g. dcatap:availability ->
# .../r5ravailability instead of .../r5r/availability), silently failing to
# match any real dcat-ap-plus slot. The correct namespace is unambiguous (3
# of 4 sources agree), so this is corrected before parsing rather than left
# to silently produce garbage slot names -- worth reporting upstream, but
# also safe to fix locally since it's not a judgment call.
_KNOWN_UPSTREAM_PREFIX_FIXES = {
    "@prefix dcatap: <http://data.europa.eu/r5r> .": "@prefix dcatap: <http://data.europa.eu/r5r/> .",
}


def parse_turtle_with_known_fixes(g: rdflib.Graph, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for bad, good in _KNOWN_UPSTREAM_PREFIX_FIXES.items():
        text = text.replace(bad, good)
    g.parse(data=text, format="turtle")


def to_snake_case(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0 and not name[i - 1].isupper():
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def load_base_schema(schema_path: str):
    """Return (SchemaView, {expanded slot URI: slot name}, {expanded class URI: class name})."""
    sv = SchemaView(schema_path)
    uri_to_slot = {}
    for slot_name in sv.all_slots(imports=True):
        uri = sv.get_uri(slot_name, expand=True)
        if uri:
            uri_to_slot[uri] = slot_name
    uri_to_class = {}
    for class_name in sv.all_classes(imports=True):
        uri = sv.get_uri(class_name, expand=True)
        if uri:
            uri_to_class[uri] = class_name
    return sv, uri_to_slot, uri_to_class


def class_name_for(uri: URIRef, uri_to_class: dict[str, str]) -> str:
    uri_str = str(uri)
    if uri_str in CLASS_RENAME:
        return CLASS_RENAME[uri_str]
    if uri_str in uri_to_class:
        return uri_to_class[uri_str]
    return local_name(uri_str)


def property_name_for(uri: URIRef, uri_to_slot: dict[str, str]) -> str:
    uri_str = str(uri)
    if uri_str in uri_to_slot:
        return uri_to_slot[uri_str]
    return to_snake_case(local_name(uri_str))


def resolve_shape_class_name(shape, graph, uri_to_class, cache) -> str:
    """Name a NodeShape after its sh:targetClass if it has one, else after its own
    local name with a trailing "_Shape" stripped -- the convention every named
    shape in these files follows (see healthdcat_ap_non_public_to_table.py in
    SandBox_LinkML, where this was first confirmed against the real files)."""
    if shape in cache:
        return cache[shape]
    target = graph.value(shape, SH.targetClass)
    name = (
        class_name_for(target, uri_to_class)
        if target is not None
        else local_name(str(shape)).removesuffix("_Shape")
    )
    cache[shape] = name
    return name


class PropertyFact:
    __slots__ = ("range_name", "is_class_like", "min_count", "max_count", "path_uri")

    def __init__(self):
        self.range_name = None
        self.is_class_like = False
        self.min_count = None
        self.max_count = None
        self.path_uri = None


def parse_shapes(graph, uri_to_slot, uri_to_class):
    """Walk every named sh:NodeShape and collect {(class, property): PropertyFact}
    plus {class: parent_class} from sh:extends. Mirrors
    healthdcat_ap_non_public_to_table.py's parse_shapes, extended to also
    capture sh:minCount/sh:maxCount (needed here for required/multivalued,
    not needed there since that script only produced a flat range table)."""
    facts: dict[tuple[str, str], PropertyFact] = {}
    shape_target: dict[str, str | None] = {}
    parents: dict[str, str] = {}
    skipped: list[str] = []
    name_cache: dict = {}
    # sh:class ranges point straight at an external class URI, not at a shape
    # node -- if that class has no NodeShape of its own among the files we
    # parsed (e.g. dpv:Purpose, only ever referenced, never shaped here), it
    # would otherwise end up as a dangling range with no class definition.
    # Keep the raw URI so build_linkml can stub in a minimal class for it.
    class_like_range_uris: dict[str, str] = {}

    for shape in graph.subjects(RDF.type, SH.NodeShape):
        if not isinstance(shape, URIRef):
            continue
        class_name = resolve_shape_class_name(shape, graph, uri_to_class, name_cache)
        target = graph.value(shape, SH.targetClass)
        shape_target[class_name] = str(target) if target is not None else None

        extended = graph.value(shape, SH_EXTENDS)
        if extended is not None:
            parents[class_name] = resolve_shape_class_name(extended, graph, uri_to_class, name_cache)

        for prop_shape in graph.objects(shape, SH.property):
            path = graph.value(prop_shape, SH.path)
            if path is None:
                skipped.append(f"{class_name}: property shape with no sh:path (sh:or/sh:and composite)")
                continue
            if not isinstance(path, URIRef):
                skipped.append(f"{class_name}: composite sh:path (e.g. sh:alternativePath), not a single property")
                continue

            prop_name = property_name_for(path, uri_to_slot)
            key = (class_name, prop_name)
            fact = facts.setdefault(key, PropertyFact())
            if fact.path_uri is None:
                fact.path_uri = str(path)

            sh_class = graph.value(prop_shape, SH["class"])
            sh_node = graph.value(prop_shape, SH.node)
            sh_datatype = graph.value(prop_shape, SH.datatype)
            if fact.range_name is None:
                if sh_class is not None:
                    fact.range_name = class_name_for(sh_class, uri_to_class)
                    fact.is_class_like = True
                    class_like_range_uris.setdefault(fact.range_name, str(sh_class))
                elif sh_node is not None:
                    fact.range_name = resolve_shape_class_name(sh_node, graph, uri_to_class, name_cache)
                    fact.is_class_like = True
                elif sh_datatype is not None:
                    fact.range_name = XSD_TYPE_NAME.get(sh_datatype, local_name(str(sh_datatype)))

            min_count = graph.value(prop_shape, SH.minCount)
            if min_count is not None:
                min_count = int(min_count)
                if fact.min_count is None or min_count > fact.min_count:
                    fact.min_count = min_count
            max_count = graph.value(prop_shape, SH.maxCount)
            if max_count is not None and fact.max_count is None:
                fact.max_count = int(max_count)

    return facts, shape_target, parents, skipped, class_like_range_uris


def parse_vocabulary_restrictions(vocab_graph):
    """Parse mdr-vocabularies.shape.ttl's controlled-vocabulary-membership
    shapes into {(target_class_uri, predicate_uri): (vocab_uris, recommended_only)}.

    Two shape patterns, both confirmed by reading the file rather than
    guessed: (1) simple "X_Restriction" shapes are just
    `sh:property [sh:path skos:inScheme; sh:hasValue <vocab-uri>]` -- "a
    valid value has this skos:inScheme". (2) "X_ShapeCV" shapes carry
    `sh:targetClass <class>` and a list of `sh:property [sh:path <predicate>;
    sh:node <RestrictionShape-or-sh:or-list-of-them>]` entries -- these are
    what actually connects a property to the vocabulary(ies) its values must
    come from. A property entry with a bare `sh:hasValue` and no
    skos:inScheme node (e.g. "Dataset must include theme .../HEAL") is a
    different kind of constraint -- a fixed required value, not "must be
    from vocabulary V" -- and isn't representable via values_from, so it's
    reported as skipped rather than silently dropped or misrepresented.
    """
    restriction_vocabs: dict = {}
    for shape in vocab_graph.subjects(RDF.type, SH.NodeShape):
        for prop in vocab_graph.objects(shape, SH.property):
            if vocab_graph.value(prop, SH.path) == SKOS.inScheme:
                val = vocab_graph.value(prop, SH.hasValue)
                if val is not None:
                    restriction_vocabs.setdefault(shape, []).append(str(val))

    def vocabs_for(node) -> list[str]:
        if node in restriction_vocabs:
            return list(restriction_vocabs[node])
        or_list = vocab_graph.value(node, SH["or"])
        if or_list is not None:
            out: list[str] = []
            for item in vocab_graph.items(or_list):
                out.extend(restriction_vocabs.get(item, []))
            return out
        return []

    bindings: dict[tuple[str, str], tuple[list[str], bool]] = {}
    skipped: list[str] = []
    for shape in vocab_graph.subjects(RDF.type, SH.NodeShape):
        target = vocab_graph.value(shape, SH.targetClass)
        if target is None:
            continue
        for prop in vocab_graph.objects(shape, SH.property):
            path = vocab_graph.value(prop, SH.path)
            if path is None or not isinstance(path, URIRef):
                continue
            node = vocab_graph.value(prop, SH.node)
            vocabs = vocabs_for(node) if node is not None else []
            if not vocabs:
                skipped.append(
                    f"{local_name(str(target))} {local_name(str(path))}: no resolvable "
                    "vocabulary (direct sh:hasValue constraint or unhandled composite)"
                )
                continue
            severity = vocab_graph.value(prop, SH.severity)
            recommended_only = severity is not None and str(severity).endswith("Warning")
            key = (str(target), str(path))
            if key in bindings:
                prev_vocabs, prev_recommended = bindings[key]
                vocabs = sorted(set(prev_vocabs) | set(vocabs))
                recommended_only = prev_recommended and recommended_only
            bindings[key] = (vocabs, recommended_only)
    return bindings, skipped


def build_rename_map(facts, shape_target, base_class_names: set[str]) -> dict[str, str]:
    """Classes whose resolved name already matches a base (dcat-ap-plus) class
    are HealthDCAT-AP *profiles* of that class (same RDF type, tighter shape)
    -- rename to Health<X>, matching chem-dcat-ap's own
    SubstanceSampleCharacterizationDataset-is_a-Dataset pattern. Classes with
    no base match (synthetic shapes like HealthAgent) keep their resolved name."""
    touched_classes = {c for c, _ in facts} | set(shape_target)
    rename: dict[str, str] = {}
    for class_name in touched_classes:
        if class_name in base_class_names:
            rename[class_name] = f"Health{class_name}"
    return rename


def build_linkml(
    base_sv: SchemaView,
    facts: dict[tuple[str, str], PropertyFact],
    shape_target: dict[str, str | None],
    shape_parents: dict[str, str],
    rename: dict[str, str],
) -> tuple[dict, dict]:
    """Return (classes, slots) LinkML dicts."""
    base_class_names = set(base_sv.all_classes(imports=True))

    def resolve_range(name: str) -> str:
        return rename.get(name, name)

    def base_slot(name: str, cls_name: str | None = None):
        # Try the class-specific induced slot first -- several base
        # dcat-ap-plus slots (contact_point, had_role, ...) declare no range
        # of their own at the top level (defaulting to "string") and are
        # only ever given a real range via per-class slot_usage (e.g.
        # Dataset.contact_point -> Kind). Calling induced_slot(name) alone,
        # with no class context, silently returns that generic "string"
        # fallback instead of the class's real range -- found by testing,
        # not assumed, when a contact_point range-recovery fix appeared to
        # have zero effect on the generated output. Falls back to the
        # classless lookup when cls_name isn't a class base_sv knows about
        # (a synthetic HealthDCAT-AP class, e.g. HealthAgent reusing
        # contact_point) -- still needed there to recognize the slot NAME
        # already exists globally, so it gets reused rather than duplicated.
        if cls_name:
            try:
                return base_sv.induced_slot(name, cls_name)
            except Exception:
                pass
        try:
            return base_sv.induced_slot(name)
        except Exception:
            return None

    classes: dict[str, dict] = {}
    slots: dict[str, dict] = {}

    touched_classes = sorted({c for c, _ in facts} | set(shape_target))
    for class_name in touched_classes:
        final_name = rename.get(class_name, class_name)
        cls: dict = {}

        if class_name in rename:
            cls["is_a"] = class_name
            cls["class_uri"] = base_sv.get_uri(class_name, expand=False)
        else:
            parent = shape_parents.get(class_name)
            if parent:
                cls["is_a"] = resolve_range(parent)
            target = shape_target.get(class_name)
            if target:
                cls["class_uri"] = to_curie(target)

        own_slots: list[str] = []
        slot_usage: dict[str, dict] = {}
        parent_name = cls.get("is_a")
        try:
            inherited_names = (
                {s.name for s in base_sv.class_induced_slots(parent_name, imports=True)}
                if parent_name
                else set()
            )
        except ValueError:
            # parent_name is itself a new HealthDCAT-AP class (not yet known
            # to base_sv, which only knows the imported dcat-ap-plus schema)
            inherited_names = set()

        for (c, prop_name), fact in facts.items():
            if c != class_name:
                continue
            range_name = resolve_range(fact.range_name) if fact.range_name else None
            required = bool(fact.min_count and fact.min_count >= 1)
            multivalued = fact.max_count is None or fact.max_count > 1

            existing = base_slot(prop_name, class_name)
            if existing is not None:
                usage: dict = {}
                if range_name is None and existing.range in rename:
                    # This property's own shape never explicitly narrowed its
                    # range (no sh:class/sh:node on THIS property) -- but its
                    # base-declared range class was independently shaped
                    # elsewhere in the same graph (e.g. :Kind_Shape,
                    # sh:targetClass vcard:Kind, required by dcat:contactPoint's
                    # value without ever being sh:node-referenced from
                    # contactPoint's own property shape). In real SHACL
                    # semantics a sh:targetClass-based shape applies to every
                    # node of that type regardless of which property pointed to
                    # it, so recovering this narrowing is restating a
                    # constraint the source SHACL actually imposes, not
                    # inventing one the mechanical per-property walk above
                    # can't see on its own.
                    range_name = rename[existing.range]
                if range_name and range_name != (existing.range or "string"):
                    usage["range"] = range_name
                if required and not existing.required:
                    usage["required"] = True
                if multivalued != bool(existing.multivalued):
                    usage["multivalued"] = multivalued
                if usage:
                    slot_usage[prop_name] = usage
                # Only needs listing under this class's own `slots:` if it
                # isn't already reachable via the is_a chain -- slot_usage
                # alone has no effect on a slot the class doesn't already use.
                if prop_name not in inherited_names:
                    own_slots.append(prop_name)
            else:
                if prop_name not in slots:
                    slot_def: dict = {}
                    if fact.path_uri:
                        slot_def["slot_uri"] = to_curie(fact.path_uri)
                    if range_name:
                        slot_def["range"] = range_name
                    if required:
                        slot_def["required"] = True
                    if multivalued:
                        slot_def["multivalued"] = True
                    slots[prop_name] = slot_def
                own_slots.append(prop_name)

        if own_slots:
            cls["slots"] = sorted(set(own_slots))
        if slot_usage:
            cls["slot_usage"] = slot_usage

        classes[final_name] = cls

    return classes, slots


def git_commit(repo_dir: Path) -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True, check=True)
    return out.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("shacl_dir", help="Directory with <tier>-shapes.ttl, <tier>-shapes_recommended.ttl, range.ttl")
    parser.add_argument("base_schema", help="Path to dcat_ap_plus.yaml (or equivalent base LinkML schema)")
    parser.add_argument("output", help="Path to write the generated LinkML YAML schema fragment to")
    parser.add_argument("--tier", choices=sorted(TIER_FILES), default="non-public")
    parser.add_argument("--healthdcat-ap-repo", help="Path to the healthdcat-ap clone, for commit-hash provenance", default=None)
    args = parser.parse_args()

    shacl_dir = Path(args.shacl_dir)
    graph = rdflib.Graph()
    for fname in TIER_FILES[args.tier]:
        parse_turtle_with_known_fixes(graph, shacl_dir / fname)

    # Parsed into its own graph, not merged into `graph` above: its
    # *Restriction/*ShapeCV shapes would otherwise also get walked by
    # parse_shapes() below (which matches on rdf:type sh:NodeShape, not on
    # source file) and misread as ordinary classes/properties -- they have a
    # structurally different shape (sh:node pointing at a restriction or
    # sh:or list, not sh:datatype/sh:class) that parse_shapes() isn't built
    # to interpret.
    vocab_graph = rdflib.Graph()
    parse_turtle_with_known_fixes(vocab_graph, shacl_dir / "mdr-vocabularies.shape.ttl")

    base_sv, uri_to_slot, uri_to_class = load_base_schema(args.base_schema)
    facts, shape_target, shape_parents, skipped, class_like_range_uris = parse_shapes(graph, uri_to_slot, uri_to_class)

    base_class_names = set(base_sv.all_classes(imports=True))
    rename = build_rename_map(facts, shape_target, base_class_names)
    classes, slots = build_linkml(base_sv, facts, shape_target, shape_parents, rename)

    # Apply controlled-vocabulary-membership bindings (mdr-vocabularies.shape.ttl)
    # onto the classes/slots build_linkml just produced.
    vocab_bindings, vocab_skipped = parse_vocabulary_restrictions(vocab_graph)
    for (target_class_uri, predicate_uri), (vocab_uris, recommended_only) in vocab_bindings.items():
        class_name = class_name_for(URIRef(target_class_uri), uri_to_class)
        final_class_name = rename.get(class_name, class_name)
        if final_class_name not in classes:
            if class_name not in base_class_names:
                vocab_skipped.append(f"{class_name}: target class not resolvable, skipping binding")
                continue
            # The tier shapes never touched this class directly, but a
            # controlled-vocabulary binding is still a real HealthDCAT-AP
            # constraint on it -- give it the same Health<X> profile
            # treatment any other touched class gets (e.g. DataService,
            # constrained here via dct:language/prov:wasGeneratedBy but not
            # by non-public-shapes.ttl itself).
            final_class_name = f"Health{class_name}"
            rename[class_name] = final_class_name
            classes[final_class_name] = {
                "is_a": class_name,
                "class_uri": base_sv.get_uri(class_name, expand=False),
            }

        slot_name = property_name_for(URIRef(predicate_uri), uri_to_slot)
        cls = classes[final_class_name]
        parent_name = cls.get("is_a")
        try:
            inherited_names = (
                {s.name for s in base_sv.class_induced_slots(parent_name, imports=True)} if parent_name else set()
            )
        except ValueError:
            inherited_names = set()
        already_applicable = slot_name in inherited_names or slot_name in cls.get("slots", [])
        if not already_applicable:
            vocab_skipped.append(
                f"{final_class_name}.{slot_name}: not an existing slot on this class, skipping values_from binding"
            )
            continue

        usage = cls.setdefault("slot_usage", {}).setdefault(slot_name, {})
        usage["values_from"] = vocab_uris
        if recommended_only:
            usage.setdefault("comments", []).append(
                "Recommended alignment (HealthDCAT-AP's own SHACL marks this sh:Warning, not sh:Violation) -- not strictly enforced."
            )

    # Closure pass: a range can point at a class (via sh:class) that has no
    # sh:NodeShape of its own in the files parsed here -- e.g. dpv:Purpose is
    # referenced as a range but only ever shaped (if at all) in
    # mdr-vocabularies.shape.ttl, which is deliberately not parsed (see module
    # docstring). Left alone this is a dangling range name with no class
    # definition, which fails schema compilation. Stub in a minimal class
    # (just its real class_uri) rather than silently dropping the reference or
    # crashing -- the honest mechanical-port answer when the source shapes
    # don't fully define something they still point at.
    referenced_ranges: set[str] = set()
    for slot_def in slots.values():
        if "range" in slot_def:
            referenced_ranges.add(slot_def["range"])
    for cls in classes.values():
        for usage in cls.get("slot_usage", {}).values():
            if "range" in usage:
                referenced_ranges.add(usage["range"])

    base_type_names = set(base_sv.all_types(imports=True)) | set(XSD_TYPE_NAME.values())
    stubbed = []
    for name in sorted(referenced_ranges):
        if name in classes or name in base_class_names or name in base_type_names:
            continue
        stub: dict = {
            "description": (
                "External vocabulary term referenced by a HealthDCAT-AP shape "
                "but not itself defined by a sh:NodeShape anywhere in HealthDCAT-AP's "
                "own release -- confirmed, not assumed: it doesn't appear in the tier "
                "shapes files or in mdr-vocabularies.shape.ttl (which this port does "
                "parse, for controlled-vocabulary bindings on other properties -- see "
                "script docstring); it's a pointer into an external ontology (DPV/DQV) "
                "HealthDCAT-AP never embeds. Carries just id: real usage is a reference "
                "to an external controlled-vocabulary term (e.g. a DPV Purpose/LegalBasis "
                "URI), not a locally-described object -- and a slotless class "
                "can only ever be instantiated as {}, which linkml_runtime's "
                "own YAML loader rejects outright ('Empty list elements are "
                "not allowed'), making a slotless required range unusable in "
                "practice, not just thin."
            ),
            # Every class here is a bare external-term reference, so "id" is
            # the one slot that makes it real without inventing a shape
            # HealthDCAT-AP itself never gave it.
            "slots": ["id"],
        }
        uri = class_like_range_uris.get(name)
        if uri:
            stub["class_uri"] = to_curie(uri)
        classes[name] = stub
        stubbed.append(name)

    source_commit = None
    if args.healthdcat_ap_repo:
        source_commit = git_commit(Path(args.healthdcat_ap_repo))

    header_lines = [
        "# GENERATED FILE -- do not hand-edit.",
        f"# Ported from HealthDCAT-AP's {args.tier} SHACL shapes by",
        "# scripts/port_healthdcat_ap_shacl_to_linkml.py -- re-run that script to",
        "# regenerate after editing it or after HealthDCAT-AP publishes a new release.",
        f"# Source: {shacl_dir}",
    ]
    if source_commit:
        header_lines.append(f"# healthdcat-ap commit: {source_commit}")
    header_lines.append(f"# Generated: {dt.date.today().isoformat()}")

    schema = {
        "id": f"https://w3id.org/portail-fresh/Health-DCAT-AP-Plus/healthdcat_ap_{args.tier.replace('-', '_')}",
        "name": f"healthdcat_ap_{args.tier.replace('-', '_')}",
        "title": f"HealthDCAT-AP ({args.tier} tier), ported from SHACL",
        "description": (
            f"LinkML port of HealthDCAT-AP's {args.tier}-tier SHACL shapes, generated "
            "mechanically (not hand-modeled) by scripts/port_healthdcat_ap_shacl_to_linkml.py, "
            "the same targetClass/sh:property-walking method NFDI4Chem used to port plain "
            "DCAT-AP's SHACL when building chem-dcat-ap."
        ),
        "license": "MIT",
        "prefixes": dict(PREFIXES),
        "default_prefix": "health_dcat_ap_plus",
        "default_range": "string",
        "imports": ["linkml:types", "dcatapplus:latest/schema/dcat_ap_plus"],
        "classes": classes,
        "slots": slots,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    import yaml

    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(header_lines) + "\n")
        yaml.safe_dump(schema, f, sort_keys=False, allow_unicode=True, width=100)

    n_profile = len(rename)
    print(f"HealthDCAT-AP {args.tier}: {len(facts)} shape-derived (class, property) facts")
    print(f"-> {len(classes)} classes ({n_profile} profile subclasses of dcat-ap-plus, {len(classes) - n_profile} new)")
    print(f"-> {len(slots)} new top-level slots")
    if stubbed:
        print(f"-> {len(stubbed)} stub class(es) for externally-referenced-but-unshaped ranges: {', '.join(stubbed)}")
    n_applied_bindings = sum(1 for c in classes.values() for u in c.get("slot_usage", {}).values() if "values_from" in u)
    print(f"-> {n_applied_bindings} controlled-vocabulary (values_from) binding(s) applied from mdr-vocabularies.shape.ttl")
    print(f"Written to {out_path}")
    if skipped:
        print(f"\nSkipped {len(skipped)} composite constraint(s), not representable as a single property:")
        for s in skipped:
            print(f"  - {s}")
    if vocab_skipped:
        print(f"\nSkipped {len(vocab_skipped)} vocabulary binding(s) from mdr-vocabularies.shape.ttl:")
        for s in vocab_skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()

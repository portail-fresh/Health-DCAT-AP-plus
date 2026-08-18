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
from rdflib.namespace import RDF, SH, XSD

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

    return facts, shape_target, parents, skipped


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

    def base_slot(name: str):
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

            existing = base_slot(prop_name)
            if existing is not None:
                usage: dict = {}
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
        graph.parse(shacl_dir / fname, format="turtle")

    base_sv, uri_to_slot, uri_to_class = load_base_schema(args.base_schema)
    facts, shape_target, shape_parents, skipped = parse_shapes(graph, uri_to_slot, uri_to_class)

    base_class_names = set(base_sv.all_classes(imports=True))
    rename = build_rename_map(facts, shape_target, base_class_names)
    classes, slots = build_linkml(base_sv, facts, shape_target, shape_parents, rename)

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
    print(f"Written to {out_path}")
    if skipped:
        print(f"\nSkipped {len(skipped)} composite constraint(s), not representable as a single property:")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()

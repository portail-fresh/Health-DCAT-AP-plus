# Architecture verification: the Health-DCAT-AP-plus merge layer

Context: [nfdi-de/dcat-ap-plus Discussion #109](https://github.com/nfdi-de/dcat-ap-plus/discussions/109),
where the `dcat-ap-plus` maintainers (Hendrik Borgelt, Philip Strömert) confirmed
the intended architecture — this repo imports the LinkML port of HealthDCAT-AP's
SHACL plus `dcat-ap-plus` itself, as one clean intermediate layer. A *separate*
downstream repo specializes it further (roles, `ResearchStudy`-shaped classes,
...) — that specialization work does not belong here.

This document has two parts. The first documents *how the port itself works*
— what it reads, what it deliberately doesn't, what's been found and fixed
along the way. The second tracks the specific points we want 100% confidence
on in the *merged result*, one at a time: what's checked, how, and the
result. Each section states a claim, the check that was run to confirm or
refute it, and the actual output — not just an assertion.

## Import hierarchy (per Hendrik Borgelt's comment, Discussion #109)

Hendrik pointed at `dcat-ap-plus`'s own [extension rules](https://nfdi-de.github.io/dcat-ap-plus/latest/how-to-extend/)
as the requirement for "a correct import hierarchy." Checked directly, not
assumed — five concrete rules, each checked against what this repo actually
does:

| Rule (their docs, verbatim) | This repo |
| --- | --- |
| "Import the full DCAT-AP+ schema in your LinkML schema's `imports` section" | `health_dcat_ap_plus.yaml` imports `dcatapplus:latest/schema/dcat_ap_plus` (the w3id permalink, full schema) — not a cherry-picked subset. |
| Extend classes via `is_a` | Every ported class (`HealthDataset`, `HealthAgent`, `HealthCatalogue`, ...) is `is_a: <base class>` — the core mechanism of the whole port script, not an afterthought. |
| "Create sub-slots using `is_a` on slots for stricter constraints" | Not yet used — see open item below. |
| Never modify `class_uri`/`slot_uri` on imported elements | Confirmed by construction: every `slot_usage` override in the port script only ever sets `range`/`required`/`multivalued`/`values_from` — never `slot_uri`. `class_uri` on a `Health<X>` class is always the *same* URI as its base, never a modification of the base's own definition (checked in §1 Check a — one shared SHACL shape, not two). |
| Avoid broadening cardinality on inherited properties | Every tightening found goes one direction: optional→required, or narrower `range`. Never loosens an inherited `required: true` back to `false` (confirmed elsewhere this session to be a real LinkML limitation even if attempted — a subclass's `slot_usage` can't suppress an ancestor's own required-field check). |
| Never add domain-specific classes directly to `dcat-ap-plus` itself | `repos/dcat-ap-plus` is a read-only clone (gitignored), never edited — every health-specific class lives in this repo's own `healthdcat_ap_non_public.yaml`. |

**Open item, not yet acted on:** the "sub-slots via `is_a` on slots" rule has
no example in this port yet — worth watching for once the specialization
repo starts adding roles/relations of its own, since none of the tightening
done so far needed a new slot that specializes an *existing* slot via `is_a`
(as opposed to a genuinely new top-level slot, which the port does use, e.g.
`health_category`).

## Porting HealthDCAT-AP's SHACL to LinkML

`scripts/port_healthdcat_ap_shacl_to_linkml.py` — same method NFDI4Chem used
to port plain DCAT-AP's SHACL to LinkML when building `chem-dcat-ap`: walk
every `sh:NodeShape`, turn one with a `sh:targetClass` into a LinkML class,
turn its `sh:property` shapes into slots. See the script's own docstring for
the full three-bucket mechanism (profile subclass of an existing `dcat-ap-plus`
class / genuinely new class / cardinality-tightening on an inherited slot).
This section covers what it reads, what it doesn't, and what building it for
real (not just trusting the mechanism) has turned up.

**What's parsed, per tier:** `<tier>-shapes.ttl` (mandatory constraints),
`<tier>-shapes_recommended.ttl` (recommended, non-mandatory), `range.ttl`
(class-range constraints, shared across tiers). Plus, as of this session,
`mdr-vocabularies.shape.ttl` (see "Controlled-vocabulary bindings" below).

**What's deliberately not parsed, and why that's actually fine — checked, not
assumed:**
- `imports.ttl` / `mdr_imports.ttl` — read directly: pure `owl:imports`
  manifests, lists of external ontology/vocabulary URLs (`prov-o.ttl`,
  `dqv.ttl`, the EU health-category codelist endpoint, ...). Zero
  `sh:NodeShape`/`sh:property` content — there is nothing structural in them
  to miss.
- `deprecateduris.ttl` — a deprecated→current URI mapping table, not shape
  content.

**Known issues found while building this, not visible from schema
introspection alone — this is why building real instances and generated
artifacts matters, not just trusting the mechanical walk:**

1. **Fixed — zero-slot stub classes.** Four classes HealthDCAT-AP's shapes
   reference as ranges (`Purpose`, `LegalBasis`, `PersonalData`,
   `QualityCertificate` — via `has_purpose`/`has_legal_basis`/
   `has_personal_data`/`has_quality_annotation` on `HealthDataset`) have no
   `sh:NodeShape` of their own *anywhere* in HealthDCAT-AP's release —
   confirmed by grepping every file, tier shapes and `mdr-vocabularies.shape.ttl`
   both, for zero matches. Root cause, confirmed by asking rather than
   assuming: these genuinely are pointers into external ontologies (DPV —
   Data Privacy Vocabulary, DQV — Data Quality Vocabulary) that HealthDCAT-AP
   references (`sh:class dpv:Purpose`) but never embeds a shape for. The port
   correctly stubbed them as classes, but with *zero slots* — and a
   zero-slot class can only ever be instantiated as `{}`, which
   `linkml_runtime`'s own YAML loader unconditionally rejects ("Empty list
   elements are not allowed" — `linkml_runtime/utils/yamlutils.py`,
   `seq_constructor`). Since all four are `required: true` on `HealthDataset`,
   this meant **`HealthDataset` was structurally unloadable via
   `linkml-convert` no matter what data you provided.** Fixed by giving each
   stub an `id` slot — the correct fix, not a workaround: real usage is a
   reference to an external controlled-vocabulary term (e.g. a DPV `Purpose`
   URI), so `id` is what they actually need. Side benefit: with exactly one
   slot (the identifier), LinkML treats references to them as bare identifier
   strings rather than nested objects.

2. **Fixed — `contact_point`'s range was never actually disconnected from
   `HealthKind`; the port script's per-property walk just couldn't see the
   connection.** `Kind` (`vcard:Kind`, `Dataset.contact_point`'s range) is a
   zero-slot stub in `dcat-ap-plus` itself, confirmed by reading its schema
   directly. HealthDCAT-AP's own shapes tighten `contact_point`'s
   *cardinality* only (`sh:minCount 1`, no `sh:class`/`sh:node`) — but
   *separately* define `:Kind_Shape` (`sh:targetClass vcard:Kind`, requiring
   `vcard:hasURL`/`vcard:hasEmail`), which the port already turns into
   `HealthKind`. First write of this document claimed these two were
   unconnected in the source and that narrowing `contact_point` to
   `HealthKind` locally "would mean inventing a connection" — **that was
   wrong**, caught when a user asked why a plain DCAT-AP property/class pair
   was being blamed on `dcat-ap-plus` at all. In real SHACL semantics, a
   `sh:targetClass`-scoped shape applies to *every* node of that type,
   regardless of which property pointed to it — no explicit `sh:node`
   chaining required. The connection genuinely exists in the source; the
   port script's range resolution just only ever looked at `sh:class`/
   `sh:node` on a property's *own* shape, never at whether some other,
   independently-walked shape already targets that property's declared base
   range. Fixed in `build_linkml`: when a fact has no explicit range
   narrowing but the inherited slot's own base range is itself a class that
   got profiled elsewhere in the same run, recover that as the range — not
   an invention, a restatement of what `sh:targetClass` already implies.
   `HealthDataset.contact_point` now correctly resolves to `HealthKind`, and
   converts to real RDF end to end (confirmed via `linkml-convert`, not just
   schema introspection).

   Same fix also surfaced and corrected an unrelated, latent bug in the base
   comparison logic: `base_slot()` compared a fact against
   `induced_slot(name)` with **no class context**, silently falling back to
   a slot's generic top-level definition (often just `range: string`, the
   schema default) for any slot — like `contact_point`, like `had_role` —
   whose real range is only ever set via per-class `slot_usage` in
   `dcat-ap-plus` itself. Fixed by passing the class name through; verified
   by diffing the full regenerated output line by line rather than trusting
   the change was safe, since it also correctly dropped several now-redundant
   `multivalued: true` restatements elsewhere (confirmed still correct by
   full regeneration, `pytest`, and a real instance test, not assumed safe).

3. **Found, not fixed — a separate, pre-existing LinkML code-gen limitation
   (same class as the `metadata_contributor` quirk already documented in
   `HealthStudy-DCAT-AP`'s modeling guide).** `Dataset.frequency` is
   single-valued at the base; HealthDCAT-AP tightens it to `multivalued: true`
   on `HealthDataset`, correctly expressed in `slot_usage`. But the generated
   `HealthDataset.__post_init__` correctly wraps the value into a list, then
   unconditionally calls `super().__post_init__()` — `Dataset`'s own
   single-valued construction logic — which re-processes the now-list value
   with `Frequency(**as_dict(self.frequency))`, crashing
   (`TypeError: argument after ** must be a mapping, not list`). Not a schema
   authoring mistake (the `slot_usage` is correct and necessary), not
   something this session's fixes caused (confirmed: `frequency`'s
   `multivalued: true` restatement is present, untouched, before and after)
   — a genuine gap in how LinkML generates `__post_init__` for a slot whose
   multivalued-ness a subclass narrows in either direction. `HealthDataset`
   is loadable via `linkml-convert` for every other field (`contact_point`
   included, per the fix above) but not yet fully instantiable end to end
   because of this one slot — worth raising upstream (with LinkML itself,
   not `dcat-ap-plus`) rather than working around locally.

4. **Found and fixed — a real inconsistency within HealthDCAT-AP's own
   release.** `range.ttl` and `mdr-vocabularies.shape.ttl` declare
   `@prefix dcatap: <http://data.europa.eu/r5r>` — missing the trailing
   slash that `<tier>-shapes.ttl`/`<tier>-shapes_recommended.ttl` *and*
   `dcat-ap-plus`'s own schema (`dcatap: http://data.europa.eu/r5r/`) both
   have. Confirmed by reading all four files' own `@prefix` lines directly,
   not assumed. Per the Turtle spec this makes every `dcatap:X` term in
   those two files expand to a malformed, concatenated URI (e.g.
   `dcatap:availability` → `.../r5ravailability` instead of
   `.../r5r/availability`), silently failing to match any real `dcat-ap-plus`
   slot — caught because `HealthDistribution` ended up with a nonsense
   `r5ravailability` slot instead of the real `availability` one. Corrected
   before parsing (`parse_turtle_with_known_fixes` in the port script) since
   the right namespace is unambiguous (3 of 4 sources agree) — worth
   reporting upstream, but not a judgment call worth leaving broken locally.

5. **Fixed — controlled-vocabulary bindings from `mdr-vocabularies.shape.ttl`
   are now captured.** This file (35 `NodeShape`s, all named
   `*Restriction`/`*ShapeCV`) doesn't add classes or properties — confirmed:
   none of the four stub classes above or their predicates appear in it
   either — it adds *value-set* metadata to properties already ported:
   "`dct:language`'s value must be `skos:inScheme <the EU language NAL>`,"
   etc. Recorded via LinkML's own `values_from` slot metaslot (a value-set
   *reference*, explicitly not an expanded enum — see its docstring in the
   LinkML metamodel), not by fetching and inlining the actual external
   vocabularies, which would be a separate, much larger undertaking. Example,
   from the real generated output:

   ```yaml
   HealthDataset:
     slot_usage:
       theme:
         values_from:
           - http://publications.europa.eu/resource/authority/data-theme
       health_theme:
         values_from:
           - https://hdeu-dcat.acceptance.data.health.europa.eu/resource/authority/health-theme
   ```

   21 bindings resolved and applied (across `HealthDataset`, `HealthDistribution`,
   `HealthCatalogue`, and two classes the tier shapes never touched directly
   but this file does — `HealthDataService`, `HealthLicenseDocument`, created
   the same way any other touched class is). 8 correctly *not* representable
   this way, reported rather than silently dropped — spot-checked several
   rather than assumed all fine: `dct:publisher`'s restriction points at
   *another* `*_ShapeCV` (`HealthPublisherAgent_ShapeCV`), i.e. "conform to
   this whole shape," not "come from this vocabulary" — a different,
   recursive kind of constraint `values_from` can't represent; `dcat:theme`'s
   second entry and `dcat:themeTaxonomy` are bare `sh:hasValue` business
   rules ("must include theme HEAL"), not vocabulary membership; IANA
   media-type restrictions (`dcat:mediaType`/`compressFormat`/`packageFormat`)
   use `sh:pattern` (a regex), a different SHACL constraint type entirely —
   confirmed by reading `IANARestriction`'s own shape, not assumed.

**Coverage status:** `non-public` tier done. `public`/`restricted` not yet
ported — same file pattern (`--tier public`/`--tier restricted`), should
carry over directly per the script's own design.

**Evaluated, not adopted: [mleist/shacl-linkml-tools](https://github.com/mleist/shacl-linkml-tools).**
A general-purpose, bidirectional SHACL↔LinkML converter with a round-trip
isomorphism test and real CI — and genuinely broader SHACL coverage than our
script (`sh:in`, `sh:pattern`, value bounds, `sh:sparql`, `sh:or`/`sh:and`
preserved as annotations). Not a replacement, though: it's a standalone
one-file-in/one-file-out converter with no concept of merging against an
already-imported base schema — no notion of "this class already exists in
`dcat-ap-plus`, specialize it as `Health<X>` with the same `class_uri`,"
which is the actual hard, valuable part of this port. It also doesn't
mention `sh:extends` (the non-standard term `HealthAgent`'s shape uses) at
all. Worth reading `shacl_reader.py` later for `sh:pattern`/`sh:in` handling
ideas (we currently skip both — see the IANA case above) — not worth
swapping in.

## 1. Merge resolution: does `Dataset` really get the health attributes, and do `AgenticEntity`/`Activity` stay untouched?

**Claim:** `HealthDataset` (the port's specialization of `Dataset`) carries the
complete union of both schemas' properties — nothing from `dcat-ap-plus` is
lost by specializing, and nothing outside `Dataset`/`Catalogue`/`Agent`/
`Distribution`/`DatasetSeries`/`Kind` (the classes HealthDCAT-AP's SHACL
actually constrains) is touched by the port at all.

**Check a. — is the merge complete?** `SchemaView.class_induced_slots`
(LinkML's own authoritative resolver for "every slot a class has, own +
inherited") on both classes:

```
Dataset (dcat-ap-plus):  39 own+inherited slots
HealthDataset:           62 own+inherited slots
Missing from HealthDataset: NONE
```

Confirmed at two more levels, not just the schema: the generated Python
dataclass has all 62 as constructor fields (`title`, `publisher`,
`contact_point`, ... sitting alongside `health_category`, `hdab`,
`custodian`, ...); and the generated SHACL emits **one single** `NodeShape`
for `dcat:Dataset` with 49 `sh:property` entries — because `HealthDataset`
shares the exact same `class_uri: dcat:Dataset` as the base class, there is
no separate "HealthDataset shape" a consumer could apply while missing the
other. This is deliberate, not an accident of the port: it mirrors how
`chem-dcat-ap` itself specializes `Dataset` (e.g.
`SubstanceSampleCharacterizationDataset is_a Dataset, class_uri: dcat:Dataset`
— confirmed by reading its schema directly), and it matches HealthDCAT-AP's
own real design, which constrains `dcat:Dataset` directly rather than
declaring a new RDF type.

**Check b. — is anything outside the ported classes touched?**

```bash
grep -n "AgenticEntity\|DataGeneratingActivity\|^  Activity:" \
  src/health_dcat_ap_plus/schema/healthdcat_ap_non_public.yaml
# -> no matches
```

The generated HealthDCAT-AP layer (`healthdcat_ap_non_public.yaml`) never
mentions `AgenticEntity`, `Activity`, or `DataGeneratingActivity` — they
aren't reachable from HealthDCAT-AP's SHACL shapes at all (it constrains
dataset/catalog/agent-level classes, not the Activity/provenance side), so
the port script never had a reason to touch them. Confirmed directly via
`SchemaView.get_class(...).from_schema`, which reports both classes as
originating from `https://w3id.org/nfdi-de/dcat-ap-plus/` — the real,
unmodified upstream schema, not a local shadow/override.

**Result: confirmed.** The merge is additive and complete on the `Dataset`
side, and a strict no-op on the `AgenticEntity`/`Activity` side. This is the
foundation the rest of this document's checks build on.

**Check c. — real instances, not just schema introspection.** Checks a-b
above are schema-level (`class_induced_slots`, `from_schema`) — real enough,
but not proof that a real instance actually exercises the provenance
triangle DCAT-AP+ built for exactly this purpose: `Dataset.was_generated_by`
(`prov:wasGeneratedBy`, → `DataGeneratingActivity`), `Dataset.is_about_entity`
(`dcterms:subject`, → `EvaluatedEntity`), `Dataset.is_about_activity`
(`dcterms:subject`, same predicate, → `EvaluatedActivity`). Built a real
instance with all three populated and pushed it through `linkml-validate`
and `linkml-convert` end to end (the two bugs this surfaced — the stub-class
and `dcatap:` prefix issues — are documented in the Porting section above,
where they belong; this section keeps just the result). Result:

```turtle
<https://example.org/dataset/cancer-registry-2024> a dcat:Dataset ;
    dcterms:subject <https://example.org/activity/diagnostic-reporting-process>,
        <https://example.org/population/regional-cancer-patients-2024> ;
    prov:wasGeneratedBy <https://example.org/activity/cancer-registry-collection-2024> .

<https://example.org/activity/cancer-registry-collection-2024> a prov:Activity ; ...
<https://example.org/activity/diagnostic-reporting-process> a prov:Activity ; ...
<https://example.org/population/regional-cancer-patients-2024> a prov:Entity ; ...
```

Confirmed on `HealthDataset` specifically for validation (a full, entirely
schema-valid `HealthDataset` instance carrying all three properties passes
`linkml-validate` cleanly — proving the merge doesn't just leave these slots
present but structurally usable together with the health-specific ones).
The RDF conversion above is shown on plain `Dataset`; a full `HealthDataset`
instance was also built and converts correctly for every field including
`contact_point` (once genuinely blocked here, now fixed — §Porting #2) —
it's not shown in full because one unrelated field, `frequency`, still hits
the separate LinkML code-gen limitation documented at §Porting #3. Neither
blocker touches `was_generated_by`/`is_about_entity`/`is_about_activity`
themselves, which Check a already proved are inherited by `HealthDataset`
completely unchanged, so the `Dataset`-level result above is equivalent
evidence for `HealthDataset` too.

Minor, unrelated finding while building the test data: `EvaluatedEntity.title`
is single-valued while `EvaluatedActivity.title` (and `Dataset.title`,
`DataGeneratingActivity.title`) are multivalued — an inconsistency worth
knowing when authoring instances, not necessarily a bug worth raising.

## 2. `AgenticEntity` vs `Agent` — confidence in the intended usage

**Claim (per the maintainers, Discussion #109):** `Agent` (`foaf:Agent`) is
for "who published/created this dataset" (Entity-scoped, DCAT-AP proper);
`AgenticEntity` (`prov:Agent`) is for "who was associated with the
*activity* that produced it" (Activity-scoped, DCAT-AP+'s own PROV-O layer)
— deliberately kept as two separate hierarchies rather than merged, to stay
faithful to the PROV-O pattern rather than overloading `Agent`.

**Check — is this structurally real, not just documentation?**

```
Dataset.publisher:  range=Agent          slot_uri=dcterms:publisher
Dataset.creator:    range=Agent          slot_uri=dcterms:creator
DataGeneratingActivity.carried_out_by: range=AgenticEntity  slot_uri=prov:wasAssociatedWith

Agent:          class_uri=foaf:Agent, is_a=None, mixins=[]
AgenticEntity:  class_uri=prov:Agent,  is_a=None, mixins=[ClassifierMixin]

Agent ancestors:         [Agent]                       -- fully independent
AgenticEntity ancestors: [AgenticEntity, ClassifierMixin]  -- no relation to Agent
```

`class_ancestors` confirms there is no `is_a`/mixin relationship between the
two at all — genuinely two separate hierarchies, exactly as described.

**Check — does the HealthDCAT-AP port respect this, or blur it?** The port
introduced two agent-like classes (`hdab`/`custodian`/`publisher` are all
Entity-scoped concepts — "who published/is responsible for this dataset,"
not an Activity role):

```
HealthAgent:          is_a=Agent  (ancestors: [HealthAgent, Agent])
HealthPublisherAgent: is_a=Agent  (ancestors: [HealthPublisherAgent, Agent])
```

Both correctly specialize `Agent`, not `AgenticEntity` — consistent with
their real semantics.

**Result: confirmed**, both for the base schema and for the port.

## 3. `id` and `other_identifier` on `AgenticEntity` — ORCID/ROR/IdRef readiness

*Pending.*

## 4. `qualified_attribution` (Entity-side, `Dataset`) — does it actually work?

*Pending.* Known concern going in, from having built this in
`HealthStudy-DCAT-AP`: `dcat-ap-plus`'s own `Attribution` class only has
`title`/`description` — `agent`/`had_role` were never wired up. "Works" here
needs to mean something concrete: does a `HealthDataset` instance with a
real `qualified_attribution` (PI/processor role, ORCID-identified agent)
validate and convert to the same shape as HealthDCAT-AP's own real
documentation example?

## 5. `qualified_association` (Activity-side, symmetric via `carried_out_by`/`prov:wasAssociatedWith`) — readiness

*Pending.* `dcat-ap-plus` has no `Association` class at all (only built the
Entity-side `Attribution` pattern) — same situation as #4 but starting from
further behind. Open question to resolve here vs. leave to the specialization
repo: does the `Association` mechanism belong in this merge layer (reusable
by any downstream specialization) or is it specific enough to defer?

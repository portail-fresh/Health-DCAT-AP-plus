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

3. **Found, and fixed at the port-repo level — a separate, pre-existing
   LinkML code-gen limitation (same class as the `metadata_contributor`
   quirk already documented in `HealthStudy-DCAT-AP`'s modeling guide).**
   `Dataset.frequency` is single-valued at the base; HealthDCAT-AP tightens
   it to `multivalued: true` on `HealthDataset`, correctly expressed in
   `slot_usage`. But the generated `HealthDataset.__post_init__` correctly
   wraps the value into a list, then unconditionally calls
   `super().__post_init__()` — `Dataset`'s own single-valued construction
   logic — which re-processes the now-list value with
   `Frequency(**as_dict(self.frequency))`, crashing (`TypeError: argument
   after ** must be a mapping, not list`). Not a schema authoring mistake
   (the `slot_usage` is correct and necessary) — a genuine gap in how
   LinkML generates `__post_init__` for a slot whose range or
   multivalued-ness a subclass narrows in either direction, worth raising
   upstream with LinkML itself eventually. Confirmed not limited to this
   one field either: the exact same crash reproduces on
   `HealthDistribution.format` (a different class, different base,
   confirmed independently) — this was always going to recur for every
   `Health<X>` field the vocab-range fix (§6) touched, not just
   `HealthDataset`'s.

   **Now fixed for real, not just worked around in tests.**
   `scripts/patch_post_init_shielding.py` runs as a permanent step of both
   `just gen-python` and `just gen-project` (right after the dataclasses
   are generated, before anything else uses them) — see the script's own
   docstring for the full mechanism. In short: it derives, straight from
   the schema (not a hand-maintained list), every class that narrows a
   slot in a way the parent's own generated coercion can't safely
   re-process, and rewrites that one `super().__post_init__(**kwargs)`
   line into a block that saves the already-correct values, blanks them so
   the parent's re-processing is a no-op, calls the parent, then restores
   them. Deliberately not a global, import-time monkeypatch (considered
   and rejected — see the session's own discussion): it only ever touches
   each affected class's own generated method body, so constructing a
   plain, un-profiled `dcat-ap-plus` class elsewhere in the same process is
   completely unaffected. Confirmed the fix is real, not just papering
   over the test: `tests/test_shacl_validation.py`'s own fixture-building
   helper no longer needs *any* construction workaround for these fields —
   `HealthDataset(**data)` now just works, exactly as a downstream
   consumer would call it. The schema-derived scan also caught the same
   pattern purely inside `dcat-ap-plus`'s own class hierarchy
   (`Concept`, `ConceptScheme`, `PeriodOfTime`), unrelated to anything
   this repo's port does — fixed for free by not hand-limiting the scan to
   `Health<X>` classes.

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

**Claim:** `AgenticEntity` has a required `id` (a real URI — an ORCID/ROR IRI
can be used directly as the subject) plus an optional, multivalued
`other_identifier` (range `Identifier`: `title` + `notation`) for a second
scheme when an agent has more than one — e.g. ORCID as `id`, IdRef as
`other_identifier`.

**Check — schema-level.**

```
AgenticEntity.id:               range=uriorcurie  required=True
AgenticEntity.other_identifier: range=Identifier   multivalued=True  slot_uri=adms:identifier
Identifier class: slots=[notation, title, description], class_uri=adms:Identifier
```

Cross-checked against `dcat-ap-plus`'s own published docs
([`AgenticEntity`](https://nfdi-de.github.io/dcat-ap-plus/latest/elements/classes/AgenticEntity/)),
not just the source YAML — matches exactly (`id`: required `Uriorcurie`;
`other_identifier`: optional, range `Identifier`). Their docs also confirm
`Device`/`Software` as the only currently-modeled `AgenticEntity` subclasses
— matching Hendrik's own comment in Discussion #109 about why those two
specifically ("some people argue about whether both concepts can be
considered to be a `foaf:Agent` and `prov:agent`").

**Check — a real instance, not just the schema.** Built the exact ORCID+IdRef
example from Discussion #109 and pushed it through validation and
conversion:

```turtle
<https://orcid.org/0000-0002-1825-0097> a prov:Agent ;
    dcterms:title "Josiah Carberry" ;
    adms:identifier [ a adms:Identifier ;
            dcterms:title "IdRef" ;
            skos:notation "069774160" ] .
```

Matches the discussed pattern exactly: the ORCID URI is the subject itself
(not a separate `id` property triple — `id`-as-subject is how LinkML
identifier slots serialize, confirmed by every instance converted this
session, not just this one), IdRef sits alongside as a secondary
`adms:identifier`.

**Result: confirmed** for `AgenticEntity` itself.

**A real gap this surfaced, worth flagging: `Agent` has *neither* `id` nor
`other_identifier` at all — not even a thin version.** Checked directly
against `dcat-ap-plus`'s own class definition, not inferred: `Agent`'s
entire slot list is `[name, type]`. This matters here specifically because
`HealthAgent`/`HealthPublisherAgent` — the classes this port already built
for `hdab`/`custodian`/`publisher` — specialize `Agent`, not `AgenticEntity`.
Concretely: there is currently no way to record a ROR ID (or any identifier
at all) for the Health Data Access Body or a dataset's custodian, even
though those are exactly the kind of organizations you'd want to identify
precisely. Worth deciding, not silently working around: either raise this
with the `dcat-ap-plus` maintainers (a natural companion to the
`Attribution`-has-no-`agent` and `Kind`-had-a-disconnected-shape findings —
same pattern, a class shipped thinner than its real-world use needs), or add
`id`/`other_identifier` locally on `HealthAgent`/`HealthPublisherAgent`
specifically, the same way `contact_point` was locally recovered in §Porting
#2 — except this time there's no existing HealthDCAT-AP shape to recover it
from; it would be a genuinely new addition, which is a bigger call than a
mechanical fix and shouldn't be made silently here.

**Methodological note, worth remembering for the rest of this document and
beyond:** `SchemaView.induced_slot(name, class_name)` does **not** reliably
signal "is this slot actually applicable to this class" — called with a
slot name a class doesn't really use, it can still return a plausible-looking
generic fallback instead of raising. This produced a real false trail while
building this section (`Agent.id`/`Agent.other_identifier`/`Agent.contact_point`
all appeared to "exist" via this call, with values that turned out to be
generic top-level defaults, not real class-applicable slots). The reliable
check is `class_induced_slots(class_name)` and checking *membership* in its
result — used throughout §1 already, and used to catch this specific false
trail once it looked suspicious.

## 4. `qualified_attribution` (Entity-side, `Dataset`) — does it actually work?

**Claim going in:** `dcat-ap-plus`'s own `Attribution` class has only
`title`/`description` — `agent`/`had_role` were never wired up, confirmed
directly (§Porting also references this). Re-confirmed here: neither
`Attribution` nor `qualified_attribution` appear anywhere in HealthDCAT-AP's
own SHACL either — this is a generic `dcat-ap-plus` gap, not something
HealthDCAT-AP could have fixed even if it wanted to.

**A real architecture question this raised, resolved before fixing
anything:** `HealthStudy-DCAT-AP` already built and verified this exact fix
(`DatasetAttribution`, `agent`, `had_role`) — but it can't just be copied
over mechanically, because *where* it needed to attach differs. There,
`ResearchDataset` (the class needing `qualified_attribution` narrowed) is
hand-authored directly in the main schema, so adding a sibling class in the
same file was trivial. Here, `HealthDataset` is *mechanically generated* by
the port script into `healthdcat_ap_non_public.yaml` — LinkML has no clean
way to layer more `slot_usage` onto an already-imported class from the
hand-authored main schema, and hand-editing a file marked "generated, do not
edit" would just get silently wiped on the next port run. Resolved by
extending the port script itself with an explicit, clearly-labeled
completion step (same pattern as the `dcatap:` prefix fix) — applied
programmatically, survives regeneration, but honestly documented as *not*
derived from HealthDCAT-AP's SHACL, unlike everything else the script
produces.

**Fixed, then corrected against HealthDCAT-AP's own real example.** First
pass reused `HealthStudy-DCAT-AP`'s exact design as-is (`agent`: `prov:agent`
→ `AgenticEntity`, `had_role`: `dcat:hadRole` → `Role`), flagging the
`AgenticEntity`-vs-`Agent` choice as an open, unresolved nuance. It wasn't
just a nuance — checking HealthDCAT-AP's own real documentation example
(release-7, `#provqualifiedAttribution`, fetched directly) turned up two
real mismatches:

```turtle
<https://fair.healthdata.be/dataset/...> a dcat:Dataset ;
    prov:qualifiedAttribution [ a prov:Attribution;
        dcat:hadRole <https://standards.iso.org/iso/19115/resources/Codelists/gml/CI_RoleCode.xml#processor>;
        prov:agent [ a foaf:Agent, foaf:Organization; dct:type <...>; foaf:name "Germany processor"; foaf:homepage <...>; foaf:mbox <...> ]
    ] .
```

1. `prov:agent`'s value is typed `foaf:Agent, foaf:Organization` — no
   `prov:Agent` at all. `qualified_attribution` is `Dataset`'s own
   Entity-side mechanism, so its agent should be Entity-scoped (`Agent`),
   matching `Dataset.publisher`/`creator`'s own range — not `AgenticEntity`
   (Activity-scoped, correct for `Association`'s agent, wrong here). Split
   into two separate slots: `attribution_agent` (`Agent`, for
   `DatasetAttribution`) and `agent` (`AgenticEntity`, for `Association`,
   §5) — conflating them under one shared slot was the original mistake,
   inherited unquestioned from `HealthStudy-DCAT-AP`.
2. `dcat:hadRole`'s value is a bare URI into an external codelist (ISO
   19115 `CI_RoleCode`), not a nested `dcat:Role` object with
   `title`/`description`. Tried `range: Role` first — a bare URI failed
   validation ("not of type object"). Tried `any_of: [{range: Role},
   {range: uriorcurie}]` next — the bare URI then validated, but broke the
   object form entirely, regardless of which alternative was listed first
   (tested both orderings). A class-plus-scalar `any_of` union not reliably
   supporting both shapes matches exactly what NFDI4Chem's own paper flagged
   for union ranges in general — not a fluke. Settled on `range: uriorcurie`
   with `values_from` pointing at the real ISO 19115 codelist — simpler than
   forcing a union, and the *only* shape the one real example actually uses,
   so there was no evidence the object form was ever needed in practice.
   Renamed `had_role` → `attribution_had_role` along the way: the bare name
   collided with `dcat-ap-plus`'s own pre-existing top-level `had_role` slot
   (`ValueError: Conflicting URIs for item: had_role`, hit by actually
   running it, not predicted).

Corrected real instance, converted end to end:

```turtle
[] a prov:Attribution ;
    dcat:hadRole <https://standards.iso.org/iso/19115/resources/Codelists/gml/CI_RoleCode.xml#processor> ;
    prov:agent [ a foaf:Agent ; foaf:name "Germany processor" ] .
```

Now a structural match to the real example (bare codelist URI, `foaf:Agent`
typing) rather than a plausible-looking approximation. `multivalued: true`/
`inlined_as_list: true` were restated explicitly on `HealthDataset`'s
`qualified_attribution` `slot_usage` override, applying the lesson already
learned in `HealthStudy-DCAT-AP` (a range-only override without restating
those breaks the generated `__post_init__` even when the values don't
actually change) — not rediscovered the hard way this time.

**Result: confirmed**, and now actually matching the one real example
available, not just structurally plausible. Worth remembering: a design
"already proven" in a sibling repo is proven against *that repo's* test
data, not automatically against the real spec — worth re-checking against
primary sources even when reusing a working pattern.

## 5. `qualified_association` (Activity-side, symmetric via `carried_out_by`/`prov:wasAssociatedWith`) — readiness

**Claim going in:** `dcat-ap-plus` has no `Association` class at all (only
built the Entity-side `Attribution` pattern, and even that only as a stub —
confirmed absent, not assumed, same grep-everything approach as the other
findings in this document). Open question: does building `Association`
belong in this merge layer, or is it specific enough to defer to the
specialization repo?

**`Association` itself belongs here** — the generic PROV-O completion, same
reasoning as `DatasetAttribution` (§4). Built in the main hand-authored
schema (not the port script's completion step, unlike `DatasetAttribution`
— `Association` has no dependency on anything the port generates):
`is_a: SupportiveEntity`, `class_uri: prov:Association`, `agent`
(`prov:agent` → `AgenticEntity` — correctly Activity-scoped here, unlike
`DatasetAttribution`'s Entity-scoped `attribution_agent`, per §4's
correction) and `association_had_role` (`prov:hadRole` → `uriorcurie`,
`values_from` the same ISO 19115 `CI_RoleCode` codelist — same fix as
`attribution_had_role` in §4, same reason: a bare URI is what
HealthDCAT-AP's real examples actually use, and a class-plus-scalar
`any_of` union doesn't reliably validate both shapes).

**A real gap caught by the user, not this document's own checks: the class
existed, but the mechanism connecting anything to it didn't.**
`qualified_association` — the slot that actually makes `Association`
reachable from an Activity — was never defined at all. The original framing
here ("narrowing `qualified_association` onto a specific class doesn't
belong in this merge layer") quietly slid into "so don't define the slot
either," which doesn't follow: the slot itself needs no class to attach
to — it's new, not an override of an existing `dcat-ap-plus` slot, so its
`range: Association` can be set directly at the top level, with zero
dependency on any Activity-side class existing yet. That's exactly the
"ready to use, only needs specializing" schema the downstream repo needs,
consistent with the user's own framing of what this merge layer is for.
Fixed:

```yaml
qualified_association:
  slot_uri: prov:qualifiedAssociation
  range: Association
  multivalued: true
  inlined_as_list: true
```

The specialization repo can now add `qualified_association` to any
`is_a: DataGeneratingActivity` class's own `slots:` list and get the
correct range immediately — no schema work needed there just to make the
mechanism usable, only to define what its own Activity-side class actually
looks like.

Real instance, converted end to end:

```turtle
<https://ror.org/00k4n6c32> a prov:Agent ;
    dcterms:title "Example Funding Agency" .

[] a prov:Association ;
    prov:agent <https://ror.org/00k4n6c32> ;
    prov:hadRole <https://standards.iso.org/iso/19115/resources/Codelists/gml/CI_RoleCode.xml#funder> .
```

**Result: confirmed**, and corrected on the actual scope question at the
time: not "defer everything Activity-related," but "defer only what
genuinely needs a class that doesn't exist yet." `Association` and
`qualified_association` were both fully usable already; only the class
that *references* `qualified_association` was left to the specialization
repo.

**That narrowest deferred piece was itself built here once a real need
appeared** — a request for a full worked example with `AgenticEntity`s on
`Activity`s (PI/sponsor/funder), the same kind of thing this whole
document keeps testing rather than assuming works.
`AssociatedDataGeneratingActivity` (`health_dcat_ap_plus.yaml`) is
`DataGeneratingActivity`, `is_a`, same `class_uri`, with
`qualified_association` added to its own `slots:` — exactly as generic and
health-agnostic as `Association` itself, so building it doesn't cross the
line that was actually meant (no health-specific content, just the one
slot that makes the already-generic mechanism reachable from a real
Activity). Couldn't be done by narrowing `HealthDataset.was_generated_by`'s
declared range directly onto it — `HealthDataset` lives in the generated
`healthdcat_ap_non_public.yaml`, which doesn't import this file (only the
reverse), and reopening an already-imported class's `slot_usage` throws
"Conflicting URIs" regardless of which file tries it (confirmed elsewhere
this session). Used directly instead:
`tests/test_shacl_validation.py`'s fixture-construction helper
pre-constructs each `was_generated_by` entry as a real
`AssociatedDataGeneratingActivity` instance before `HealthDataset(**data)`
runs — `_normalize_inlined_as_list`'s own `isinstance(list_entry,
slot_type)` fast path (confirmed by reading its source directly) accepts
an already-built subclass instance as-is, no schema-level range narrowing
needed at all.

Full worked example — `tests/data/problem/valid/HealthDataset-shacl-full.yaml`'s
`was_generated_by`, three real ISO 19115 `CI_RoleCode` roles (not
invented):

```turtle
<https://example.org/activity/cancer-registry-collection-2024> a prov:Activity ;
    dcterms:title "Cancer registry data collection process" ;
    prov:qualifiedAssociation
        [ a prov:Association ;
            prov:agent <https://orcid.org/0000-0002-1825-0097> ;
            prov:hadRole <https://standards.iso.org/iso/19115/resources/Codelists/gml/CI_RoleCode.xml#principalInvestigator> ],
        [ a prov:Association ;
            prov:agent <https://ror.org/00k4n6c32> ;
            prov:hadRole <https://standards.iso.org/iso/19115/resources/Codelists/gml/CI_RoleCode.xml#sponsor> ],
        [ a prov:Association ;
            prov:agent <https://ror.org/03yrm5c26> ;
            prov:hadRole <https://standards.iso.org/iso/19115/resources/Codelists/gml/CI_RoleCode.xml#funder> ] .

<https://orcid.org/0000-0002-1825-0097> a prov:Agent ;
    dcterms:title "Dr. Maria Santos" .
```

Checked against both shape sets in §6 as part of the same fixture, not
separately: zero new violations against either — our own generated SHACL
has no conflicting shape for `prov:Agent`/`prov:Association`/
`prov:qualifiedAssociation` (`Association`/`AgenticEntity` are
hand-authored, no base `dcat-ap-plus` class collides with them the way
`Dataset`'s own fields did in §6), and HealthDCAT-AP's real shapes
genuinely never reach the Activity side at all (the same finding already
confirmed in §1 Check b) — so real Activity-side content adds nothing new
to validate against there either.

## 6. Real SHACL validation — does a real instance actually conform?

Everything above verifies the *schema*: shapes of classes and slots, checked
via `SchemaView` introspection and `linkml-validate`'s JSON-schema-derived
checks. None of that can see what real SHACL enforces —
`sh:nodeKind`/IRI-vs-literal, `sh:class` membership, `sh:hasValue`,
cardinality nested inside sub-shapes. `tests/test_shacl_validation.py`
closes that gap: it builds a comprehensive `HealthDataset` instance (a
cancer registry dataset with agents, activities, entities, attribution,
and qualified associations (PI/sponsor/funder, §5) —
[tests/data/problem/valid/HealthDataset-shacl-full.yaml](https://github.com/portail-fresh/Health-DCAT-AP-plus/blob/main/tests/data/problem/valid/HealthDataset-shacl-full.yaml)),
dumps it to real RDF via `rdflib_dumper.as_rdf_graph`, and runs `pyshacl`
against it twice: once against our own generated SHACL, once against
HealthDCAT-AP's real, official upstream `.ttl` shapes directly (cloned
locally at `repos/healthdcat-ap`, per README.md) — two independent
questions ("is our merge self-consistent?" and "does the dataset portion
still conform to the spec it was ported from?").

Both runs produce real violations. Rather than requiring conformance
outright, the tests compare the exact set of violation *signatures*
(severity, SHACL constraint component, result path) against an explicit,
commented allowlist in the test file — a genuinely new violation fails the
test (a real regression), and so does fixing a known one (a prompt to
prune the allowlist), so the allowlist stays an accurate, living record of
what's actually still broken. Two real, structural port bugs came out of
the first run, not visible to any check above — **both now fixed and
verified** (the real-shapes violation count dropped from 31 to 20; every
`NodeKind`, `sh:hasValue`, and `contactPoint` finding below is confirmed
gone from the allowlist):

- **Vocabulary-bound slots kept class-object ranges.** Every
  `values_from`-bound slot this repo ported (`theme`, `health_category`,
  `health_theme`, `access_rights`, `frequency`, `has_coding_system`,
  `language`, `type`, `conforms_to`) ranged over a nested class (`Concept`,
  `RightsStatement`, `Frequency`, `Standard`, ...) inherited from
  `dcat-ap-plus` or added by the port, instead of the bare IRI the real
  shapes require (`sh:nodeKind sh:IRI`, confirmed directly in
  `non-public-shapes.ttl`/`mdr-vocabularies.shape.ttl` — 25 of 27
  vocabulary-bound property shapes there carry it; the 2 real exceptions,
  `dct:publisher` and `prov:wasGeneratedBy`, correctly stay nested/inlined
  objects and were confirmed *not* touched by the fix). Same lesson as
  `attribution_had_role` in §4, except it turns out that fix should have
  generalized to every vocabulary-bound field, not just that one —
  `values_from` correctly recorded *which* vocabulary to point to, but
  never corrected the range to match. **Fixed** in
  `parse_vocabulary_restrictions`/`main()` (the port script): every
  vocabulary binding whose source property shape also carries
  `sh:nodeKind sh:IRI` now forces `range: uriorcurie` in the generated
  `slot_usage`. Two sharper instances of the same family, also now
  resolvable since the range supports a plain IRI: `dct:accessRights`
  requires `sh:hasValue <.../access-right/NON_PUBLIC>` exactly (the test
  fixture now supplies it directly), and `dcat:theme` must include the
  fixed `.../data-theme/HEAL` term specifically (ditto).
- **`HealthAgent`/`HealthPublisherAgent` reused the wrong contact-point
  predicate.** `hdab`/`custodian`/`publisher` reused `dcat-ap-plus`'s own
  `contact_point` slot, hardwired to `dcat:contactPoint` (confirmed via
  `SchemaView.induced_slot`) — root cause: `cv:contactPoint`'s local name
  snake-cases to the exact same `contact_point`, and `build_linkml`'s
  classless slot-lookup fallback (needed because `HealthAgent` isn't a real
  `dcat-ap-plus` class) matched that name to the wrong, unrelated slot. The
  real `HealthAgent_Shape` requires `cv:contactPoint`
  (`http://data.europa.eu/m8g/` Core Vocabulary predicate) instead — a
  different predicate for Agent-typed contact points than for
  Dataset/Distribution's own. Same class of issue as the
  `attribution_had_role` rename in §4: a `dcat-ap-plus` slot reused where
  it doesn't actually apply. **Fixed** via a `PROPERTY_RENAME` map (same
  pattern as `CLASS_RENAME`) — `cv:contactPoint` now resolves to its own
  `agent_contact_point` slot, correctly `slot_uri: cv:contactPoint`.

Regenerating after both fixes surfaced one new, deeper finding — visible
only against our own generated shapes, not the real ones: `HealthDataset`
shares `dcat:Dataset`'s own `class_uri` with `dcat-ap-plus`'s unmodified
base `Dataset` class (the whole point of the "`Health<X>` profile"
pattern — same real-world type, tighter shape). Confirmed directly by
querying our generated SHACL: `sh:targetClass dcat:Dataset` now carries
*two* `sh:property` shapes for `dct:accessRights` (and
`accrualPeriodicity`/`language`/`theme`/`type`) — `dcat-ap-plus`'s own
original `RightsStatement`-classed one, untouched, plus `HealthDataset`'s
new `uriorcurie`/`nodeKind`-IRI one — and a bare IRI can't satisfy both at
once. Every earlier profile narrowing (e.g. `contact_point` →
`HealthKind`) was a subclass tightening, compatible with the base shape;
this is the first one where the override is a genuinely different,
mutually exclusive value shape (object vs. scalar) on the *same*
`class_uri`, which "layer a stricter shape on top" can't reconcile by
itself.

**Investigated further, not treated as a one-off.** Querying every
`(sh:targetClass, sh:path)` pair in our generated SHACL for more than one
disagreeing value-shape combination turns up 26 such conflicts — 17 of
them freshly caused by the vocab-range fix, spanning five classes, not
just `HealthDataset`: `Catalog/language`, `Catalog/publisher`,
`Catalog/spatial`, `DataService/accessRights`, `DataService/format`,
`Dataset/accessRights`, `Dataset/accrualPeriodicity`, `Dataset/conformsTo`,
`Dataset/language`, `Dataset/spatial`, `Dataset/type`, `Dataset/theme`,
`Distribution/availability`, `Distribution/format`,
`Distribution/language`, `Distribution/status`. So this isn't a one-off:
it will recur every time a future `Health<X>` tightening swaps a value's
shape (object → scalar) rather than just narrowing it — and that's exactly
the pattern HealthDCAT-AP's real spec uses for essentially every
controlled-vocabulary field.

The important question was *why* — is `dcat-ap-plus` wrong to model these
as nested objects, or is this real, and if real, does it mean our own
generated SHACL should be made clean? Checked directly, not assumed:
`dcat-ap-plus`'s own schema gives `Dataset.access_rights` `range:
RightsStatement` and `Dataset.frequency` `range: Frequency` with no
rationale comment either way — this is `dcat-ap-plus` faithfully
reflecting *plain DCAT-AP's own* standard convention (DCAT-AP itself
genuinely models `dct:accessRights`/`dct:accrualPeriodicity` as objects).
HealthDCAT-AP's real spec then requires bare IRIs for the same predicates
— a real divergence between the two specs, not a mistake either one made.
And critically: HealthDCAT-AP's own real, official validation set
(`non-public-shapes.ttl` etc., exactly what §6's real-shapes test
validates against) is never combined with plain DCAT-AP's own generic
`shapes.ttl` in practice — the real-shapes test is already clean, and
stays clean regardless of this finding. The conflict exists *only* in our
own self-generated SHACL, the one place that naively unions
`dcat-ap-plus`'s base `Dataset` shape with `HealthDataset`'s override —
something the real validation ecosystem never actually does either.

Given that, the options considered:

1. **Give `Health<X>` its own `class_uri`.** Rejected — HealthDCAT-AP's
   real `Dataset_Shape` targets plain `dcat:Dataset`, not a health-specific
   subtype (confirmed directly in `non-public-shapes.ttl`). A different
   `class_uri` would make our own output non-conformant to the actual
   spec — strictly worse than the cosmetic self-SHACL noise it would fix.
2. **Drop `is_a: Dataset`, keep the same `class_uri`.** Doesn't help —
   `Dataset` stays present in the compiled schema regardless (imported,
   referenced elsewhere), so `linkml generate shacl` still emits its shape
   independently. Checked directly, changes nothing.
3. **Custom SHACL generation that resolves one shape per real `class_uri`**
   (most-specific class wins). Buildable, but not more *correct* — real
   SHACL has no override semantics, so a resolved single-shape output
   wouldn't reflect what an actual SHACL processor does if it received
   both shape sources together. It would just be us inventing our own
   resolution rule to make a self-test quieter.
4. **Stop expecting our self-generated SHACL to be globally clean; let it
   be a self-consistency smell test, and treat the real-shapes test as the
   authoritative signal.** Matches what the real ecosystem already does
   (HealthDCAT-AP's own shapes are self-sufficient, never stacked with
   plain DCAT-AP's), costs nothing to implement, and is already backed by
   a passing test.

**Chosen: option 4.** This isn't a bug to fix — it's a correctly-surfaced
structural fact about how HealthDCAT-AP relates to DCAT-AP, and the
authoritative check (the real-shapes test) already reflects it correctly.
`KNOWN_OWN_SHAPES_VIOLATIONS` stays the honest, permanent record of it
rather than papering over it with an invented resolution rule.

**A third real, structural port bug, found the same way**:
`HealthAgent`/`HealthPublisherAgent` (case 2 in the port script's own
docstring — a synthetic class with no `sh:targetClass` match) never got a
`class_uri` at all. Root cause: `:HealthAgent_Shape` in the real shapes has
no `sh:targetClass` of its own — only `sh:extends :Agent_Shape` — so it's a
pure value-shape, reused via `sh:node` from `hdab`/`custodian`/`publisher`,
not an independently-targeted RDF type. The port correctly resolved
`is_a: Agent` from the `sh:extends`, but `class_uri` was only ever set from
`sh:targetClass`, which is absent here — so `HealthAgent` silently fell
back to LinkML's own auto-generated `class_uri`
(`health_dcat_ap_plus:HealthAgent`) instead of inheriting `foaf:Agent` from
its parent, the same "profile, same `class_uri` as base" pattern used
everywhere else in this port. Real instances of `hdab`/`custodian` never
actually typed as `foaf:Agent` at all — confirmed via real SHACL validation
(`HealthAgent_Shape` requires it; the dumped RDF never provided it, and
`ClassConstraintComponent "hdab"` was in `KNOWN_REAL_SHAPES_VIOLATIONS`).
**Fixed**: `build_linkml` now falls back to the resolved parent's own
`class_uri` when a class has an `is_a` (via `sh:extends`) but no
`sh:targetClass` of its own. Verified: the `hdab` finding is gone from the
real-shapes test.

Fixing it introduced one expected instance of the *same* class_uri-sharing
fact from above, this time in our own shapes: `HealthAgent`/
`HealthPublisherAgent` now correctly share `class_uri: foaf:Agent` with
`dcat-ap-plus`'s own base `Agent` — which is what makes a real `hdab`/
`custodian` value actually type as `foaf:Agent`, as it should — but that
also means `Agent`'s merged `foaf:Agent` shape now carries
`HealthAgent`'s required `agent_contact_point` constraint too, which bleeds
onto *every* `foaf:Agent`-typed node in the graph, including
`DatasetAttribution.attribution_agent`'s plain `Agent` value (§4), which
has nothing to do with `HealthAgent` and shouldn't need a contact point.
Tracked as `MinCountConstraintComponent "contactPoint"` in
`KNOWN_OWN_SHAPES_VIOLATIONS` — the same accepted limitation as everything
else in that section, not a new category of problem.

**Two more findings from the same investigation, both fully diagnosed as
non-bugs** (not schema or port issues, and not fixed, since there's nothing
to fix):

- The `MinCountConstraintComponent "value"` finding on `is_about_entity`
  isn't about `EvaluatedEntity` at all — confirmed directly: neither
  `EvaluatedEntity` nor `Entity` declares a `value` slot. `dcat-ap-plus`'s
  own `QualitativeAttribute` class does (`required: true`), and shares the
  exact same `class_uri: prov:Entity` with `Entity`/`EvaluatedEntity`/
  `AnalysisSourceData` (four distinct `dcat-ap-plus` classes, confirmed by
  grep) — the same class_uri-sharing mechanism as everything above, except
  this instance is entirely internal to `dcat-ap-plus`'s own base schema,
  with nothing to do with HealthDCAT-AP or this port at all.
- The whole `DatatypeConstraintComponent` cluster in
  `KNOWN_OWN_SHAPES_VIOLATIONS` (title/description/... and separately
  startDate/maxTypicalAge/...) is diagnosed too, in two unrelated causes,
  neither a schema bug: (a) `rdflib.Literal("x") != rdflib.Literal("x",
  datatype=XSD.string)` in rdflib itself, confirmed directly — `.datatype`
  is `None` vs. explicit — so `rdflib_dumper`'s plain-string output never
  satisfies `sh:datatype xsd:string` even though RDF 1.1 says an untyped
  literal *is* an `xsd:string`; and (b), for fields that already carry the
  exactly-correct explicit datatype and still fail (`maxTypicalAge` etc.):
  `linkml generate shacl` numbers `sh:order` per source class, restarting
  at 1 for `HealthDataset`'s own additions, and once merged onto the same
  `dcat:Dataset` shape subject (the class_uri-sharing fact again),
  `sh:order` values collide across unrelated properties — confirmed
  directly, `dcat:landingPage` and `healthdcatap:maxTypicalAge` both carry
  `sh:order 15` on the merged shape — and `pyshacl` visibly mishandles the
  collision. Reproduced in a self-contained, 948-triple extract of just
  `dcat:Dataset`'s own shape closure, independent of the rest of the
  schema, ruling out any other cause.

**A fourth and fifth real, structural port bug**, both fixed the same way,
found while building out a fuller test fixture:

- **The `dcterms:relation`/`dcterms:source`/`dcterms:conformsTo` predicate
  collision, now fixed.** `dcat-ap-plus` reuses each of these predicate
  URIs across several of its own slots (`dcterms:relation` alone maps to
  `has_qualitative_attribute` / `has_quantitative_attribute` /
  `related_resource` / `relation`), and the port script's URI→slot-name
  resolution (a single classless dict, one slot name remembered per URI)
  could only pick one, arbitrarily. `property_name_for` now resolves
  against the *current shape's own class* first — checked directly, all
  three URIs resolve unambiguously against `Dataset`'s own induced slots
  (`related_resource`, `source`, `conforms_to` respectively) — falling
  back to the classless dict only when the class doesn't resolve it either
  (a genuinely new HealthDCAT-AP class with no `dcat-ap-plus` counterpart).
  `HealthDataset.relation`/`source_metadata` are renamed to
  `related_resource`/`source` accordingly (the fixture and
  `tests/test_shacl_validation.py` updated to match); `linked_schemas` is
  renamed to `conforms_to`, correctly picking up the vocab-range fix along
  the way (it's one of the `values_from`-bound fields from §6's first
  fix).
- **`sh:severity sh:Warning` cardinality getting promoted to a hard LinkML
  `required`, now fixed.** Found chasing why `source`'s newly-correct
  resolution left it `required: true` despite `dct:source` not appearing
  anywhere in HealthDCAT-AP's *required*-tier files at all — it turned out
  to live only in `non-public-shapes_recommended.ttl`, `sh:severity
  sh:Warning`. `parse_shapes` never tracked `sh:severity` at all (only the
  separate `mdr-vocabularies.shape.ttl` parser did, for its own
  `recommended_only` comments) — every `sh:minCount` from the
  `*_recommended.ttl` files was mechanically promoted into a hard
  `required`, regardless of severity. Confirmed with real numbers, not
  assumed: `HealthDataset`'s own required-field count dropped from ~30 to
  16 once fixed (`access_rights`, `applicable_legislation`, `contact_point`,
  `dataset_distribution`, `description`, `has_structured_data`, `hdab`,
  `health_category`, `id`, `identifier`, `keyword`, `provenance`, `theme`,
  `title`, `type`, `was_generated_by`) — spot-checked several of the
  now-optional ones directly against both real shape files (`dct:source`,
  `dpv:hasPurpose`, `healthdcatap:minTypicalAge`, `healthdcatap:analytics`)
  to confirm each really is `sh:Warning`-only, not a fix that silently
  loosened something genuinely required.

One genuine bug in HealthDCAT-AP's own upstream shapes, not ours: in
`non-public-shapes.ttl`, `Dataset_Shape`'s conditional constraint ("if
`hasStructuredData` is true, must have `hasVariables`") is a bare `sh:or`
used directly as an `sh:property` value with no `sh:path` — not a
well-formed SHACL PropertyShape, which makes strict processors (`pyshacl`
included, in `advanced` mode) reject the whole file. The test works around
it (drops just that triple, asserting there's exactly one such offender so
a future upstream change would be caught) rather than fixing it — not our
file to fix. Worth raising with Mohamed Chouaiech (the file's listed
author) alongside the already-known `dcatap:` prefix typo (missing trailing
slash in `deprecateduris.ttl`/`range.ttl`/`mdr-vocabularies.shape.ttl`,
confirmed fixed in the vendored `HealthDCAT-AP_validator` copies of the
same files but not the top-level release ones), whenever that conversation
happens.

The rest of the allowlisted violations are either already-known separate
bugs reconfirmed independently (`vcard:hasEmail` must be an IRI, not a
string literal — same finding as §1 Check c, now caught by real shapes too;
the `temporal_resolution` list-repr-into-literal bug, same class as the
`frequency` multivalued-narrowing crash worked around in the test's own
fixture-construction helper) or test-fixture artifacts, not schema bugs
(the DPV/DQV `sh:class` membership checks need the real ontologies loaded
for reasoning, which this fixture doesn't attempt; most of the
`skos:inScheme` "non-EU managed concept" warnings are exactly what real
vocabulary term IRIs would resolve, expected to mostly disappear once the
vocab-range bug above is fixed and the fixture switches from fabricated
`skos:Concept` blank nodes to real term IRIs).

**Result: five real, structural port bugs found that no prior check in
this document could see — all five fixed and verified (real-shapes
violations: 31 → 20 → 19 → 20, the last uptick a single benign, expected
`sh:Warning` finding, not a regression) — plus two findings fully
diagnosed as non-bugs (one entirely internal to `dcat-ap-plus`'s own base
schema, one a two-cause rdflib/pyshacl tooling nuance), one confirmed
upstream bug (not ours), and one settled architectural question, all
formalized as a permanent regression test** (`just test` runs it; the
upstream-shapes half skips gracefully if `repos/healthdcat-ap` isn't
cloned locally) so future port-script or schema changes get checked
against real SHACL automatically instead of ad hoc.

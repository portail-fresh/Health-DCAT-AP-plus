# Roadmap

A living planning document across both repos in this effort —
**Health-DCAT-AP-plus** (the merge layer: HealthDCAT-AP's ported SHACL +
dcat-ap-plus) and **[ResHealth-DCAT-AP](https://github.com/portail-fresh/ResHealth-DCAT-AP)**
(the specialization layer on top: research-study/role modeling). For the
detailed, evidence-by-evidence technical narrative behind any of this, see
[`docs/architecture-verification.md`](docs/architecture-verification.md) —
this file is deliberately the higher-level "what, why, what's next," not a
repeat of that forensic record.

## What's done

- **The merge layer itself.** HealthDCAT-AP's non-public-tier SHACL
  mechanically ported to LinkML (`scripts/port_healthdcat_ap_shacl_to_linkml.py`)
  and merged with dcat-ap-plus, following the "`Health<X>` profile" pattern
  throughout (same `class_uri` as the dcat-ap-plus base class, tighter
  shape) — matching the same method NFDI4Chem used for chem-dcat-ap.
- **Published, with a real w3id permalink** ([perma-id/w3id.org#6598](https://github.com/perma-id/w3id.org/pull/6598),
  merged) — `https://w3id.org/portail-fresh/Health-DCAT-AP-plus/`.
- **Layered SHACL validation, in both repos**: three genuinely different
  checks (own generated shapes, HealthDCAT-AP's real official shapes, and
  one merged production shapes graph combining both without conflicts),
  each a permanent regression test with an explicit, individually-diagnosed
  allowlist. See `docs/architecture-verification.md` §6–7 for the full
  story, including several real, structural bugs found and fixed this way
  that no earlier check could see.
- **Cross-checked against the real world, not just our own tooling**:
  Sciensano's official hosted HealthDCAT-AP validator, and HealthDCAT-AP's
  own official worked example (now vendored at
  `examples/reference/example-healthdcat-dataset.ttl`) — both used to find
  and fix genuine bugs (invented vocabulary codes, `dct:source`'s eager
  nested construction, `hasQualityAnnotation`'s missing `inlined_as_list`),
  not just to feel reassured. `KNOWN_REAL_SHAPES_VIOLATIONS` is now
  **empty** — the `HealthDataset` portion fully conforms to HealthDCAT-AP's
  real, official upstream SHACL shapes, in both repos.
- **`association_had_role`'s `values_from` moved down to the specializing
  repo** (ResHealth-DCAT-AP's own `ResearchAssociation`, narrowing
  `ResearchStudy`'s `qualified_association` range) — Health-DCAT-AP-plus's
  own copy of `Association` now stays genuinely open, matching dcat-ap-plus's
  own stated intent for the upstream proposal and validating the design
  ahead of that proposal landing.
- **ResHealth-DCAT-AP**: `ResearchStudy`/`InterventionalStudy`/
  `ObservationalStudy` built on top, using dcat-ap-plus's existing
  `Association`-completion pattern (`qualified_association`, PI/sponsor/
  funder roles via real ISO 19115 `CI_RoleCode` values). Confirmed
  empirically that its own new classes introduce zero new violations
  against any of the three shapes graphs.
- **An upstream proposal drafted, posted and approved in principle** in
  dcat-ap-plus's own GitHub Discussion
  ([#109](https://github.com/nfdi-de/dcat-ap-plus/discussions/109)): bring the
  generic PROV-O `Association`/`qualified_association` pattern upstream (it's
  not health-specific). Three maintainers have answered (2026-08-19 to
  2026-10-14): StroemPhi found it reasonable, with no conflict; HendrikBorgelt
  gave the go-ahead on 2026-10-13 (the others will mostly stay silent, so no
  further approval is needed); and dalito, on 2026-10-14, called it "a real gap"
  and "a candidate for being added to DCAT-AP+", with concrete changes for the
  pull request (see "Problems that still need fixing"). Nothing is blocked on
  them any more: the next move is ours.
- **The `ClassifierMixin`/`rdf_type` finding, posted to dcat-ap-plus as
  [#110](https://github.com/nfdi-de/dcat-ap-plus/issues/110), traced one
  level further up to LinkML itself and filed as
  [linkml/linkml#3931](https://github.com/linkml/linkml/issues/3931).**
  Maintainer StroemPhi confirmed the bug independently and proposed a
  `sh:or`-union fix direction; LinkML maintainer matentzn asked for it to
  be filed on LinkML's own tracker instead, since it's a `ShaclGenerator`
  bug, not a dcat-ap-plus one. Reproduced again with a genuinely minimal,
  dcat-ap-plus-independent schema (two classes, one slot) at
  `examples/issues_for_linkml/` — confirms it's a real LinkML bug, not
  something specific to dcat-ap-plus's own mixin design. **Filed, waiting
  on maintainer response** (see "Blocked" below).
- **The `value`/`QualitativeAttribute` finding, filed directly as
  [linkml/linkml#3932](https://github.com/linkml/linkml/issues/3932)**
  (no separate dcat-ap-plus issue — see "Blocked" below for why). Same
  underlying mechanism as
  [linkml/linkml#3011](https://github.com/linkml/linkml/issues/3011)
  ("Unintentional SHACL Class merge," closed, partially fixed by
  [#3020](https://github.com/linkml/linkml/pull/3020)), but demonstrates a
  functional consequence (a `required` slot's `sh:minCount` bleeding onto
  every other class sharing its `class_uri`, breaking otherwise-valid
  data) rather than #3011's cosmetic one (`sh:description` duplication).
  Reproduced standalone at
  `examples/issues_for_linkml/class-uri-cardinality-bleed.ipynb`. **Filed,
  waiting on maintainer response.**
- **`title`'s violation, fixed for real — it was never an `rdflib`/`pyshacl`
  quirk.** Prompted by directly asking "is this third violation also worth
  reporting upstream?" instead of trusting the standing diagnosis:
  re-verified from scratch, found the standing diagnosis was wrong (a
  synthetic reproduction of the exact same shape conformed cleanly),
  and traced the real cause by querying the actual failing shape's own
  `sh:datatype` term directly — it was the *unexpanded CURIE string*
  `"xsd:string"` used as a literal 10-character `URIRef`, not the real
  39-character `http://www.w3.org/2001/XMLSchema#string`. Root cause: this
  schema's own `prefixes:` block already works around a known LinkML
  `gen-shacl`/`gen-owl` bug (imported schemas' own prefixes don't
  propagate into generated Turtle) by manually redeclaring every prefix it
  needs — `xsd:` was simply missing from that list, the one prefix nobody
  thought to check because it's assumed to always be there. Fixed by
  adding `xsd:` to `health_dcat_ap_plus.yaml`'s `prefixes:` block and the
  port script's own `PREFIXES` dict. This single fix cleared 17 allowlist
  entries at once, not just `title` — every plain-string/date/boolean-typed
  slot had the same malformed `sh:datatype`, previously attributed to two
  separate, both-wrong theories (an rdflib literal-typing quirk for one
  group, an `sh:order`-collision theory for another). See
  `docs/architecture-verification.md`'s "A tenth finding" section for the
  full misdiagnosis-then-correction narrative.
  `KNOWN_OWN_SHAPES_VIOLATIONS` is now 14 (was 30);
  `KNOWN_MERGED_SHAPES_VIOLATIONS` is now 2 (`type`, `value` — see above).
- **The genuinely generic pieces extracted into a real, installable
  package**: [linkml-merge-toolkit](https://github.com/portail-fresh/linkml-merge-toolkit)
  (`post_init_shielding`'s shield-map computation, `shacl_merge`'s
  base+profile shape-filtering logic) — first package the user has ever
  published, done step by step: new repo, `pyproject.toml`/`LICENSE`/
  `README`, a standalone test suite with its own minimal fixtures (zero
  dependency on this repo), CI, then both existing repos wired to depend
  on it via `git+https://...` (not published to PyPI — a deliberate
  choice, see the package's own commit history) instead of reaching
  directly into `scripts/`. `scripts/patch_post_init_shielding.py` is
  gone entirely (replaced by the package's own `patch-post-init-shielding`
  console script); `scripts/gen_merged_shacl.py` keeps only what's
  genuinely project-specific (which files to load, `EXTERNAL_VOCABULARY_STUB_CLASSES`,
  `foaf:Agent`) and imports the generic filtering logic. Regenerated
  everything afterward and confirmed byte-for-byte equivalent output
  (module-level diffs only: a generation timestamp, and the `xsd:` prefix
  the previous fix added but hadn't been regenerated through yet) — the
  extraction changed where the code lives, not what it does.
- **Brought up to date with LinkML 1.12.1 and dcat-ap-plus v0.1.0rc5**
  (2026-10-16). rc5 is semantically identical to rc4 but renamed its own
  prefix `dcatapplus` → `dcatap_plus`; under LinkML 1.12 that turned the
  prefix-propagation gap from 2b below from *silent* into *fatal*:
  `ShaclGenerator.serialize()` now canonicalises through pyoxigraph, which
  rejects the unexpanded `dcatap_plus:…` IRIs (an underscore isn't legal in a
  URI scheme), and the rdflib fallback it drops to did not finish on this
  graph — `gen-project`, `gen-shacl` and the SHACL tests simply hung. Fixed by
  renaming the prefix and import and redeclaring the four other prefixes
  dcat-ap-plus's own URIs use (`qudt:`, `schema:`, `rdfs:`, `eli:`), which had
  been producing eight silently wrong IRIs. One real bug fell out of it:
  `gen_merged_shacl.py`'s exclusion of `schema:DefinedTerm` never matched (it
  names the real IRI; our shape carried the unexpanded one), so a shape the
  merge is meant to drop shipped anyway. A permanent guard
  (`test_*_has_no_unexpanded_iris`, run first by `just test`) now turns a
  repeat into an immediate, readable failure instead of a hang. Allowlists
  unchanged (own 14, merged 2, real 0); dependency floors raised to
  `linkml>=1.12.1`; `docs/schema/` regenerated (it was last refreshed
  2026-08-25, five source commits ago). Also corrected: the `subject`
  allowlist entry is the shared-`slot_uri` bug, not a DPV/DQV artifact. Full
  narrative: `docs/architecture-verification.md`, "An eleventh finding".
- **The w3id permalink now serves a schema that other schemas can import**
  (2026-10-19). `…/latest/schema/health_dcat_ap_plus.yaml` had been serving
  `gen-yaml`'s *merged* output — all 51 dcat-ap-plus classes copied in, the
  same `imports:` still listed — so anything importing it defined each of
  them twice, and LinkML's legacy loader (`PythonGenerator`, `gen-yaml`,
  `gen-project`) refused with "Conflicting URIs". That is the error that had
  been blamed on "2+ levels of stacked CURIE imports", and the reason
  ResHealth-DCAT-AP needed a local importmap. `scripts/publish_schema.py`
  (run by `just gen-doc`, so by the Deploy docs workflow) now publishes the
  *source* root schema instead, with its sibling import written as an
  absolute URL, and keeps the merged output next to it as
  `health_dcat_ap_plus.merged.yaml` under a banner saying not to import it.
  Verified end to end, not assumed: against the real address,
  ResHealth-DCAT-AP generates Python, `gen-yaml`, Pydantic, SHACL, OWL, JSON
  Schema and the JSON-LD context with no importmap at all, with output
  identical to what the importmap route gave; both repos' CI is green on
  Linux (Python 3.10–3.14). ResHealth-DCAT-AP then **deleted its importmap
  altogether**: its generation, its whole test suite (SHACL layers included)
  and its docs build now run through the published schema, and its docs
  workflows no longer clone this repo. `tests/test_published_schema.py` here
  and ResHealth-DCAT-AP's `check_schema_resolves.py` keep it that way. Full
  narrative: `docs/architecture-verification.md`, "A twelfth finding".
- **Moved from HealthDCAT-AP release 7 to release 8** (2026-10-21; release 7
  is deprecated upstream, release 8 is commit `cd7841f` of 2026-09-18). The
  port now reads release 8's folder layout, the clone is pinned by commit in
  CI and checked against the generated schema's header, and the fixture,
  the vendored official example and the vocabulary URLs follow the release
  (the six controlled vocabularies moved from the acceptance to the
  production host). New in the schema: `hdab_coordinator`, a mandatory
  `title` on the CSVW table group, one `column_name` per column,
  `column_title` (was `titles`). The move also exposed three slots that had
  silently been ported onto the wrong predicate since release 7 (a CSVW
  column's name and title, an opening-hours `cv:frequency`), because their
  local names equal dcat-ap-plus slots; the port script now stops when that
  happens, and the fixture populates both so the official shapes check them.
  Full narrative: `docs/architecture-verification.md`, "A thirteenth
  finding". Not part of this step, deliberately: how the official shapes are
  merged with ours (still the per-class selection the audit of 2026-10-21
  questioned).

- **The merged shapes now check what the official validator checks**
  (2026-10-21, after an audit that found they did not). They were the five
  HealthDCAT-AP files plus our own shapes for the classes those files don't
  target; the validator also loads the DCAT-AP 3.0.0 shapes the files
  `owl:import`. `gen_merged_shacl.py` now follows those imports through the
  validator's own `owlImportMapping`, generates our shapes open instead of
  closed, derives the classes to leave to the official shapes instead of
  listing `foaf:Agent` and `skos:Concept` by hand, applies the two LinkML
  workarounds above and lets a `prov:Activity`'s `dct:type` be a `skos:Concept`
  as HealthDCAT-AP's own example has it, and writes the file with
  deterministic blank nodes. HealthDCAT-AP's own example now has to give the
  same result against the official and the merged shapes (three warnings, no
  violation), the published example and the fixture validate with warnings
  only, and the fixture's `dct:source` is a described dataset because DCAT-AP's
  shape wants one. Not part of the merge, on purpose: `graph-guard.ttl`.
  ResHealth-DCAT-AP uses the same function. Narrative:
  `docs/architecture-verification.md`, "A fourteenth finding".

## Problems that still need fixing

- **The `Association`/`qualified_association` pull request to dcat-ap-plus is
  ours to open** (go-ahead 2026-10-13; not started). What the maintainers asked
  for, and how it differs from what is built here. dalito (2026-10-14) suggests:
  the role as a node, `ActivityRole` with `class_uri: prov:Role` and
  `ClassifierMixin` (the name `Role` is taken by DCAT-AP's `dcat:Role`), so that
  SKOS profiles write `{id: <CI_RoleCode IRI>}` and OWL/BFO profiles such as
  ChemDCAT-AP type the same node; `Attribution` kept as DCAT-AP defines it;
  constraints in `slot_usage` (a global `agent` slot ranged `AgenticEntity`
  clashes with the `Agent` range of `Attribution`), with agents referenced
  rather than inlined; the role recommended, not required; and
  `qualified_association` on `Activity`/`Association` in `domain_agnostic_core`,
  which would make `AssociatedDataGeneratingActivity` unnecessary. Here the role
  is a bare `uriorcurie` with `values_from` (ISO 19115 `CI_RoleCode`, bound in
  ResHealth-DCAT-AP's `ResearchAssociation`), `Association` lives in this repo's
  own schema and `AssociatedDataGeneratingActivity` carries the slot, so
  following the suggestions changes both repos. StroemPhi also wants the PROV-O
  and BFO role patterns compared before the pattern spreads (the paper
  doi:10.1038/s41597-025-04580-1), and is open to alternatives to `values_from`
  for controlled values (LinkML's binding feature is, in his words, still not
  really implemented).
- **Two LinkML bugs are worked around in the merged shapes, not fixed.**
  `scripts/gen_merged_shacl.py`'s `GENERATOR_WORKAROUNDS` drop the
  `ClassifierMixin`/`rdf_type` property shapes
  ([linkml/linkml#3931](https://github.com/linkml/linkml/issues/3931)) and the
  required `prov:value` that `QualitativeAttribute` puts on every `prov:Entity`
  through a shared `class_uri`
  ([linkml/linkml#3932](https://github.com/linkml/linkml/issues/3932)). Each
  workaround raises when it finds nothing left to change, so a fix upstream
  shows up as a failing build that says what to delete. The merged-shapes
  allowlist is empty since 2026-10-21 (it had 2 entries, `type` and `value`,
  which these two workarounds now remove); `KNOWN_OWN_SHAPES_VIOLATIONS` (our
  generated shapes alone) keeps the five that show the same bugs and the
  class_uri/slot_uri sharing behind them.
- **HealthDCAT-AP itself is still moving** (open upstream issues, read on
  2026-10-21 at https://code.europa.eu/healthdataeu/healthdcat-ap/-/issues).
  What each would change here: #43 (the shape without `sh:path`; our loader
  keeps it as a node shape until it is fixed), #51 (a permanent namespace for
  `healthdcatap:`, a breaking change for every slot URI of the ported
  schema), #55 / #56 / #4 / #31 (CSVW: a `csvw:TableSchema` level between table
  and column, the range of `csvw:url` / `csvw:propertyUrl`, mandatory table
  name; the ported `Table`/`Column` classes would follow), #37
  (`trustedDataHolder` may come back), #53 (`dct:type` on `prov:Activity` is
  used by shapes and example but not documented), #50 (the shapes import
  DCAT-AP 3.0.0, not 3.0.1). One discrepancy found while moving to release 8
  is not reported yet: its `dpv:hasPersonalData` rule and example use
  `https://w3id.org/dpv/dpv-pd#…`, while DPV 2.3 defines its personal-data
  categories under `https://w3id.org/dpv/pd#…` (see the fixture's comment);
  a candidate issue for the HealthDCAT-AP tracker, not filed.
- **`public`/`restricted` HealthDCAT-AP tiers are unported.** Only
  `non-public` exists today. The port script's own README says the other
  two "should port the same way" — never actually run.
- **The sibling-checkout dependency pattern is a real, known limitation**
  for the *remaining* case (cloning `repos/healthdcat-ap` for real-shapes/
  vocabulary testing) — see "Future improvements" below. The `scripts/`
  half of this same problem is fixed (see "What's done" above); not
  urgent, but the sibling-clone half is still what's standing between
  "works for us" and "ready for someone else to copy."

## Blocked, waiting on external input

- **[linkml/linkml#3931](https://github.com/linkml/linkml/issues/3931)**
  (the `ClassifierMixin`/`rdf_type` finding) and
  **[linkml/linkml#3932](https://github.com/linkml/linkml/issues/3932)**
  (the `value`/`QualitativeAttribute` finding): both filed, both waiting
  on maintainer response. The workarounds for them in
  `scripts/gen_merged_shacl.py` stay until either gets fixed upstream.
  #3932 also still references closed issue
  [nfdi-de/dcat-ap-plus#15](https://github.com/nfdi-de/dcat-ap-plus/issues/15)
  and the design-patterns.md "three distinct node shapes" claim, which is
  empirically inaccurate (shapes get merged by `class_uri`, not kept
  distinct) — background only, not part of the issue text itself.
- **[linkml/linkml#3933](https://github.com/linkml/linkml/issues/3933)**
  (the `SchemaView.namespaces()` `@lru_cache` staleness finding): filed,
  with cross-link comments posted on both #3574 and PR #3575 explaining
  why the PR's own fix doesn't resolve this manifestation. Waiting on
  maintainer response on all three now. Re-checked 2026-10-16: all still
  open on LinkML 1.12.1, all three standalone reproductions under
  `examples/issues_for_linkml/` still reproduce, and a fix proposal for #3933
  specifically, [PR #4116](https://github.com/linkml/linkml/pull/4116), has
  since been opened (not merged).

## Future improvements (the "would a third party want to copy this" pass)

Prompted by a direct question: if Health-DCAT-AP-plus is "done" and
someone wants to build their own specialization the way ResHealth-DCAT-AP
does, is the *current* way ResHealth-DCAT-AP depends on Health-DCAT-AP-plus
what they should copy? Honest answer: not as-is. Almost everything fragile
in that relationship turns out to be either a genuine upstream LinkML bug,
or generic tooling that happens to live in the wrong repo — not something
inherent to Health-DCAT-AP-plus itself. In order (step 1 is done — see
"What's done" above):

1. ~~Extract the genuinely generic pieces into a small, real, versioned,
   installable package.~~ **Done** — `linkml-merge-toolkit`.
2. ~~**Check whether LinkML's own `SchemaLoader` "Conflicting URIs" bug
   (2+-level CURIE-resolved import chains) is already a known/reported
   issue, and report it if not.**~~ **It was never that bug** — the error
   came from what *we* published, and is gone (see "What's done",
   2026-10-19). ResHealth-DCAT-AP has no importmap any more, and
   `check_schema_resolves.py` there guards the published schema. What the
   investigation did turn up are two smaller,
   genuine gaps in the same legacy loader, neither blocking and **neither
   reported yet** (checked the tracker 2026-10-19; reproductions in
   `docs/architecture-verification.md`, "A twelfth finding", and as a script in
   `examples/issues_for_linkml/legacy-loader-gaps-repro.py`):
   (a) imports declared by a schema that was itself loaded over HTTP or by
   CURIE are resolved against the *root* schema (a bare name fails with
   `FileNotFoundError`) or mangled by `pathlib` (`./name` → backslashes on
   Windows, `//` collapsed everywhere) — the legacy-loader twin of what
   [linkml/linkml#3499](https://github.com/linkml/linkml/issues/3499) fixed
   for `SchemaView` (PR #3855, in 1.12.1), near
   [#3560](https://github.com/linkml/linkml/issues/3560) (open);
   (b) `gen-yaml`'s merged output keeps its `imports:` and so cannot be
   imported again — and it is what the LinkML project template publishes as
   `docs/schema/<name>.yaml`, so any template-based schema that is imported
   through its permalink would hit this.
2b. ~~Check whether LinkML's "imported schema prefixes don't propagate
   into `gen-shacl`/`gen-owl` output" gap is already known/reported, and
   report it if not.~~ **Root-caused precisely, going further than
   originally planned.** Checked first, per the plan: already tracked as
   [linkml/linkml#3574](https://github.com/linkml/linkml/issues/3574)
   ("prefixes declared by sub-schema are dropped during (merge) import"),
   with an open fix, [PR #3575](https://github.com/linkml/linkml/pull/3575).
   Prompted by being asked directly whether our own `xsd:` fix "could be
   hiding a deeper problem" — it did. Several hand-built minimal schemas
   failed to reproduce the bug even though the general mechanism looked
   simple; chasing that down (bisecting the real files, then reading
   `ShaclGenerator`/`SchemaView` source directly instead of guessing at
   schema shapes) found the *actual* mechanism: `SchemaView.namespaces()`
   is `@lru_cache(None)`-memoized with no invalidation, and gets called
   *from inside* `imports_closure()` itself (to resolve a CURIE-style
   import name) — so it can permanently cache an incomplete prefix map
   taken mid-traversal, before the schema that would supply a needed
   prefix (`xsd:`, from `linkml:types`) has loaded. Confirmed directly,
   not inferred: cleared the cache mid-run on the real files and watched
   resolution fix itself instantly. Also confirmed directly that PR
   #3575's own fix (`materialize_prefixes()`) does **not** resolve this
   specific manifestation — it mutates `schema.prefixes` but never clears
   `namespaces()`'s own cache, and by the time it runs, that cache is
   already poisoned. Neither #3574's own diagnosis nor #3575's own fix
   mention this. Reproduced standalone (three tiny synthetic schemas, zero
   network dependency, exact call-stack trace to the buggy line, plus a
   live demonstration that PR #3575's fix doesn't help) at
   `examples/issues_for_linkml/namespaces-cache-staleness.ipynb`. **Filed
   as [linkml/linkml#3933](https://github.com/linkml/linkml/issues/3933)**,
   cross-linked from #3574 and PR #3575 rather than folded into either —
   see "Blocked" below. See `docs/architecture-verification.md`'s "A tenth
   finding" section for the original `xsd:` story this grew out of.
3. **Have ResHealth-DCAT-AP clone `repos/healthdcat-ap` directly**,
   instead of reading it through Health-DCAT-AP-plus's own copy — simpler
   dependency graph, and it's what any third party would naturally do. Since
   2026-10-19 this, plus reusing this repo's `scripts/gen_merged_shacl.py`,
   is the *only* reason ResHealth-DCAT-AP still needs a Health-DCAT-AP-plus
   checkout: its schema import, generation and docs build go through the
   published w3id address.
4. **Only then, build a template repo** (via `linkml-project-copier`,
   matching how both current repos were bootstrapped) — pre-wiring the
   w3id import, the shared toolkit package dependency from step 1, the
   `gen-python`/`gen-shacl`/`test` recipes, a starter fixture, and clear
   instructions for the one legitimate clone step. Building this *before*
   the steps above would just template today's workarounds instead of
   fixing them.

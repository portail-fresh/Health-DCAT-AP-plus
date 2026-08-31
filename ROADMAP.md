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
- **An upstream proposal drafted and posted** to dcat-ap-plus's own GitHub
  Discussion: bring the generic PROV-O `Association`/`qualified_association`
  pattern upstream (it's not health-specific). A maintainer has responded
  positively; **currently waiting on further maintainer input** (see
  "Blocked" below).
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

## Problems that still need fixing

- **Known, deliberate SHACL violations** (`KNOWN_MERGED_SHAPES_VIOLATIONS`,
  2 entries, mirrored in both repos — down from 3; `title` turned out
  fixable after all, see "What's done" above). Both remaining are
  genuinely outside our own control, not unexplored: real LinkML
  `ShaclGenerator`-level bugs, not dcat-ap-plus's to fix either (the
  `ClassifierMixin`/`rdf_type` predicate collision, filed as
  [linkml/linkml#3931](https://github.com/linkml/linkml/issues/3931);
  `QualitativeAttribute`'s required field bleeding onto every `prov:Entity`
  node via a shared `class_uri`, filed as
  [linkml/linkml#3932](https://github.com/linkml/linkml/issues/3932)) —
  both diagnosed, reproduced standalone, and now filed; neither fixable
  from here, both waiting on upstream response.
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

- **The dcat-ap-plus Discussion** (Association/`qualified_association`
  proposal): posted, one maintainer response so far, more input requested
  from other maintainers. Nothing to do here until they respond — revisit
  the `ResearchAssociation`/`values_from` downstream design (sketched, not
  built) once it moves.
- **[linkml/linkml#3931](https://github.com/linkml/linkml/issues/3931)**
  (the `ClassifierMixin`/`rdf_type` finding) and
  **[linkml/linkml#3932](https://github.com/linkml/linkml/issues/3932)**
  (the `value`/`QualitativeAttribute` finding): both filed, both waiting
  on maintainer response. `KNOWN_MERGED_SHAPES_VIOLATIONS`' `type` and
  `value` entries stay in the allowlist until either gets fixed upstream.
  #3932 also still references closed issue
  [nfdi-de/dcat-ap-plus#15](https://github.com/nfdi-de/dcat-ap-plus/issues/15)
  and the design-patterns.md "three distinct node shapes" claim, which is
  empirically inaccurate (shapes get merged by `class_uri`, not kept
  distinct) — background only, not part of the issue text itself.
- **[linkml/linkml#3933](https://github.com/linkml/linkml/issues/3933)**
  (the `SchemaView.namespaces()` `@lru_cache` staleness finding): filed,
  with cross-link comments posted on both #3574 and PR #3575 explaining
  why the PR's own fix doesn't resolve this manifestation. Waiting on
  maintainer response on all three now.

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
2. **Check whether LinkML's own `SchemaLoader` "Conflicting URIs" bug
   (2+-level CURIE-resolved import chains) is already a known/reported
   issue, and report it if not.** Confirmed present even with direct
   `PythonGenerator`/`ShaclGenerator` instantiation, not just the CLI
   tools — a real LinkML bug, not a Health-DCAT-AP-plus-specific problem.
   The w3id permalink already resolves correctly on its own (confirmed
   directly via `SchemaView`); the sibling-checkout workaround exists
   *only* because of this separate bug in the generation tooling, not
   because the permalink is insufficient. Fixing it upstream would shrink
   the sibling-checkout requirement to just what's legitimately needed:
   cloning the *official* HealthDCAT-AP spec repo for real-shapes/
   vocabulary testing (a genuine third-party dependency, not a smell).
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
   dependency graph, and it's what any third party would naturally do.
4. **Only then, build a template repo** (via `linkml-project-copier`,
   matching how both current repos were bootstrapped) — pre-wiring the
   w3id import, the shared toolkit package dependency from step 1, the
   `gen-python`/`gen-shacl`/`test` recipes, a starter fixture, and clear
   instructions for the one legitimate clone step. Building this *before*
   the steps above would just template today's workarounds instead of
   fixing them.

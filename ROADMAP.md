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

## Problems that still need fixing

- **Known, deliberate SHACL violations** (`KNOWN_MERGED_SHAPES_VIOLATIONS`,
  3 entries, mirrored in both repos — down from 4; `hasQualityAnnotation`
  turned out fixable after all, see "What's done" above). All three
  remaining are genuinely outside our own control, not unexplored: `title`
  is an `rdflib`/`pyshacl` interoperability quirk (untyped literals don't
  satisfy an explicit `sh:datatype xsd:string`, even though RDF 1.1 says
  they're implicitly one) — a tooling-level issue, not ours or
  `dcat-ap-plus`'s to fix. `type` and `value` are real `dcat-ap-plus`-level
  bugs (the `ClassifierMixin`/`rdf_type` predicate collision;
  `QualitativeAttribute`'s required field bleeding onto every `prov:Entity`
  node via a shared `class_uri`) — both diagnosed, neither fixable from
  here; both belong in the upstream conversation once it's
  live again.
- **`public`/`restricted` HealthDCAT-AP tiers are unported.** Only
  `non-public` exists today. The port script's own README says the other
  two "should port the same way" — never actually run.
- **The sibling-checkout dependency pattern is a real, known limitation**
  (see "Future improvements" below) — not urgent, but it's the main thing
  standing between "works for us" and "ready for someone else to copy."

## Blocked, waiting on external input

- **The dcat-ap-plus Discussion** (Association/`qualified_association`
  proposal): posted, one maintainer response so far, more input requested
  from other maintainers. Nothing to do here until they respond — revisit
  the `type`/`value` findings above and the `HealthAssociation`/
  `values_from` downstream design (sketched, not built) once it moves.

## Future improvements (the "would a third party want to copy this" pass)

Prompted by a direct question: if Health-DCAT-AP-plus is "done" and
someone wants to build their own specialization the way ResHealth-DCAT-AP
does, is the *current* way ResHealth-DCAT-AP depends on Health-DCAT-AP-plus
what they should copy? Honest answer: not as-is. Almost everything fragile
in that relationship turns out to be either a genuine upstream LinkML bug,
or generic tooling that happens to live in the wrong repo — not something
inherent to Health-DCAT-AP-plus itself. In order:

1. **Extract the genuinely generic pieces into a small, real, versioned,
   installable package** — `patch_post_init_shielding.py`'s shield-map
   computation and `gen_merged_shacl.py`'s filtering logic
   (`filtered_own_shapes_graph`/`excluded_target_classes`/`_blank_closure`)
   are both schema-agnostic; neither has anything to do with health data
   specifically. Today ResHealth-DCAT-AP reaches into Health-DCAT-AP-plus's
   own `scripts/` directory directly, with no version pinning — the
   highest-leverage fix here, benefiting any future specializer, not just
   this one.
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

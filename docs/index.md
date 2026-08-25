# Health-DCAT-AP-plus

A schema combining HealthDCAT-AP's health-dataset metadata tiers with DCAT-AP+'s PROV-O provenance extensions (DataGeneratingActivity, Entity, AgenticEntity, Plan).

- Auto-generated [schema documentation](elements/index.md)

## `Health<X>` classes vs. plain DCAT-AP classes

For each class HealthDCAT-AP adds constraints to — `Dataset`, `Catalogue`, `Distribution`, `Agent`, and a few others — this schema provides a `Health<X>` version (`HealthDataset`, `HealthCatalogue`, `HealthDistribution`, `HealthAgent`, ...) alongside the plain one it comes from. Each `Health<X>` class is a superset of its base: every field the base class has, plus the additional health-specific fields and stricter requirements HealthDCAT-AP defines (e.g. `HealthDataset` adds `health_category`, `hdab`, tiered `access_rights`, and more, several of which it also requires).

**Important: `Health<X>` and its base class describe the same real-world RDF type, not two different ones.** `HealthDataset` and `Dataset` both convert to `a dcat:Dataset` — there is no separate "this is a health dataset" RDF type to check for. This is deliberate: it matches how HealthDCAT-AP's own official specification is written (it constrains `dcat:Dataset` directly, rather than inventing a new class), and it means a consumer can't tell a `HealthDataset` apart from a plain `Dataset` by `rdf:type` alone — only by which fields are actually present, or by validating against HealthDCAT-AP's SHACL shapes.

**Which one to use:**

- If the data needs to conform to HealthDCAT-AP (the EU/EHDS health-dataset profile) — use the `Health<X>` class. It's the only one with the required health-specific fields, and the only one that validates cleanly against HealthDCAT-AP's shapes.
- If it doesn't — the plain `dcat-ap-plus` class remains fully valid. There's no need or benefit to using `Health<X>` for non-health data; it would just require populating fields that don't apply.
- Both can be mixed freely in the same catalogue — nothing about using one forces the other, and there's no RDF-level conflict between them.

For the full reasoning and verification evidence behind this design (including why a shared `class_uri` was chosen over a distinct one), see [`docs/architecture-verification.md`](architecture-verification.md).

# Examples of using Health-DCAT-AP-Plus

This folder contains examples using the datamodel.

The source of the data used in the example is [tests/data](../tests/data/).

The command `just test` creates different representations of the data in [tests/data](../tests/data/) and writes them to the subfolder `output`.
It also generates a markdown documentation of the examples which is not very useful in its current form.
Hence, the `output` sub-folder is git-ignored.

## `HealthDataset-full-example.ttl`

A full worked instance -- a cancer registry `HealthDataset` with agents,
activities, entities, dataset-level attribution, and (on the
`DataGeneratingActivity`) three `qualified_association` entries for a PI,
sponsor, and funder. Source YAML:
[tests/data/problem/valid/HealthDataset-shacl-full.yaml](../tests/data/problem/valid/HealthDataset-shacl-full.yaml).
Unlike the rest of this folder, not produced by `just test`'s
`linkml-run-examples` step -- see the file's own header comment for how
it's regenerated and why it needs a dedicated construction helper
(`tests/test_shacl_validation.py`). Validated against both this repo's own
generated SHACL and HealthDCAT-AP's real, official shapes -- see
[docs/architecture-verification.md](../docs/architecture-verification.md)
sections 5-6.

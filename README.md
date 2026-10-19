<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# Health-DCAT-AP-plus

A schema combining HealthDCAT-AP's health-dataset metadata tiers with DCAT-AP+'s PROV-O provenance extensions (DataGeneratingActivity, Entity, AgenticEntity, Plan).

The schema (`src/health_dcat_ap_plus/schema/health_dcat_ap_plus.yaml`) imports
[dcat-ap-plus](https://github.com/nfdi-de/dcat-ap-plus) directly via its w3id
permalink, plus a generated file,
`src/health_dcat_ap_plus/schema/healthdcat_ap_non_public.yaml`, which ports
HealthDCAT-AP's *non-public* tier SHACL shapes to LinkML. HealthDCAT-AP has no
LinkML schema of its own (only SHACL), so that file is produced mechanically
by `scripts/port_healthdcat_ap_shacl_to_linkml.py` — the same
targetClass/sh:property-walking method
[NFDI4Chem used to port plain DCAT-AP's SHACL to LinkML](https://github.com/nfdi-de/chem-dcat-ap)
when building `chem-dcat-ap`. **Do not hand-edit the generated file** —
re-run the script instead (see its own docstring for the method, known
limitations, and how classes/slots are named).

To regenerate after `repos/healthdcat-ap` or `repos/dcat-ap-plus` are updated
(shallow clones, gitignored — re-clone with `git clone --depth 1
https://github.com/nfdi-de/dcat-ap-plus.git repos/dcat-ap-plus` and `git
clone --depth 1 https://code.europa.eu/healthdataeu/healthdcat-ap.git
repos/healthdcat-ap`):

```
.venv/Scripts/python scripts/port_healthdcat_ap_shacl_to_linkml.py \
  repos/healthdcat-ap/public/releases/release-7/html/shacl \
  repos/dcat-ap-plus/src/dcat_ap_plus/schema/dcat_ap_plus.yaml \
  src/health_dcat_ap_plus/schema/healthdcat_ap_non_public.yaml \
  --tier non-public \
  --healthdcat-ap-repo repos/healthdcat-ap
```

Only the `non-public` tier is ported so far; `public` and `restricted` use
the same shape files (`--tier public` / `--tier restricted`) and should port
the same way.

dcat-ap-plus is imported at a **pinned release** (currently `v0.1.0rc5`), not
`latest`, so a new release changes nothing — here or for anyone importing this
schema — until it is bumped on purpose. To bump: change the import in
`health_dcat_ap_plus.yaml` and `DCAT_AP_PLUS_IMPORT` in the port script, check
out the same tag in `repos/dcat-ap-plus`, re-run the command above, run
`just test` (`tests/test_published_schema.py` fails if the two disagree) and
`just gen-doc` to refresh `docs/schema/`.

## Importing this schema from another schema

Specializations import it through its w3id permalink, the way
[ResHealth-DCAT-AP](https://github.com/portail-fresh/ResHealth-DCAT-AP) does:

```yaml
prefixes:
  healthdcatapplus: https://w3id.org/portail-fresh/Health-DCAT-AP-plus/
  dcatap_plus: https://w3id.org/nfdi-de/dcat-ap-plus/
  # ... plus the other prefixes of this schema's own `prefixes:` block
imports:
  - linkml:types
  - healthdcatapplus:latest/schema/health_dcat_ap_plus
```

That is all: no importmap and no sibling checkout, with either of LinkML's
loaders (ResHealth-DCAT-AP's `scripts/check_schema_resolves.py` checks both on
every test run). The importing schema does have to redeclare `dcatap_plus` and the other prefixes listed here, because LinkML
expands a nested import's CURIE with the *importing* schema's prefix map and
does not carry an imported schema's prefixes into generated output — see
[the eleventh finding](docs/architecture-verification.md) for why.

What the permalink serves (`docs/schema/`, written by
`scripts/publish_schema.py`, which `just gen-doc` runs):

* `health_dcat_ap_plus.yaml` — **import this one.** A copy of the source
  schema; the only difference is that its sibling import is an absolute URL.
* `healthdcat_ap_non_public.yaml` — the generated sibling it imports.
* `health_dcat_ap_plus.merged.yaml` — `gen-yaml`'s output: the whole model,
  dcat-ap-plus included, in a single file, for reading. **Do not import it.**
  It still lists its imports, so every dcat-ap-plus class would be defined
  twice and LinkML's legacy loader fails with "Conflicting URIs". Served by
  [GitHub Pages](https://portail-fresh.github.io/Health-DCAT-AP-plus/schema/health_dcat_ap_plus.merged.yaml)
  only; w3id has no rule for it.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for what's done, what's still open, and
planned future improvements across both this repo and
[ResHealth-DCAT-AP](https://github.com/portail-fresh/ResHealth-DCAT-AP).

## Documentation Website

[https://portail-fresh.github.io/Health-DCAT-AP-plus](https://portail-fresh.github.io/Health-DCAT-AP-plus)

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [src/](src/) - source files (edit these)
  * [health_dcat_ap_plus](src/health_dcat_ap_plus)
    * [schema/](src/health_dcat_ap_plus/schema) -- LinkML schema
      (edit this)
    * [datamodel/](src/health_dcat_ap_plus/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/).
To list all pre-defined commands, run `just` or `just --list`.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier).

It builds directly on [nfdi-de/dcat-ap-plus](https://github.com/nfdi-de/dcat-ap-plus)
(imported, not forked) and follows the SHACL-to-LinkML porting method
pioneered by [nfdi-de/chem-dcat-ap](https://github.com/nfdi-de/chem-dcat-ap)
to bring in [HealthDCAT-AP](https://code.europa.eu/healthdataeu/healthdcat-ap)
(EU Commission / EHDS), which has no LinkML form of its own. See also the
sibling project [ResHealth-DCAT-AP](https://github.com/portail-fresh/ResHealth-DCAT-AP),
which specializes `dcat-ap-plus` for research-study metadata rather than
health-dataset metadata.

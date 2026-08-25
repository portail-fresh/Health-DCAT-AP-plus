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

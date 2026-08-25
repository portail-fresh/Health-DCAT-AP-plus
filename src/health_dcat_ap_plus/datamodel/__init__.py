"""Data model package for Health-DCAT-AP-plus."""

from pathlib import Path
from .health_dcat_ap_plus import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "health_dcat_ap_plus.yaml"

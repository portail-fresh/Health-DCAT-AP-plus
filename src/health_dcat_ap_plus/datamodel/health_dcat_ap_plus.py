# Auto generated from health_dcat_ap_plus.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-08-24T16:10:37
# Schema: Health-DCAT-AP-Plus
#
# id: https://w3id.org/portail-fresh/Health-DCAT-AP-plus
# description: A schema combining HealthDCAT-AP's health-dataset metadata tiers with DCAT-AP+'s PROV-O provenance extensions (DataGeneratingActivity, Entity, AgenticEntity, Plan).
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Decimal, Float, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, Decimal, URIorCURIE, XSDDate

metamodel_version = "1.11.0"
version = None

# Namespaces
AFE = CurieNamespace('AFE', 'http://purl.allotrope.org/ontologies/equipment#AFE_')
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
NCIT = CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_')
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
SIO = CurieNamespace('SIO', 'http://semanticscience.org/resource/SIO_')
ADMS = CurieNamespace('adms', 'http://www.w3.org/ns/adms#')
CSVW = CurieNamespace('csvw', 'http://www.w3.org/ns/csvw#')
CV = CurieNamespace('cv', 'http://data.europa.eu/m8g/')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCATAP = CurieNamespace('dcatap', 'http://data.europa.eu/r5r/')
DCATAPPLUS = CurieNamespace('dcatapplus', 'https://w3id.org/nfdi-de/dcat-ap-plus/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
DPV = CurieNamespace('dpv', 'https://w3id.org/dpv#')
DQV = CurieNamespace('dqv', 'http://www.w3.org/ns/dqv#')
ELI = CurieNamespace('eli', 'http://data.europa.eu/eli/ontology#')
EPOS = CurieNamespace('epos', 'https://www.epos-eu.org/epos-dcat-ap#')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
GEODCATAP = CurieNamespace('geodcatap', 'http://data.europa.eu/930/')
HEALTH_DCAT_AP_PLUS = CurieNamespace('health_dcat_ap_plus', 'https://w3id.org/portail-fresh/Health-DCAT-AP-plus/')
HEALTHDCATAP = CurieNamespace('healthdcatap', 'http://healthdataportal.eu/ns/health#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LOCN = CurieNamespace('locn', 'http://www.w3.org/ns/locn#')
ODRL = CurieNamespace('odrl', 'http://www.w3.org/ns/odrl/2/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
QUDT = CurieNamespace('qudt', 'http://qudt.org/schema/qudt/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SPDX = CurieNamespace('spdx', 'http://spdx.org/rdf/terms#')
TIME = CurieNamespace('time', 'http://www.w3.org/2006/time#')
VCARD = CurieNamespace('vcard', 'http://www.w3.org/2006/vcard/ns#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = HEALTH_DCAT_AP_PLUS


# Types
class Duration(str):
    """ The datatype that represents durations of time. """
    type_class_uri = XSD["duration"]
    type_class_curie = "xsd:duration"
    type_name = "duration"
    type_model_uri = HEALTH_DCAT_AP_PLUS.Duration


class HexBinary(str):
    """ The datatype that represents arbitrary hex-encoded binary data. """
    type_class_uri = XSD["hexBinary"]
    type_class_curie = "xsd:hexBinary"
    type_name = "hexBinary"
    type_model_uri = HEALTH_DCAT_AP_PLUS.HexBinary


class NonNegativeInteger(int):
    """ The datatype that represents non-negative integers. """
    type_class_uri = XSD["nonNegativeInteger"]
    type_class_curie = "xsd:nonNegativeInteger"
    type_name = "nonNegativeInteger"
    type_model_uri = HEALTH_DCAT_AP_PLUS.NonNegativeInteger


# Class references
class ActivityId(URIorCURIE):
    pass


class AgenticEntityId(URIorCURIE):
    pass


class DataGeneratingActivityId(ActivityId):
    pass


class AssociatedDataGeneratingActivityId(DataGeneratingActivityId):
    pass


class DataAnalysisId(DataGeneratingActivityId):
    pass


class DatasetId(URIorCURIE):
    pass


class AnalysisDatasetId(DatasetId):
    pass


class DefinedTermId(URIorCURIE):
    pass


class DeviceId(AgenticEntityId):
    pass


class EntityId(URIorCURIE):
    pass


class EvaluatedActivityId(ActivityId):
    pass


class EvaluatedEntityId(EntityId):
    pass


class AnalysisSourceDataId(EvaluatedEntityId):
    pass


class SoftwareId(AgenticEntityId):
    pass


class DocumentId(URIorCURIE):
    pass


class LegalResourceId(URIorCURIE):
    pass


class LicenseDocumentId(URIorCURIE):
    pass


class ResourceId(URIorCURIE):
    pass


class HealthDatasetId(DatasetId):
    pass


class HealthLicenseDocumentId(LicenseDocumentId):
    pass


class LegalBasisId(URIorCURIE):
    pass


class PersonalDataId(URIorCURIE):
    pass


class PurposeId(URIorCURIE):
    pass


class QualityCertificateId(URIorCURIE):
    pass


@dataclass(repr=False)
class Activity(YAMLRoot):
    """
    See [DCAT-AP specs:Activity](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Activity)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Activity

    id: Union[str, ActivityId] = None
    title: Optional[Union[str, list[str]]] = empty_list()
    description: Optional[Union[str, list[str]]] = empty_list()
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()
    has_part: Optional[Union[dict[Union[str, ActivityId], Union[dict, "Activity"]], list[Union[dict, "Activity"]]]] = empty_dict()
    had_input_entity: Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]] = empty_dict()
    had_output_entity: Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]] = empty_dict()
    had_input_activity: Optional[Union[dict[Union[str, ActivityId], Union[dict, "Activity"]], list[Union[dict, "Activity"]]]] = empty_dict()
    carried_out_by: Optional[Union[dict[Union[str, AgenticEntityId], Union[dict, "AgenticEntity"]], list[Union[dict, "AgenticEntity"]]]] = empty_dict()
    has_qualitative_attribute: Optional[Union[Union[dict, "QualitativeAttribute"], list[Union[dict, "QualitativeAttribute"]]]] = empty_list()
    has_quantitative_attribute: Optional[Union[Union[dict, "QuantitativeAttribute"], list[Union[dict, "QuantitativeAttribute"]]]] = empty_list()
    part_of: Optional[Union[dict[Union[str, ActivityId], Union[dict, "Activity"]], list[Union[dict, "Activity"]]]] = empty_dict()
    type: Optional[Union[dict, "DefinedTerm"]] = None
    rdf_type: Optional[Union[dict, "DefinedTerm"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActivityId):
            self.id = ActivityId(self.id)

        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_part", slot_type=Activity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="had_input_entity", slot_type=Entity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="had_output_entity", slot_type=Entity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="had_input_activity", slot_type=Activity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="carried_out_by", slot_type=AgenticEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="has_qualitative_attribute", slot_type=QualitativeAttribute, key_name="value", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_quantitative_attribute", slot_type=QuantitativeAttribute, key_name="value", keyed=False)

        self._normalize_inlined_as_list(slot_name="part_of", slot_type=Activity, key_name="id", keyed=True)

        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Agent(YAMLRoot):
    """
    See [DCAT-AP specs:Agent](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Agent)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Agent"]
    class_class_curie: ClassVar[str] = "foaf:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Agent

    name: Union[str, list[str]] = None
    type: Optional[Union[dict, "Concept"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, list):
            self.name = [self.name] if self.name is not None else []
        self.name = [v if isinstance(v, str) else str(v) for v in self.name]

        if self.type is not None and not isinstance(self.type, Concept):
            self.type = Concept(**as_dict(self.type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AgenticEntity(YAMLRoot):
    """
    An entity that is somehow responsible for an Activity to take place.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Agent"]
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "AgenticEntity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.AgenticEntity

    id: Union[str, AgenticEntityId] = None
    title: Optional[str] = None
    description: Optional[str] = None
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()
    has_qualitative_attribute: Optional[Union[Union[dict, "QualitativeAttribute"], list[Union[dict, "QualitativeAttribute"]]]] = empty_list()
    has_quantitative_attribute: Optional[Union[Union[dict, "QuantitativeAttribute"], list[Union[dict, "QuantitativeAttribute"]]]] = empty_list()
    has_part: Optional[Union[dict[Union[str, AgenticEntityId], Union[dict, "AgenticEntity"]], list[Union[dict, "AgenticEntity"]]]] = empty_dict()
    part_of: Optional[Union[dict[Union[str, AgenticEntityId], Union[dict, "AgenticEntity"]], list[Union[dict, "AgenticEntity"]]]] = empty_dict()
    type: Optional[Union[dict, "DefinedTerm"]] = None
    rdf_type: Optional[Union[dict, "DefinedTerm"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AgenticEntityId):
            self.id = AgenticEntityId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_qualitative_attribute", slot_type=QualitativeAttribute, key_name="value", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_quantitative_attribute", slot_type=QuantitativeAttribute, key_name="value", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_part", slot_type=AgenticEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="part_of", slot_type=AgenticEntity, key_name="id", keyed=True)

        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


Any = Any

@dataclass(repr=False)
class Catalogue(YAMLRoot):
    """
    See [DCAT-AP specs:Catalogue](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Catalogue)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Catalog"]
    class_class_curie: ClassVar[str] = "dcat:Catalog"
    class_name: ClassVar[str] = "Catalogue"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Catalogue

    description: Union[str, list[str]] = None
    publisher: Union[dict, Agent] = None
    title: Union[str, list[str]] = None
    applicable_legislation: Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]] = empty_dict()
    catalogue: Optional[Union[Union[dict, "Catalogue"], list[Union[dict, "Catalogue"]]]] = empty_list()
    creator: Optional[Union[dict, Agent]] = None
    geographical_coverage: Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]] = empty_list()
    has_dataset: Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]] = empty_dict()
    has_part: Optional[Union[Union[dict, "Catalogue"], list[Union[dict, "Catalogue"]]]] = empty_list()
    homepage: Optional[Union[dict, "Document"]] = None
    language: Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]] = empty_list()
    licence: Optional[Union[dict, "LicenseDocument"]] = None
    modification_date: Optional[Union[str, XSDDate]] = None
    record: Optional[Union[Union[dict, "CatalogueRecord"], list[Union[dict, "CatalogueRecord"]]]] = empty_list()
    release_date: Optional[Union[str, XSDDate]] = None
    rights: Optional[Union[dict, "RightsStatement"]] = None
    service: Optional[Union[Union[dict, "DataService"], list[Union[dict, "DataService"]]]] = empty_list()
    temporal_coverage: Optional[Union[Union[dict, "PeriodOfTime"], list[Union[dict, "PeriodOfTime"]]]] = empty_list()
    themes: Optional[Union[Union[dict, "ConceptScheme"], list[Union[dict, "ConceptScheme"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        if self._is_empty(self.publisher):
            self.MissingRequiredField("publisher")
        if not isinstance(self.publisher, Agent):
            self.publisher = Agent(**as_dict(self.publisher))

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="catalogue", slot_type=Catalogue, key_name="description", keyed=False)

        if self.creator is not None and not isinstance(self.creator, Agent):
            self.creator = Agent(**as_dict(self.creator))

        if not isinstance(self.geographical_coverage, list):
            self.geographical_coverage = [self.geographical_coverage] if self.geographical_coverage is not None else []
        self.geographical_coverage = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.geographical_coverage]

        self._normalize_inlined_as_list(slot_name="has_dataset", slot_type=Dataset, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="has_part", slot_type=Catalogue, key_name="description", keyed=False)

        if self.homepage is not None and not isinstance(self.homepage, Document):
            self.homepage = Document(**as_dict(self.homepage))

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, LinguisticSystem) else LinguisticSystem(**as_dict(v)) for v in self.language]

        if self.licence is not None and not isinstance(self.licence, LicenseDocument):
            self.licence = LicenseDocument(**as_dict(self.licence))

        if self.modification_date is not None and not isinstance(self.modification_date, XSDDate):
            self.modification_date = XSDDate(self.modification_date)

        self._normalize_inlined_as_list(slot_name="record", slot_type=CatalogueRecord, key_name="modification_date", keyed=False)

        if self.release_date is not None and not isinstance(self.release_date, XSDDate):
            self.release_date = XSDDate(self.release_date)

        if self.rights is not None and not isinstance(self.rights, RightsStatement):
            self.rights = RightsStatement(**as_dict(self.rights))

        self._normalize_inlined_as_list(slot_name="service", slot_type=DataService, key_name="title", keyed=False)

        if not isinstance(self.temporal_coverage, list):
            self.temporal_coverage = [self.temporal_coverage] if self.temporal_coverage is not None else []
        self.temporal_coverage = [v if isinstance(v, PeriodOfTime) else PeriodOfTime(**as_dict(v)) for v in self.temporal_coverage]

        self._normalize_inlined_as_list(slot_name="themes", slot_type=ConceptScheme, key_name="title", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CatalogueRecord(YAMLRoot):
    """
    See [DCAT-AP specs:CatalogueRecord](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#CatalogueRecord)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["CatalogRecord"]
    class_class_curie: ClassVar[str] = "dcat:CatalogRecord"
    class_name: ClassVar[str] = "CatalogueRecord"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.CatalogueRecord

    modification_date: Union[str, XSDDate] = None
    primary_topic: Union[dict, Any] = None
    application_profile: Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]] = empty_list()
    change_type: Optional[Union[dict, "Concept"]] = None
    description: Optional[Union[str, list[str]]] = empty_list()
    language: Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]] = empty_list()
    listing_date: Optional[Union[str, XSDDate]] = None
    source_metadata: Optional[Union[dict, "CatalogueRecord"]] = None
    title: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.modification_date):
            self.MissingRequiredField("modification_date")
        if not isinstance(self.modification_date, XSDDate):
            self.modification_date = XSDDate(self.modification_date)

        if not isinstance(self.application_profile, list):
            self.application_profile = [self.application_profile] if self.application_profile is not None else []
        self.application_profile = [v if isinstance(v, Standard) else Standard(**as_dict(v)) for v in self.application_profile]

        if self.change_type is not None and not isinstance(self.change_type, Concept):
            self.change_type = Concept(**as_dict(self.change_type))

        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, LinguisticSystem) else LinguisticSystem(**as_dict(v)) for v in self.language]

        if self.listing_date is not None and not isinstance(self.listing_date, XSDDate):
            self.listing_date = XSDDate(self.listing_date)

        if self.source_metadata is not None and not isinstance(self.source_metadata, CatalogueRecord):
            self.source_metadata = CatalogueRecord(**as_dict(self.source_metadata))

        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Checksum(YAMLRoot):
    """
    See [DCAT-AP specs:Checksum](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Checksum)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SPDX["Checksum"]
    class_class_curie: ClassVar[str] = "spdx:Checksum"
    class_name: ClassVar[str] = "Checksum"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Checksum

    algorithm: Union[dict, "ChecksumAlgorithm"] = None
    checksum_value: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.algorithm):
            self.MissingRequiredField("algorithm")
        if not isinstance(self.algorithm, ChecksumAlgorithm):
            self.algorithm = ChecksumAlgorithm(**as_dict(self.algorithm))

        if self._is_empty(self.checksum_value):
            self.MissingRequiredField("checksum_value")
        if not isinstance(self.checksum_value, str):
            self.checksum_value = str(self.checksum_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClassifierMixin(YAMLRoot):
    """
    A mixin with which an entity of this schema can be classified via an additional rdf:type or dcterms:type assertion.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCATAPPLUS["ClassifierMixin"]
    class_class_curie: ClassVar[str] = "dcatapplus:ClassifierMixin"
    class_name: ClassVar[str] = "ClassifierMixin"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.ClassifierMixin

    type: Optional[Union[dict, "DefinedTerm"]] = None
    rdf_type: Optional[Union[dict, "DefinedTerm"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataGeneratingActivity(Activity):
    """
    An Activity (process) that has the objective to produce information (in form of a dataset) about another Activity
    or Entity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "DataGeneratingActivity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.DataGeneratingActivity

    id: Union[str, DataGeneratingActivityId] = None
    evaluated_entity: Optional[Union[dict[Union[str, EvaluatedEntityId], Union[dict, "EvaluatedEntity"]], list[Union[dict, "EvaluatedEntity"]]]] = empty_dict()
    evaluated_activity: Optional[Union[dict[Union[str, EvaluatedActivityId], Union[dict, "EvaluatedActivity"]], list[Union[dict, "EvaluatedActivity"]]]] = empty_dict()
    realized_plan: Optional[Union[dict, "Plan"]] = None
    occurred_in: Optional[Union[dict, "Surrounding"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataGeneratingActivityId):
            self.id = DataGeneratingActivityId(self.id)

        self._normalize_inlined_as_list(slot_name="evaluated_entity", slot_type=EvaluatedEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="evaluated_activity", slot_type=EvaluatedActivity, key_name="id", keyed=True)

        if self.realized_plan is not None and not isinstance(self.realized_plan, Plan):
            self.realized_plan = Plan(**as_dict(self.realized_plan))

        if self.occurred_in is not None and not isinstance(self.occurred_in, Surrounding):
            self.occurred_in = Surrounding(**as_dict(self.occurred_in))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AssociatedDataGeneratingActivity(DataGeneratingActivity):
    """
    DataGeneratingActivity, with qualified_association actually wired in -- was_generated_by can then carry
    PI/sponsor/funder-style agent roles on a real HealthDataset instance, not just document that the slot exists.
    Originally deferred as "specialization work" (the same line drawn for DatasetAttribution/HealthDataset): the
    reasoning was never "Activity-side classes belong exclusively downstream," it was "don't invent a class before
    there's a real need for it." This one is exactly as generic as Association itself -- no health-specific content,
    just DataGeneratingActivity plus the one slot that makes qualified_association reachable -- so once a real need
    appeared (an end-to-end example with AgenticEntities on Activities), building it here is the same kind of generic
    completion Association already is, not a boundary violation.
    Can't be done by narrowing HealthDataset.was_generated_by's range directly onto this class from either file:
    HealthDataset lives in the generated healthdcat_ap_non_public.yaml, which doesn't import this file (this file
    imports it, not the reverse, so it can't see Association/qualified_association), and this file can't reopen
    HealthDataset's own already-imported slot_usage either (confirmed elsewhere this session: reopening an imported
    class throws "Conflicting URIs"). Used directly instead, by constructing real instances of this class in place of
    plain DataGeneratingActivity ones -- isinstance-compatible since it's a real subclass, so LinkML's own
    inlined-list construction (_normalize_inlined_as_list) accepts an already-built instance as-is without needing to
    touch was_generated_by's declared range at all. See tests/test_shacl_validation.py for the real instance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "AssociatedDataGeneratingActivity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.AssociatedDataGeneratingActivity

    id: Union[str, AssociatedDataGeneratingActivityId] = None
    qualified_association: Optional[Union[Union[dict, "Association"], list[Union[dict, "Association"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AssociatedDataGeneratingActivityId):
            self.id = AssociatedDataGeneratingActivityId(self.id)

        self._normalize_inlined_as_list(slot_name="qualified_association", slot_type=Association, key_name="association_had_role", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataAnalysis(DataGeneratingActivity):
    """
    An Activity that evaluates the data produced by another Activity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "DataAnalysis"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.DataAnalysis

    id: Union[str, DataAnalysisId] = None
    evaluated_entity: Optional[Union[dict[Union[str, AnalysisSourceDataId], Union[dict, "AnalysisSourceData"]], list[Union[dict, "AnalysisSourceData"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataAnalysisId):
            self.id = DataAnalysisId(self.id)

        self._normalize_inlined_as_list(slot_name="evaluated_entity", slot_type=AnalysisSourceData, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataService(YAMLRoot):
    """
    See [DCAT-AP specs:DataService](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#DataService)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["DataService"]
    class_class_curie: ClassVar[str] = "dcat:DataService"
    class_name: ClassVar[str] = "DataService"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.DataService

    endpoint_URL: Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]] = empty_dict()
    title: Union[str, list[str]] = None
    access_rights: Optional[Union[dict, "RightsStatement"]] = None
    applicable_legislation: Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]] = empty_dict()
    conforms_to: Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]] = empty_list()
    contact_point: Optional[Union[Union[dict, "Kind"], list[Union[dict, "Kind"]]]] = empty_list()
    description: Optional[Union[str, list[str]]] = empty_list()
    documentation: Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]] = empty_dict()
    endpoint_description: Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]] = empty_dict()
    format: Optional[Union[Union[dict, "MediaTypeOrExtent"], list[Union[dict, "MediaTypeOrExtent"]]]] = empty_list()
    keyword: Optional[Union[str, list[str]]] = empty_list()
    landing_page: Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]] = empty_dict()
    licence: Optional[Union[dict, "LicenseDocument"]] = None
    publisher: Optional[Union[dict, Agent]] = None
    serves_dataset: Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]] = empty_dict()
    theme: Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.endpoint_URL):
            self.MissingRequiredField("endpoint_URL")
        self._normalize_inlined_as_list(slot_name="endpoint_URL", slot_type=Resource, key_name="id", keyed=True)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        if self.access_rights is not None and not isinstance(self.access_rights, RightsStatement):
            self.access_rights = RightsStatement(**as_dict(self.access_rights))

        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        if not isinstance(self.conforms_to, list):
            self.conforms_to = [self.conforms_to] if self.conforms_to is not None else []
        self.conforms_to = [v if isinstance(v, Standard) else Standard(**as_dict(v)) for v in self.conforms_to]

        if not isinstance(self.contact_point, list):
            self.contact_point = [self.contact_point] if self.contact_point is not None else []
        self.contact_point = [v if isinstance(v, Kind) else Kind(**as_dict(v)) for v in self.contact_point]

        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        self._normalize_inlined_as_list(slot_name="documentation", slot_type=Document, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="endpoint_description", slot_type=Resource, key_name="id", keyed=True)

        if not isinstance(self.format, list):
            self.format = [self.format] if self.format is not None else []
        self.format = [v if isinstance(v, MediaTypeOrExtent) else MediaTypeOrExtent(**as_dict(v)) for v in self.format]

        if not isinstance(self.keyword, list):
            self.keyword = [self.keyword] if self.keyword is not None else []
        self.keyword = [v if isinstance(v, str) else str(v) for v in self.keyword]

        self._normalize_inlined_as_list(slot_name="landing_page", slot_type=Document, key_name="id", keyed=True)

        if self.licence is not None and not isinstance(self.licence, LicenseDocument):
            self.licence = LicenseDocument(**as_dict(self.licence))

        if self.publisher is not None and not isinstance(self.publisher, Agent):
            self.publisher = Agent(**as_dict(self.publisher))

        self._normalize_inlined_as_list(slot_name="serves_dataset", slot_type=Dataset, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="theme", slot_type=Concept, key_name="preferred_label", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Dataset(YAMLRoot):
    """
    A collection of data, published or curated by a single agent, and available for access or download in one or more
    representations.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Dataset"]
    class_class_curie: ClassVar[str] = "dcat:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Dataset

    id: Union[str, DatasetId] = None
    description: Union[str, list[str]] = None
    title: Union[str, list[str]] = None
    was_generated_by: Union[dict[Union[str, DataGeneratingActivityId], Union[dict, DataGeneratingActivity]], list[Union[dict, DataGeneratingActivity]]] = empty_dict()
    access_rights: Optional[Union[dict, "RightsStatement"]] = None
    applicable_legislation: Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]] = empty_dict()
    conforms_to: Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]] = empty_list()
    contact_point: Optional[Union[Union[dict, "Kind"], list[Union[dict, "Kind"]]]] = empty_list()
    creator: Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]] = empty_list()
    dataset_distribution: Optional[Union[Union[dict, "Distribution"], list[Union[dict, "Distribution"]]]] = empty_list()
    documentation: Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]] = empty_dict()
    frequency: Optional[Union[dict, "Frequency"]] = None
    geographical_coverage: Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]] = empty_list()
    has_version: Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]] = empty_dict()
    identifier: Optional[Union[str, list[str]]] = empty_list()
    in_series: Optional[Union[Union[dict, "DatasetSeries"], list[Union[dict, "DatasetSeries"]]]] = empty_list()
    is_referenced_by: Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]] = empty_dict()
    keyword: Optional[Union[str, list[str]]] = empty_list()
    landing_page: Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]] = empty_dict()
    language: Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]] = empty_list()
    modification_date: Optional[Union[str, XSDDate]] = None
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()
    provenance: Optional[Union[Union[dict, "ProvenanceStatement"], list[Union[dict, "ProvenanceStatement"]]]] = empty_list()
    publisher: Optional[Union[dict, Agent]] = None
    qualified_attribution: Optional[Union[Union[dict, "Attribution"], list[Union[dict, "Attribution"]]]] = empty_list()
    qualified_relation: Optional[Union[Union[dict, "Relationship"], list[Union[dict, "Relationship"]]]] = empty_list()
    related_resource: Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]] = empty_dict()
    release_date: Optional[Union[str, XSDDate]] = None
    sample: Optional[Union[Union[dict, "Distribution"], list[Union[dict, "Distribution"]]]] = empty_list()
    source: Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]] = empty_dict()
    spatial_resolution: Optional[Decimal] = None
    temporal_coverage: Optional[Union[Union[dict, "PeriodOfTime"], list[Union[dict, "PeriodOfTime"]]]] = empty_list()
    temporal_resolution: Optional[str] = None
    theme: Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]] = empty_list()
    type: Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]] = empty_list()
    version: Optional[str] = None
    version_notes: Optional[Union[str, list[str]]] = empty_list()
    is_about_entity: Optional[Union[dict[Union[str, EvaluatedEntityId], Union[dict, "EvaluatedEntity"]], list[Union[dict, "EvaluatedEntity"]]]] = empty_dict()
    is_about_activity: Optional[Union[dict[Union[str, EvaluatedActivityId], Union[dict, "EvaluatedActivity"]], list[Union[dict, "EvaluatedActivity"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetId):
            self.id = DatasetId(self.id)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        if self._is_empty(self.was_generated_by):
            self.MissingRequiredField("was_generated_by")
        self._normalize_inlined_as_list(slot_name="was_generated_by", slot_type=DataGeneratingActivity, key_name="id", keyed=True)

        if self.access_rights is not None and not isinstance(self.access_rights, RightsStatement):
            self.access_rights = RightsStatement(**as_dict(self.access_rights))

        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        if not isinstance(self.conforms_to, list):
            self.conforms_to = [self.conforms_to] if self.conforms_to is not None else []
        self.conforms_to = [v if isinstance(v, Standard) else Standard(**as_dict(v)) for v in self.conforms_to]

        if not isinstance(self.contact_point, list):
            self.contact_point = [self.contact_point] if self.contact_point is not None else []
        self.contact_point = [v if isinstance(v, Kind) else Kind(**as_dict(v)) for v in self.contact_point]

        self._normalize_inlined_as_list(slot_name="creator", slot_type=Agent, key_name="name", keyed=False)

        if not isinstance(self.dataset_distribution, list):
            self.dataset_distribution = [self.dataset_distribution] if self.dataset_distribution is not None else []
        self.dataset_distribution = [v if isinstance(v, Distribution) else Distribution(**as_dict(v)) for v in self.dataset_distribution]

        self._normalize_inlined_as_list(slot_name="documentation", slot_type=Document, key_name="id", keyed=True)

        if self.frequency is not None and not isinstance(self.frequency, Frequency):
            self.frequency = Frequency(**as_dict(self.frequency))

        if not isinstance(self.geographical_coverage, list):
            self.geographical_coverage = [self.geographical_coverage] if self.geographical_coverage is not None else []
        self.geographical_coverage = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.geographical_coverage]

        self._normalize_inlined_as_list(slot_name="has_version", slot_type=Dataset, key_name="id", keyed=True)

        if not isinstance(self.identifier, list):
            self.identifier = [self.identifier] if self.identifier is not None else []
        self.identifier = [v if isinstance(v, str) else str(v) for v in self.identifier]

        self._normalize_inlined_as_list(slot_name="in_series", slot_type=DatasetSeries, key_name="description", keyed=False)

        self._normalize_inlined_as_list(slot_name="is_referenced_by", slot_type=Resource, key_name="id", keyed=True)

        if not isinstance(self.keyword, list):
            self.keyword = [self.keyword] if self.keyword is not None else []
        self.keyword = [v if isinstance(v, str) else str(v) for v in self.keyword]

        self._normalize_inlined_as_list(slot_name="landing_page", slot_type=Document, key_name="id", keyed=True)

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, LinguisticSystem) else LinguisticSystem(**as_dict(v)) for v in self.language]

        if self.modification_date is not None and not isinstance(self.modification_date, XSDDate):
            self.modification_date = XSDDate(self.modification_date)

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        if not isinstance(self.provenance, list):
            self.provenance = [self.provenance] if self.provenance is not None else []
        self.provenance = [v if isinstance(v, ProvenanceStatement) else ProvenanceStatement(**as_dict(v)) for v in self.provenance]

        if self.publisher is not None and not isinstance(self.publisher, Agent):
            self.publisher = Agent(**as_dict(self.publisher))

        if not isinstance(self.qualified_attribution, list):
            self.qualified_attribution = [self.qualified_attribution] if self.qualified_attribution is not None else []
        self.qualified_attribution = [v if isinstance(v, Attribution) else Attribution(**as_dict(v)) for v in self.qualified_attribution]

        if not isinstance(self.qualified_relation, list):
            self.qualified_relation = [self.qualified_relation] if self.qualified_relation is not None else []
        self.qualified_relation = [v if isinstance(v, Relationship) else Relationship(**as_dict(v)) for v in self.qualified_relation]

        self._normalize_inlined_as_list(slot_name="related_resource", slot_type=Resource, key_name="id", keyed=True)

        if self.release_date is not None and not isinstance(self.release_date, XSDDate):
            self.release_date = XSDDate(self.release_date)

        if not isinstance(self.sample, list):
            self.sample = [self.sample] if self.sample is not None else []
        self.sample = [v if isinstance(v, Distribution) else Distribution(**as_dict(v)) for v in self.sample]

        self._normalize_inlined_as_list(slot_name="source", slot_type=Dataset, key_name="id", keyed=True)

        if self.spatial_resolution is not None and not isinstance(self.spatial_resolution, Decimal):
            self.spatial_resolution = Decimal(self.spatial_resolution)

        if not isinstance(self.temporal_coverage, list):
            self.temporal_coverage = [self.temporal_coverage] if self.temporal_coverage is not None else []
        self.temporal_coverage = [v if isinstance(v, PeriodOfTime) else PeriodOfTime(**as_dict(v)) for v in self.temporal_coverage]

        if self.temporal_resolution is not None and not isinstance(self.temporal_resolution, str):
            self.temporal_resolution = str(self.temporal_resolution)

        self._normalize_inlined_as_list(slot_name="theme", slot_type=Concept, key_name="preferred_label", keyed=False)

        self._normalize_inlined_as_list(slot_name="type", slot_type=Concept, key_name="preferred_label", keyed=False)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.version_notes, list):
            self.version_notes = [self.version_notes] if self.version_notes is not None else []
        self.version_notes = [v if isinstance(v, str) else str(v) for v in self.version_notes]

        self._normalize_inlined_as_list(slot_name="is_about_entity", slot_type=EvaluatedEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="is_about_activity", slot_type=EvaluatedActivity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnalysisDataset(Dataset):
    """
    A Dataset that was generated by an analysis of some previously generated data. For example, a dataset that
    contains the data of an assignment of a chemical structure to a sample based on the spectral data obtained from
    the sample is an AnalyticalDataset.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Dataset"]
    class_class_curie: ClassVar[str] = "dcat:Dataset"
    class_name: ClassVar[str] = "AnalysisDataset"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.AnalysisDataset

    id: Union[str, AnalysisDatasetId] = None
    description: Union[str, list[str]] = None
    title: Union[str, list[str]] = None
    was_generated_by: Optional[Union[dict[Union[str, DataAnalysisId], Union[dict, DataAnalysis]], list[Union[dict, DataAnalysis]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnalysisDatasetId):
            self.id = AnalysisDatasetId(self.id)

        self._normalize_inlined_as_list(slot_name="was_generated_by", slot_type=DataAnalysis, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DatasetSeries(YAMLRoot):
    """
    See [DCAT-AP specs:DatasetSeries](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#DatasetSeries)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["DatasetSeries"]
    class_class_curie: ClassVar[str] = "dcat:DatasetSeries"
    class_name: ClassVar[str] = "DatasetSeries"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.DatasetSeries

    description: Union[str, list[str]] = None
    title: Union[str, list[str]] = None
    applicable_legislation: Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]] = empty_dict()
    contact_point: Optional[Union[Union[dict, "Kind"], list[Union[dict, "Kind"]]]] = empty_list()
    frequency: Optional[Union[dict, "Frequency"]] = None
    geographical_coverage: Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]] = empty_list()
    modification_date: Optional[Union[str, XSDDate]] = None
    publisher: Optional[Union[dict, Agent]] = None
    release_date: Optional[Union[str, XSDDate]] = None
    temporal_coverage: Optional[Union[Union[dict, "PeriodOfTime"], list[Union[dict, "PeriodOfTime"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        if not isinstance(self.contact_point, list):
            self.contact_point = [self.contact_point] if self.contact_point is not None else []
        self.contact_point = [v if isinstance(v, Kind) else Kind(**as_dict(v)) for v in self.contact_point]

        if self.frequency is not None and not isinstance(self.frequency, Frequency):
            self.frequency = Frequency(**as_dict(self.frequency))

        if not isinstance(self.geographical_coverage, list):
            self.geographical_coverage = [self.geographical_coverage] if self.geographical_coverage is not None else []
        self.geographical_coverage = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.geographical_coverage]

        if self.modification_date is not None and not isinstance(self.modification_date, XSDDate):
            self.modification_date = XSDDate(self.modification_date)

        if self.publisher is not None and not isinstance(self.publisher, Agent):
            self.publisher = Agent(**as_dict(self.publisher))

        if self.release_date is not None and not isinstance(self.release_date, XSDDate):
            self.release_date = XSDDate(self.release_date)

        if not isinstance(self.temporal_coverage, list):
            self.temporal_coverage = [self.temporal_coverage] if self.temporal_coverage is not None else []
        self.temporal_coverage = [v if isinstance(v, PeriodOfTime) else PeriodOfTime(**as_dict(v)) for v in self.temporal_coverage]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DefinedTerm(YAMLRoot):
    """
    A word, name, acronym or phrase that is defined in a controlled vocabulary (CV) and that is used to provide an
    additional rdf:type or dcterms:type of a class within this schema.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["DefinedTerm"]
    class_class_curie: ClassVar[str] = "schema:DefinedTerm"
    class_name: ClassVar[str] = "DefinedTerm"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.DefinedTerm

    id: Union[str, DefinedTermId] = None
    title: Optional[str] = None
    from_CV: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DefinedTermId):
            self.id = DefinedTermId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.from_CV is not None and not isinstance(self.from_CV, URIorCURIE):
            self.from_CV = URIorCURIE(self.from_CV)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Device(AgenticEntity):
    """
    A material instrument that is designed to perform a function primarily by means of its mechanical or electrical
    nature.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Agent"]
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "Device"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Device

    id: Union[str, DeviceId] = None
    has_part: Optional[Union[dict[Union[str, DeviceId], Union[dict, "Device"]], list[Union[dict, "Device"]]]] = empty_dict()
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DeviceId):
            self.id = DeviceId(self.id)

        self._normalize_inlined_as_list(slot_name="has_part", slot_type=Device, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Distribution(YAMLRoot):
    """
    See [DCAT-AP specs:Distribution](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Distribution)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Distribution"]
    class_class_curie: ClassVar[str] = "dcat:Distribution"
    class_name: ClassVar[str] = "Distribution"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Distribution

    access_URL: Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]] = empty_dict()
    access_service: Optional[Union[Union[dict, DataService], list[Union[dict, DataService]]]] = empty_list()
    applicable_legislation: Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]] = empty_dict()
    availability: Optional[Union[dict, "Concept"]] = None
    byte_size: Optional[int] = None
    checksum: Optional[Union[dict, Checksum]] = None
    compression_format: Optional[Union[dict, "MediaType"]] = None
    description: Optional[Union[str, list[str]]] = empty_list()
    documentation: Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]] = empty_dict()
    download_URL: Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]] = empty_dict()
    format: Optional[Union[dict, "MediaTypeOrExtent"]] = None
    has_policy: Optional[Union[dict, "Policy"]] = None
    language: Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]] = empty_list()
    licence: Optional[Union[dict, "LicenseDocument"]] = None
    linked_schemas: Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]] = empty_list()
    media_type: Optional[Union[dict, "MediaType"]] = None
    modification_date: Optional[Union[str, XSDDate]] = None
    packaging_format: Optional[Union[dict, "MediaType"]] = None
    release_date: Optional[Union[str, XSDDate]] = None
    rights: Optional[Union[dict, "RightsStatement"]] = None
    spatial_resolution: Optional[Decimal] = None
    status: Optional[Union[dict, "Concept"]] = None
    temporal_resolution: Optional[str] = None
    title: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.access_URL):
            self.MissingRequiredField("access_URL")
        self._normalize_inlined_as_list(slot_name="access_URL", slot_type=Resource, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="access_service", slot_type=DataService, key_name="title", keyed=False)

        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        if self.availability is not None and not isinstance(self.availability, Concept):
            self.availability = Concept(**as_dict(self.availability))

        if self.byte_size is not None and not isinstance(self.byte_size, int):
            self.byte_size = int(self.byte_size)

        if self.checksum is not None and not isinstance(self.checksum, Checksum):
            self.checksum = Checksum(**as_dict(self.checksum))

        if self.compression_format is not None and not isinstance(self.compression_format, MediaType):
            self.compression_format = MediaType(**as_dict(self.compression_format))

        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        self._normalize_inlined_as_list(slot_name="documentation", slot_type=Document, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="download_URL", slot_type=Resource, key_name="id", keyed=True)

        if self.format is not None and not isinstance(self.format, MediaTypeOrExtent):
            self.format = MediaTypeOrExtent(**as_dict(self.format))

        if self.has_policy is not None and not isinstance(self.has_policy, Policy):
            self.has_policy = Policy(**as_dict(self.has_policy))

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, LinguisticSystem) else LinguisticSystem(**as_dict(v)) for v in self.language]

        if self.licence is not None and not isinstance(self.licence, LicenseDocument):
            self.licence = LicenseDocument(**as_dict(self.licence))

        if not isinstance(self.linked_schemas, list):
            self.linked_schemas = [self.linked_schemas] if self.linked_schemas is not None else []
        self.linked_schemas = [v if isinstance(v, Standard) else Standard(**as_dict(v)) for v in self.linked_schemas]

        if self.media_type is not None and not isinstance(self.media_type, MediaType):
            self.media_type = MediaType(**as_dict(self.media_type))

        if self.modification_date is not None and not isinstance(self.modification_date, XSDDate):
            self.modification_date = XSDDate(self.modification_date)

        if self.packaging_format is not None and not isinstance(self.packaging_format, MediaType):
            self.packaging_format = MediaType(**as_dict(self.packaging_format))

        if self.release_date is not None and not isinstance(self.release_date, XSDDate):
            self.release_date = XSDDate(self.release_date)

        if self.rights is not None and not isinstance(self.rights, RightsStatement):
            self.rights = RightsStatement(**as_dict(self.rights))

        if self.spatial_resolution is not None and not isinstance(self.spatial_resolution, Decimal):
            self.spatial_resolution = Decimal(self.spatial_resolution)

        if self.status is not None and not isinstance(self.status, Concept):
            self.status = Concept(**as_dict(self.status))

        if self.temporal_resolution is not None and not isinstance(self.temporal_resolution, str):
            self.temporal_resolution = str(self.temporal_resolution)

        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Entity(YAMLRoot):
    """
    A physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Entity"]
    class_class_curie: ClassVar[str] = "prov:Entity"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Entity

    id: Union[str, EntityId] = None
    title: Optional[str] = None
    description: Optional[str] = None
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()
    has_qualitative_attribute: Optional[Union[Union[dict, "QualitativeAttribute"], list[Union[dict, "QualitativeAttribute"]]]] = empty_list()
    has_quantitative_attribute: Optional[Union[Union[dict, "QuantitativeAttribute"], list[Union[dict, "QuantitativeAttribute"]]]] = empty_list()
    has_part: Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]] = empty_dict()
    part_of: Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]] = empty_dict()
    type: Optional[Union[dict, DefinedTerm]] = None
    rdf_type: Optional[Union[dict, DefinedTerm]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EntityId):
            self.id = EntityId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_qualitative_attribute", slot_type=QualitativeAttribute, key_name="value", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_quantitative_attribute", slot_type=QuantitativeAttribute, key_name="value", keyed=False)

        self._normalize_inlined_as_list(slot_name="has_part", slot_type=Entity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="part_of", slot_type=Entity, key_name="id", keyed=True)

        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EvaluatedActivity(Activity):
    """
    An activity or process that is being evaluated in a DataGeneratingActivity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "EvaluatedActivity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.EvaluatedActivity

    id: Union[str, EvaluatedActivityId] = None
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EvaluatedActivityId):
            self.id = EvaluatedActivityId(self.id)

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EvaluatedEntity(Entity):
    """
    An Entity that is being evaluated in a DataGeneratingActivity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Entity"]
    class_class_curie: ClassVar[str] = "prov:Entity"
    class_name: ClassVar[str] = "EvaluatedEntity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.EvaluatedEntity

    id: Union[str, EvaluatedEntityId] = None
    was_generated_by: Optional[Union[dict[Union[str, ActivityId], Union[dict, Activity]], list[Union[dict, Activity]]]] = empty_dict()
    title: Optional[str] = None
    description: Optional[str] = None
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EvaluatedEntityId):
            self.id = EvaluatedEntityId(self.id)

        self._normalize_inlined_as_list(slot_name="was_generated_by", slot_type=Activity, key_name="id", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        __post_init_shield = {n: getattr(self, n) for n in ("was_generated_by",)}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class AnalysisSourceData(EvaluatedEntity):
    """
    Information that was evaluated within a DataAnalysis.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Entity"]
    class_class_curie: ClassVar[str] = "prov:Entity"
    class_name: ClassVar[str] = "AnalysisSourceData"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.AnalysisSourceData

    id: Union[str, AnalysisSourceDataId] = None
    was_generated_by: Optional[Union[dict[Union[str, DataGeneratingActivityId], Union[dict, DataGeneratingActivity]], list[Union[dict, DataGeneratingActivity]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnalysisSourceDataId):
            self.id = AnalysisSourceDataId(self.id)

        self._normalize_inlined_as_list(slot_name="was_generated_by", slot_type=DataGeneratingActivity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


class Kind(YAMLRoot):
    """
    See [DCAT-AP specs:Kind](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Kind)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VCARD["Kind"]
    class_class_curie: ClassVar[str] = "vcard:Kind"
    class_name: ClassVar[str] = "Kind"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Kind


@dataclass(repr=False)
class Location(YAMLRoot):
    """
    See [DCAT-AP specs:Location](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Location)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["Location"]
    class_class_curie: ClassVar[str] = "dcterms:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Location

    bbox: Optional[str] = None
    centroid: Optional[str] = None
    geometry: Optional[Union[dict, "Geometry"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.bbox is not None and not isinstance(self.bbox, str):
            self.bbox = str(self.bbox)

        if self.centroid is not None and not isinstance(self.centroid, str):
            self.centroid = str(self.centroid)

        if self.geometry is not None and not isinstance(self.geometry, Geometry):
            self.geometry = Geometry(**as_dict(self.geometry))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Plan(YAMLRoot):
    """
    A piece of information that specifies how an activity has to be carried out by its agents including what kind of
    steps have to be taken and what kind of parameters have to be met/set.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Plan"]
    class_class_curie: ClassVar[str] = "prov:Plan"
    class_name: ClassVar[str] = "Plan"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Plan

    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Union[dict, DefinedTerm]] = None
    rdf_type: Optional[Union[dict, DefinedTerm]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QualitativeAttribute(YAMLRoot):
    """
    A piece of information that is attributed to an Entity, Activity or AgenticEntity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Entity"]
    class_class_curie: ClassVar[str] = "prov:Entity"
    class_name: ClassVar[str] = "QualitativeAttribute"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.QualitativeAttribute

    value: str = None
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Union[dict, DefinedTerm]] = None
    rdf_type: Optional[Union[dict, DefinedTerm]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuantitativeAttribute(YAMLRoot):
    """
    A quantifiable piece of information that is attributed to an Entity, Activity or AgenticEntity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = QUDT["Quantity"]
    class_class_curie: ClassVar[str] = "qudt:Quantity"
    class_name: ClassVar[str] = "QuantitativeAttribute"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.QuantitativeAttribute

    value: float = None
    has_quantity_type: Union[str, DefinedTermId] = None
    title: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[Union[str, DefinedTermId]] = None
    type: Optional[Union[dict, DefinedTerm]] = None
    rdf_type: Optional[Union[dict, DefinedTerm]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, float):
            self.value = float(self.value)

        if self._is_empty(self.has_quantity_type):
            self.MissingRequiredField("has_quantity_type")
        if not isinstance(self.has_quantity_type, DefinedTermId):
            self.has_quantity_type = DefinedTermId(self.has_quantity_type)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.unit is not None and not isinstance(self.unit, DefinedTermId):
            self.unit = DefinedTermId(self.unit)

        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Relationship(YAMLRoot):
    """
    See [DCAT-AP specs:Relationship](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Relationship)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Relationship"]
    class_class_curie: ClassVar[str] = "dcat:Relationship"
    class_name: ClassVar[str] = "Relationship"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Relationship

    had_role: Union[Union[dict, "Role"], list[Union[dict, "Role"]]] = None
    relation: Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.had_role):
            self.MissingRequiredField("had_role")
        if not isinstance(self.had_role, list):
            self.had_role = [self.had_role] if self.had_role is not None else []
        self.had_role = [v if isinstance(v, Role) else Role(**as_dict(v)) for v in self.had_role]

        if self._is_empty(self.relation):
            self.MissingRequiredField("relation")
        self._normalize_inlined_as_list(slot_name="relation", slot_type=Resource, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Software(AgenticEntity):
    """
    An instrument composed of a series of instructions that can be interpreted by or directly executed by a computer.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["SoftwareAgent"]
    class_class_curie: ClassVar[str] = "prov:SoftwareAgent"
    class_name: ClassVar[str] = "Software"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Software

    id: Union[str, SoftwareId] = None
    has_part: Optional[Union[dict[Union[str, SoftwareId], Union[dict, "Software"]], list[Union[dict, "Software"]]]] = empty_dict()
    other_identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SoftwareId):
            self.id = SoftwareId(self.id)

        self._normalize_inlined_as_list(slot_name="has_part", slot_type=Software, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="other_identifier", slot_type=Identifier, key_name="notation", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SupportiveEntity(YAMLRoot):
    """
    The supportive entities are supporting the main entities in the Application Profile. They are included in the
    Application Profile because they form the range of properties.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCATAPPLUS["SupportiveEntity"]
    class_class_curie: ClassVar[str] = "dcatapplus:SupportiveEntity"
    class_name: ClassVar[str] = "SupportiveEntity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.SupportiveEntity

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Association(SupportiveEntity):
    """
    The qualified form of prov:wasAssociatedWith (what carried_out_by already shortcuts to, on
    DataGeneratingActivity/Activity) -- PROV-O's own Activity-side counterpart to Attribution's Entity-side
    qualification. dcat-ap-plus has no Association class at all (a bigger gap than Attribution, which at least has a
    title/description stub) -- confirmed absent from its schema, not assumed.
    This class, and the ready-to-use qualified_association slot below (already correctly ranged at Association), are
    built here even though this repo's own port never touches the Activity side at all (HealthDCAT-AP's SHACL doesn't
    reach it -- confirmed in Section 1 Check b of architecture-verification.md) and there's no Health<X> profile of
    Activity to narrow anything onto: this is exactly the kind of generic, domain-agnostic completion the merge layer
    exists to provide, so the downstream specialization repo gets a schema it only has to specialize, not one it has
    to finish first.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Association"]
    class_class_curie: ClassVar[str] = "prov:Association"
    class_name: ClassVar[str] = "Association"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Association

    agent: Union[dict, AgenticEntity] = None
    association_had_role: Union[str, URIorCURIE] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.agent):
            self.MissingRequiredField("agent")
        if not isinstance(self.agent, AgenticEntity):
            self.agent = AgenticEntity(**as_dict(self.agent))

        if self._is_empty(self.association_had_role):
            self.MissingRequiredField("association_had_role")
        if not isinstance(self.association_had_role, URIorCURIE):
            self.association_had_role = URIorCURIE(self.association_had_role)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Attribution(SupportiveEntity):
    """
    See [DCAT-AP specs:Attribution](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Attribution)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Attribution"]
    class_class_curie: ClassVar[str] = "prov:Attribution"
    class_name: ClassVar[str] = "Attribution"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Attribution

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ChecksumAlgorithm(SupportiveEntity):
    """
    See [DCAT-AP specs:ChecksumAlgorithm](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#ChecksumAlgorithm)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SPDX["ChecksumAlgorithm"]
    class_class_curie: ClassVar[str] = "spdx:ChecksumAlgorithm"
    class_name: ClassVar[str] = "ChecksumAlgorithm"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.ChecksumAlgorithm

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Concept(SupportiveEntity):
    """
    See [DCAT-AP specs:Concept](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Concept)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Concept

    preferred_label: Union[str, list[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.preferred_label):
            self.MissingRequiredField("preferred_label")
        if not isinstance(self.preferred_label, list):
            self.preferred_label = [self.preferred_label] if self.preferred_label is not None else []
        self.preferred_label = [v if isinstance(v, str) else str(v) for v in self.preferred_label]

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        __post_init_shield = {n: getattr(self, n) for n in ("preferred_label",)}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class ConceptScheme(SupportiveEntity):
    """
    See [DCAT-AP specs:ConceptScheme](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#ConceptScheme)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["ConceptScheme"]
    class_class_curie: ClassVar[str] = "skos:ConceptScheme"
    class_name: ClassVar[str] = "ConceptScheme"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.ConceptScheme

    title: Union[str, list[str]] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        __post_init_shield = {n: getattr(self, n) for n in ("title",)}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class Document(SupportiveEntity):
    """
    See [DCAT-AP specs:Document](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Document)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Document"]
    class_class_curie: ClassVar[str] = "foaf:Document"
    class_name: ClassVar[str] = "Document"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Document

    id: Union[str, DocumentId] = None
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DocumentId):
            self.id = DocumentId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Frequency(SupportiveEntity):
    """
    See [DCAT-AP specs:Frequency](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Frequency)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["Frequency"]
    class_class_curie: ClassVar[str] = "dcterms:Frequency"
    class_name: ClassVar[str] = "Frequency"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Frequency

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Geometry(SupportiveEntity):
    """
    See [DCAT-AP specs:Geometry](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Geometry)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LOCN["Geometry"]
    class_class_curie: ClassVar[str] = "locn:Geometry"
    class_name: ClassVar[str] = "Geometry"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Geometry

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Identifier(SupportiveEntity):
    """
    See [DCAT-AP specs:Identifier](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Identifier)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ADMS["Identifier"]
    class_class_curie: ClassVar[str] = "adms:Identifier"
    class_name: ClassVar[str] = "Identifier"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Identifier

    notation: str = None
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.notation):
            self.MissingRequiredField("notation")
        if not isinstance(self.notation, str):
            self.notation = str(self.notation)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LegalResource(SupportiveEntity):
    """
    See [DCAT-AP specs:LegalResource](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#LegalResource)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ELI["LegalResource"]
    class_class_curie: ClassVar[str] = "eli:LegalResource"
    class_name: ClassVar[str] = "LegalResource"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.LegalResource

    id: Union[str, LegalResourceId] = None
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LegalResourceId):
            self.id = LegalResourceId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LicenseDocument(SupportiveEntity):
    """
    See [DCAT-AP specs:LicenseDocument](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#LicenseDocument)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["LicenseDocument"]
    class_class_curie: ClassVar[str] = "dcterms:LicenseDocument"
    class_name: ClassVar[str] = "LicenseDocument"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.LicenseDocument

    id: Union[str, LicenseDocumentId] = None
    type: Optional[Union[Union[dict, Concept], list[Union[dict, Concept]]]] = empty_list()
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LicenseDocumentId):
            self.id = LicenseDocumentId(self.id)

        self._normalize_inlined_as_list(slot_name="type", slot_type=Concept, key_name="preferred_label", keyed=False)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        __post_init_shield = {n: getattr(self, n) for n in ("type",)}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class LinguisticSystem(SupportiveEntity):
    """
    See [DCAT-AP specs:LinguisticSystem](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#LinguisticSystem)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["LinguisticSystem"]
    class_class_curie: ClassVar[str] = "dcterms:LinguisticSystem"
    class_name: ClassVar[str] = "LinguisticSystem"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.LinguisticSystem

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MediaType(SupportiveEntity):
    """
    See [DCAT-AP specs:MediaType](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#MediaType)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["MediaType"]
    class_class_curie: ClassVar[str] = "dcterms:MediaType"
    class_name: ClassVar[str] = "MediaType"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.MediaType

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MediaTypeOrExtent(SupportiveEntity):
    """
    See [DCAT-AP specs:MediaTypeOrExtent](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#MediaTypeOrExtent)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["MediaTypeOrExtent"]
    class_class_curie: ClassVar[str] = "dcterms:MediaTypeOrExtent"
    class_name: ClassVar[str] = "MediaTypeOrExtent"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.MediaTypeOrExtent

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PeriodOfTime(SupportiveEntity):
    """
    See [DCAT-AP specs:PeriodOfTime](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#PeriodOfTime)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["PeriodOfTime"]
    class_class_curie: ClassVar[str] = "dcterms:PeriodOfTime"
    class_name: ClassVar[str] = "PeriodOfTime"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.PeriodOfTime

    beginning: Optional[Union[dict, "TimeInstant"]] = None
    end: Optional[Union[dict, "TimeInstant"]] = None
    end_date: Optional[Union[str, XSDDate]] = None
    start_date: Optional[Union[str, XSDDate]] = None
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.beginning is not None and not isinstance(self.beginning, TimeInstant):
            self.beginning = TimeInstant(**as_dict(self.beginning))

        if self.end is not None and not isinstance(self.end, TimeInstant):
            self.end = TimeInstant(**as_dict(self.end))

        if self.end_date is not None and not isinstance(self.end_date, XSDDate):
            self.end_date = XSDDate(self.end_date)

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        __post_init_shield = {n: getattr(self, n) for n in ("beginning", "end", "end_date", "start_date")}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class Policy(SupportiveEntity):
    """
    See [DCAT-AP specs:Policy](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Policy)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL["Policy"]
    class_class_curie: ClassVar[str] = "odrl:Policy"
    class_name: ClassVar[str] = "Policy"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Policy

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProvenanceStatement(SupportiveEntity):
    """
    See [DCAT-AP specs:ProvenanceStatement](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#ProvenanceStatement)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["ProvenanceStatement"]
    class_class_curie: ClassVar[str] = "dcterms:ProvenanceStatement"
    class_name: ClassVar[str] = "ProvenanceStatement"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.ProvenanceStatement

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Resource(SupportiveEntity):
    """
    See [DCAT-AP specs:Resource](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Resource)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RDFS["Resource"]
    class_class_curie: ClassVar[str] = "rdfs:Resource"
    class_name: ClassVar[str] = "Resource"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Resource

    id: Union[str, ResourceId] = None
    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ResourceId):
            self.id = ResourceId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RightsStatement(SupportiveEntity):
    """
    See [DCAT-AP specs:RightsStatement](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#RightsStatement)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["RightsStatement"]
    class_class_curie: ClassVar[str] = "dcterms:RightsStatement"
    class_name: ClassVar[str] = "RightsStatement"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.RightsStatement

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Role(SupportiveEntity):
    """
    See [DCAT-AP specs:Role](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Role)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Role"]
    class_class_curie: ClassVar[str] = "dcat:Role"
    class_name: ClassVar[str] = "Role"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Role

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Standard(SupportiveEntity):
    """
    See [DCAT-AP specs:Standard](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#Standard)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["Standard"]
    class_class_curie: ClassVar[str] = "dcterms:Standard"
    class_name: ClassVar[str] = "Standard"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Standard

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Surrounding(YAMLRoot):
    """
    The surrounding in which the dataset creating activity took place (e.g. a lab).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Location"]
    class_class_curie: ClassVar[str] = "prov:Location"
    class_name: ClassVar[str] = "Surrounding"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Surrounding

    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Union[dict, DefinedTerm]] = None
    rdf_type: Optional[Union[dict, DefinedTerm]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.type is not None and not isinstance(self.type, DefinedTerm):
            self.type = DefinedTerm(**as_dict(self.type))

        if self.rdf_type is not None and not isinstance(self.rdf_type, DefinedTerm):
            self.rdf_type = DefinedTerm(**as_dict(self.rdf_type))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TimeInstant(SupportiveEntity):
    """
    See [DCAT-AP specs:TimeInstant](https://semiceu.github.io/DCAT-AP/releases/3.0.0/#TimeInstant)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TIME["Instant"]
    class_class_curie: ClassVar[str] = "time:Instant"
    class_name: ClassVar[str] = "TimeInstant"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.TimeInstant

    title: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HealthCatalogue(Catalogue):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Catalog"]
    class_class_curie: ClassVar[str] = "dcat:Catalog"
    class_name: ClassVar[str] = "HealthCatalogue"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthCatalogue

    description: Union[str, list[str]] = None
    title: Union[str, list[str]] = None
    applicable_legislation: Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]] = empty_dict()
    publisher: Union[str, URIorCURIE] = None
    language: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    geographical_coverage: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.applicable_legislation):
            self.MissingRequiredField("applicable_legislation")
        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        if self._is_empty(self.publisher):
            self.MissingRequiredField("publisher")
        if not isinstance(self.publisher, URIorCURIE):
            self.publisher = URIorCURIE(self.publisher)

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.language]

        if not isinstance(self.geographical_coverage, list):
            self.geographical_coverage = [self.geographical_coverage] if self.geographical_coverage is not None else []
        self.geographical_coverage = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.geographical_coverage]

        __post_init_shield = {n: getattr(self, n) for n in ("language", "publisher", "geographical_coverage")}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class Column(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CSVW["Column"]
    class_class_curie: ClassVar[str] = "csvw:Column"
    class_name: ClassVar[str] = "Column"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Column

    datatype: str = None
    description: Union[str, list[str]] = None
    name: Union[str, list[str]] = None
    titles: Union[str, list[str]] = None
    property_url: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.datatype):
            self.MissingRequiredField("datatype")
        if not isinstance(self.datatype, str):
            self.datatype = str(self.datatype)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, list):
            self.name = [self.name] if self.name is not None else []
        self.name = [v if isinstance(v, str) else str(v) for v in self.name]

        if self._is_empty(self.titles):
            self.MissingRequiredField("titles")
        if not isinstance(self.titles, list):
            self.titles = [self.titles] if self.titles is not None else []
        self.titles = [v if isinstance(v, str) else str(v) for v in self.titles]

        if self.property_url is not None and not isinstance(self.property_url, str):
            self.property_url = str(self.property_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContactPoint(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CV["ContactPoint"]
    class_class_curie: ClassVar[str] = "cv:ContactPoint"
    class_name: ClassVar[str] = "ContactPoint"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.ContactPoint

    contact_page: Optional[Union[str, list[str]]] = empty_list()
    email: Optional[Union[str, list[str]]] = empty_list()
    opening_hours: Optional[Union[Union[dict, "TemporalEntity"], list[Union[dict, "TemporalEntity"]]]] = empty_list()
    special_opening_hours_specification: Optional[Union[Union[dict, "TemporalEntity"], list[Union[dict, "TemporalEntity"]]]] = empty_list()
    telephone: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.contact_page, list):
            self.contact_page = [self.contact_page] if self.contact_page is not None else []
        self.contact_page = [v if isinstance(v, str) else str(v) for v in self.contact_page]

        if not isinstance(self.email, list):
            self.email = [self.email] if self.email is not None else []
        self.email = [v if isinstance(v, str) else str(v) for v in self.email]

        self._normalize_inlined_as_list(slot_name="opening_hours", slot_type=TemporalEntity, key_name="description", keyed=False)

        self._normalize_inlined_as_list(slot_name="special_opening_hours_specification", slot_type=TemporalEntity, key_name="description", keyed=False)

        if not isinstance(self.telephone, list):
            self.telephone = [self.telephone] if self.telephone is not None else []
        self.telephone = [v if isinstance(v, str) else str(v) for v in self.telephone]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HealthDataset(Dataset):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Dataset"]
    class_class_curie: ClassVar[str] = "dcat:Dataset"
    class_name: ClassVar[str] = "HealthDataset"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthDataset

    id: Union[str, HealthDatasetId] = None
    description: Union[str, list[str]] = None
    title: Union[str, list[str]] = None
    was_generated_by: Union[dict[Union[str, DataGeneratingActivityId], Union[dict, DataGeneratingActivity]], list[Union[dict, DataGeneratingActivity]]] = empty_dict()
    has_structured_data: Union[bool, Bool] = None
    hdab: Union[dict, "HealthAgent"] = None
    health_category: Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]] = None
    access_rights: Union[str, URIorCURIE] = None
    applicable_legislation: Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]] = empty_dict()
    dataset_distribution: Union[Union[dict, "HealthDistribution"], list[Union[dict, "HealthDistribution"]]] = None
    identifier: Union[str, list[str]] = None
    theme: Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]] = None
    contact_point: Union[Union[dict, "HealthKind"], list[Union[dict, "HealthKind"]]] = None
    keyword: Union[str, list[str]] = None
    type: Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]] = None
    provenance: Union[Union[dict, ProvenanceStatement], list[Union[dict, ProvenanceStatement]]] = None
    alternative: Optional[Union[str, list[str]]] = empty_list()
    analytics: Optional[Union[Union[dict, "HealthDistribution"], list[Union[dict, "HealthDistribution"]]]] = empty_list()
    custodian: Optional[Union[dict, "HealthAgent"]] = None
    has_code_values: Optional[Union[str, list[str]]] = empty_list()
    has_coding_system: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    has_legal_basis: Optional[Union[Union[str, LegalBasisId], list[Union[str, LegalBasisId]]]] = empty_list()
    has_personal_data: Optional[Union[Union[str, PersonalDataId], list[Union[str, PersonalDataId]]]] = empty_list()
    has_purpose: Optional[Union[Union[str, PurposeId], list[Union[str, PurposeId]]]] = empty_list()
    has_quality_annotation: Optional[Union[Union[str, QualityCertificateId], list[Union[str, QualityCertificateId]]]] = empty_list()
    has_variables: Optional[Union[Union[dict, "TableGroup"], list[Union[dict, "TableGroup"]]]] = empty_list()
    health_theme: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    max_typical_age: Optional[int] = None
    min_typical_age: Optional[int] = None
    number_of_records: Optional[int] = None
    number_of_unique_individuals: Optional[int] = None
    population_coverage: Optional[Union[str, list[str]]] = empty_list()
    retention_period: Optional[Union[dict, PeriodOfTime]] = None
    publisher: Optional[Union[dict, "HealthPublisherAgent"]] = None
    sample: Optional[Union[Union[dict, "HealthDistribution"], list[Union[dict, "HealthDistribution"]]]] = empty_list()
    frequency: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    source: Optional[Union[dict[Union[str, HealthDatasetId], Union[dict, "HealthDataset"]], list[Union[dict, "HealthDataset"]]]] = empty_dict()
    temporal_resolution: Optional[Union[str, list[str]]] = empty_list()
    language: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    geographical_coverage: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    conforms_to: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    qualified_attribution: Optional[Union[Union[dict, "DatasetAttribution"], list[Union[dict, "DatasetAttribution"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, HealthDatasetId):
            self.id = HealthDatasetId(self.id)

        if self._is_empty(self.has_structured_data):
            self.MissingRequiredField("has_structured_data")
        if not isinstance(self.has_structured_data, Bool):
            self.has_structured_data = Bool(self.has_structured_data)

        if self._is_empty(self.hdab):
            self.MissingRequiredField("hdab")
        if not isinstance(self.hdab, HealthAgent):
            self.hdab = HealthAgent(**as_dict(self.hdab))

        if self._is_empty(self.health_category):
            self.MissingRequiredField("health_category")
        if not isinstance(self.health_category, list):
            self.health_category = [self.health_category] if self.health_category is not None else []
        self.health_category = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.health_category]

        if self._is_empty(self.access_rights):
            self.MissingRequiredField("access_rights")
        if not isinstance(self.access_rights, URIorCURIE):
            self.access_rights = URIorCURIE(self.access_rights)

        if self._is_empty(self.applicable_legislation):
            self.MissingRequiredField("applicable_legislation")
        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        if self._is_empty(self.dataset_distribution):
            self.MissingRequiredField("dataset_distribution")
        if not isinstance(self.dataset_distribution, list):
            self.dataset_distribution = [self.dataset_distribution] if self.dataset_distribution is not None else []
        self.dataset_distribution = [v if isinstance(v, HealthDistribution) else HealthDistribution(**as_dict(v)) for v in self.dataset_distribution]

        if self._is_empty(self.identifier):
            self.MissingRequiredField("identifier")
        if not isinstance(self.identifier, list):
            self.identifier = [self.identifier] if self.identifier is not None else []
        self.identifier = [v if isinstance(v, str) else str(v) for v in self.identifier]

        if self._is_empty(self.theme):
            self.MissingRequiredField("theme")
        if not isinstance(self.theme, list):
            self.theme = [self.theme] if self.theme is not None else []
        self.theme = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.theme]

        if self._is_empty(self.contact_point):
            self.MissingRequiredField("contact_point")
        if not isinstance(self.contact_point, list):
            self.contact_point = [self.contact_point] if self.contact_point is not None else []
        self.contact_point = [v if isinstance(v, HealthKind) else HealthKind(**as_dict(v)) for v in self.contact_point]

        if self._is_empty(self.keyword):
            self.MissingRequiredField("keyword")
        if not isinstance(self.keyword, list):
            self.keyword = [self.keyword] if self.keyword is not None else []
        self.keyword = [v if isinstance(v, str) else str(v) for v in self.keyword]

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, list):
            self.type = [self.type] if self.type is not None else []
        self.type = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.type]

        if self._is_empty(self.provenance):
            self.MissingRequiredField("provenance")
        if not isinstance(self.provenance, list):
            self.provenance = [self.provenance] if self.provenance is not None else []
        self.provenance = [v if isinstance(v, ProvenanceStatement) else ProvenanceStatement(**as_dict(v)) for v in self.provenance]

        if not isinstance(self.alternative, list):
            self.alternative = [self.alternative] if self.alternative is not None else []
        self.alternative = [v if isinstance(v, str) else str(v) for v in self.alternative]

        if not isinstance(self.analytics, list):
            self.analytics = [self.analytics] if self.analytics is not None else []
        self.analytics = [v if isinstance(v, HealthDistribution) else HealthDistribution(**as_dict(v)) for v in self.analytics]

        if self.custodian is not None and not isinstance(self.custodian, HealthAgent):
            self.custodian = HealthAgent(**as_dict(self.custodian))

        if not isinstance(self.has_code_values, list):
            self.has_code_values = [self.has_code_values] if self.has_code_values is not None else []
        self.has_code_values = [v if isinstance(v, str) else str(v) for v in self.has_code_values]

        if not isinstance(self.has_coding_system, list):
            self.has_coding_system = [self.has_coding_system] if self.has_coding_system is not None else []
        self.has_coding_system = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.has_coding_system]

        if not isinstance(self.has_legal_basis, list):
            self.has_legal_basis = [self.has_legal_basis] if self.has_legal_basis is not None else []
        self.has_legal_basis = [v if isinstance(v, LegalBasisId) else LegalBasisId(v) for v in self.has_legal_basis]

        if not isinstance(self.has_personal_data, list):
            self.has_personal_data = [self.has_personal_data] if self.has_personal_data is not None else []
        self.has_personal_data = [v if isinstance(v, PersonalDataId) else PersonalDataId(v) for v in self.has_personal_data]

        if not isinstance(self.has_purpose, list):
            self.has_purpose = [self.has_purpose] if self.has_purpose is not None else []
        self.has_purpose = [v if isinstance(v, PurposeId) else PurposeId(v) for v in self.has_purpose]

        if not isinstance(self.has_quality_annotation, list):
            self.has_quality_annotation = [self.has_quality_annotation] if self.has_quality_annotation is not None else []
        self.has_quality_annotation = [v if isinstance(v, QualityCertificateId) else QualityCertificateId(v) for v in self.has_quality_annotation]

        if not isinstance(self.has_variables, list):
            self.has_variables = [self.has_variables] if self.has_variables is not None else []
        self.has_variables = [v if isinstance(v, TableGroup) else TableGroup(**as_dict(v)) for v in self.has_variables]

        if not isinstance(self.health_theme, list):
            self.health_theme = [self.health_theme] if self.health_theme is not None else []
        self.health_theme = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.health_theme]

        if self.max_typical_age is not None and not isinstance(self.max_typical_age, int):
            self.max_typical_age = int(self.max_typical_age)

        if self.min_typical_age is not None and not isinstance(self.min_typical_age, int):
            self.min_typical_age = int(self.min_typical_age)

        if self.number_of_records is not None and not isinstance(self.number_of_records, int):
            self.number_of_records = int(self.number_of_records)

        if self.number_of_unique_individuals is not None and not isinstance(self.number_of_unique_individuals, int):
            self.number_of_unique_individuals = int(self.number_of_unique_individuals)

        if not isinstance(self.population_coverage, list):
            self.population_coverage = [self.population_coverage] if self.population_coverage is not None else []
        self.population_coverage = [v if isinstance(v, str) else str(v) for v in self.population_coverage]

        if self.retention_period is not None and not isinstance(self.retention_period, PeriodOfTime):
            self.retention_period = PeriodOfTime(**as_dict(self.retention_period))

        if self.publisher is not None and not isinstance(self.publisher, HealthPublisherAgent):
            self.publisher = HealthPublisherAgent(**as_dict(self.publisher))

        if not isinstance(self.sample, list):
            self.sample = [self.sample] if self.sample is not None else []
        self.sample = [v if isinstance(v, HealthDistribution) else HealthDistribution(**as_dict(v)) for v in self.sample]

        if not isinstance(self.frequency, list):
            self.frequency = [self.frequency] if self.frequency is not None else []
        self.frequency = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.frequency]

        self._normalize_inlined_as_list(slot_name="source", slot_type=HealthDataset, key_name="id", keyed=True)

        if not isinstance(self.temporal_resolution, list):
            self.temporal_resolution = [self.temporal_resolution] if self.temporal_resolution is not None else []
        self.temporal_resolution = [v if isinstance(v, str) else str(v) for v in self.temporal_resolution]

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.language]

        if not isinstance(self.geographical_coverage, list):
            self.geographical_coverage = [self.geographical_coverage] if self.geographical_coverage is not None else []
        self.geographical_coverage = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.geographical_coverage]

        if not isinstance(self.conforms_to, list):
            self.conforms_to = [self.conforms_to] if self.conforms_to is not None else []
        self.conforms_to = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.conforms_to]

        self._normalize_inlined_as_list(slot_name="qualified_attribution", slot_type=DatasetAttribution, key_name="attribution_had_role", keyed=False)

        __post_init_shield = {n: getattr(self, n) for n in ("access_rights", "theme", "type", "frequency", "temporal_resolution", "language", "geographical_coverage", "health_category", "has_coding_system", "conforms_to", "health_theme")}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class HealthDatasetSeries(DatasetSeries):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["DatasetSeries"]
    class_class_curie: ClassVar[str] = "dcat:DatasetSeries"
    class_name: ClassVar[str] = "HealthDatasetSeries"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthDatasetSeries

    description: Union[str, list[str]] = None
    title: Union[str, list[str]] = None
    applicable_legislation: Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.applicable_legislation):
            self.MissingRequiredField("applicable_legislation")
        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HealthDistribution(Distribution):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Distribution"]
    class_class_curie: ClassVar[str] = "dcat:Distribution"
    class_name: ClassVar[str] = "HealthDistribution"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthDistribution

    access_URL: Union[dict[Union[str, ResourceId], Union[dict, Resource]], list[Union[dict, Resource]]] = empty_dict()
    applicable_legislation: Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]] = empty_dict()
    format: Optional[Union[str, URIorCURIE]] = None
    language: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    status: Optional[Union[str, URIorCURIE]] = None
    availability: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.applicable_legislation):
            self.MissingRequiredField("applicable_legislation")
        self._normalize_inlined_as_list(slot_name="applicable_legislation", slot_type=LegalResource, key_name="id", keyed=True)

        if self.format is not None and not isinstance(self.format, URIorCURIE):
            self.format = URIorCURIE(self.format)

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.language]

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.availability is not None and not isinstance(self.availability, URIorCURIE):
            self.availability = URIorCURIE(self.availability)

        __post_init_shield = {n: getattr(self, n) for n in ("format", "language", "status", "availability")}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class HealthAgent(Agent):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Agent"]
    class_class_curie: ClassVar[str] = "foaf:Agent"
    class_name: ClassVar[str] = "HealthAgent"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthAgent

    name: Union[str, list[str]] = None
    agent_contact_point: Union[dict, ContactPoint] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.agent_contact_point):
            self.MissingRequiredField("agent_contact_point")
        if not isinstance(self.agent_contact_point, ContactPoint):
            self.agent_contact_point = ContactPoint(**as_dict(self.agent_contact_point))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HealthPublisherAgent(Agent):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Agent"]
    class_class_curie: ClassVar[str] = "foaf:Agent"
    class_name: ClassVar[str] = "HealthPublisherAgent"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthPublisherAgent

    name: Union[str, list[str]] = None
    agent_contact_point: Union[dict, ContactPoint] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.agent_contact_point):
            self.MissingRequiredField("agent_contact_point")
        if not isinstance(self.agent_contact_point, ContactPoint):
            self.agent_contact_point = ContactPoint(**as_dict(self.agent_contact_point))

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HealthKind(Kind):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VCARD["Kind"]
    class_class_curie: ClassVar[str] = "vcard:Kind"
    class_name: ClassVar[str] = "HealthKind"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthKind

    has_email: Optional[str] = None
    has_url: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.has_email is not None and not isinstance(self.has_email, str):
            self.has_email = str(self.has_email)

        if self.has_url is not None and not isinstance(self.has_url, str):
            self.has_url = str(self.has_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Table(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CSVW["Table"]
    class_class_curie: ClassVar[str] = "csvw:Table"
    class_name: ClassVar[str] = "Table"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Table

    column: Union[Union[dict, Column], list[Union[dict, Column]]] = None
    title: Union[str, list[str]] = None
    keyword: Optional[Union[str, list[str]]] = empty_list()
    url: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.column):
            self.MissingRequiredField("column")
        self._normalize_inlined_as_list(slot_name="column", slot_type=Column, key_name="datatype", keyed=False)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, list):
            self.title = [self.title] if self.title is not None else []
        self.title = [v if isinstance(v, str) else str(v) for v in self.title]

        if not isinstance(self.keyword, list):
            self.keyword = [self.keyword] if self.keyword is not None else []
        self.keyword = [v if isinstance(v, str) else str(v) for v in self.keyword]

        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TableGroup(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CSVW["TableGroup"]
    class_class_curie: ClassVar[str] = "csvw:TableGroup"
    class_name: ClassVar[str] = "TableGroup"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.TableGroup

    table: Union[Union[dict, Table], list[Union[dict, Table]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.table):
            self.MissingRequiredField("table")
        self._normalize_inlined_as_list(slot_name="table", slot_type=Table, key_name="title", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TemporalEntity(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TIME["TemporalEntity"]
    class_class_curie: ClassVar[str] = "time:TemporalEntity"
    class_name: ClassVar[str] = "TemporalEntity"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.TemporalEntity

    description: Union[str, list[str]] = None
    frequency: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, list):
            self.description = [self.description] if self.description is not None else []
        self.description = [v if isinstance(v, str) else str(v) for v in self.description]

        if not isinstance(self.frequency, list):
            self.frequency = [self.frequency] if self.frequency is not None else []
        self.frequency = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.frequency]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HealthLicenseDocument(LicenseDocument):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["LicenseDocument"]
    class_class_curie: ClassVar[str] = "dcterms:LicenseDocument"
    class_name: ClassVar[str] = "HealthLicenseDocument"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthLicenseDocument

    id: Union[str, HealthLicenseDocumentId] = None
    type: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, HealthLicenseDocumentId):
            self.id = HealthLicenseDocumentId(self.id)

        if not isinstance(self.type, list):
            self.type = [self.type] if self.type is not None else []
        self.type = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.type]

        __post_init_shield = {n: getattr(self, n) for n in ("type",)}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class HealthDataService(DataService):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["DataService"]
    class_class_curie: ClassVar[str] = "dcat:DataService"
    class_name: ClassVar[str] = "HealthDataService"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.HealthDataService

    endpoint_URL: Union[dict[Union[str, ResourceId], Union[dict, Resource]], list[Union[dict, Resource]]] = empty_dict()
    title: Union[str, list[str]] = None
    access_rights: Optional[Union[str, URIorCURIE]] = None
    format: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.access_rights is not None and not isinstance(self.access_rights, URIorCURIE):
            self.access_rights = URIorCURIE(self.access_rights)

        if not isinstance(self.format, list):
            self.format = [self.format] if self.format is not None else []
        self.format = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.format]

        __post_init_shield = {n: getattr(self, n) for n in ("access_rights", "format")}
        for __n in __post_init_shield:
            setattr(self, __n, None)
        super().__post_init__(**kwargs)
        for __n, __v in __post_init_shield.items():
            setattr(self, __n, __v)


@dataclass(repr=False)
class LegalBasis(YAMLRoot):
    """
    External vocabulary term referenced by a HealthDCAT-AP shape but not itself defined by a sh:NodeShape anywhere in
    HealthDCAT-AP's own release -- confirmed, not assumed: it doesn't appear in the tier shapes files or in
    mdr-vocabularies.shape.ttl (which this port does parse, for controlled-vocabulary bindings on other properties --
    see script docstring); it's a pointer into an external ontology (DPV/DQV) HealthDCAT-AP never embeds. Carries just
    id: real usage is a reference to an external controlled-vocabulary term (e.g. a DPV Purpose/LegalBasis URI), not a
    locally-described object -- and a slotless class can only ever be instantiated as {}, which linkml_runtime's own
    YAML loader rejects outright ('Empty list elements are not allowed'), making a slotless required range unusable in
    practice, not just thin.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["LegalBasis"]
    class_class_curie: ClassVar[str] = "dpv:LegalBasis"
    class_name: ClassVar[str] = "LegalBasis"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.LegalBasis

    id: Union[str, LegalBasisId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LegalBasisId):
            self.id = LegalBasisId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PersonalData(YAMLRoot):
    """
    External vocabulary term referenced by a HealthDCAT-AP shape but not itself defined by a sh:NodeShape anywhere in
    HealthDCAT-AP's own release -- confirmed, not assumed: it doesn't appear in the tier shapes files or in
    mdr-vocabularies.shape.ttl (which this port does parse, for controlled-vocabulary bindings on other properties --
    see script docstring); it's a pointer into an external ontology (DPV/DQV) HealthDCAT-AP never embeds. Carries just
    id: real usage is a reference to an external controlled-vocabulary term (e.g. a DPV Purpose/LegalBasis URI), not a
    locally-described object -- and a slotless class can only ever be instantiated as {}, which linkml_runtime's own
    YAML loader rejects outright ('Empty list elements are not allowed'), making a slotless required range unusable in
    practice, not just thin.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["PersonalData"]
    class_class_curie: ClassVar[str] = "dpv:PersonalData"
    class_name: ClassVar[str] = "PersonalData"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.PersonalData

    id: Union[str, PersonalDataId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonalDataId):
            self.id = PersonalDataId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Purpose(YAMLRoot):
    """
    External vocabulary term referenced by a HealthDCAT-AP shape but not itself defined by a sh:NodeShape anywhere in
    HealthDCAT-AP's own release -- confirmed, not assumed: it doesn't appear in the tier shapes files or in
    mdr-vocabularies.shape.ttl (which this port does parse, for controlled-vocabulary bindings on other properties --
    see script docstring); it's a pointer into an external ontology (DPV/DQV) HealthDCAT-AP never embeds. Carries just
    id: real usage is a reference to an external controlled-vocabulary term (e.g. a DPV Purpose/LegalBasis URI), not a
    locally-described object -- and a slotless class can only ever be instantiated as {}, which linkml_runtime's own
    YAML loader rejects outright ('Empty list elements are not allowed'), making a slotless required range unusable in
    practice, not just thin.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Purpose"]
    class_class_curie: ClassVar[str] = "dpv:Purpose"
    class_name: ClassVar[str] = "Purpose"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.Purpose

    id: Union[str, PurposeId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PurposeId):
            self.id = PurposeId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QualityCertificate(YAMLRoot):
    """
    External vocabulary term referenced by a HealthDCAT-AP shape but not itself defined by a sh:NodeShape anywhere in
    HealthDCAT-AP's own release -- confirmed, not assumed: it doesn't appear in the tier shapes files or in
    mdr-vocabularies.shape.ttl (which this port does parse, for controlled-vocabulary bindings on other properties --
    see script docstring); it's a pointer into an external ontology (DPV/DQV) HealthDCAT-AP never embeds. Carries just
    id: real usage is a reference to an external controlled-vocabulary term (e.g. a DPV Purpose/LegalBasis URI), not a
    locally-described object -- and a slotless class can only ever be instantiated as {}, which linkml_runtime's own
    YAML loader rejects outright ('Empty list elements are not allowed'), making a slotless required range unusable in
    practice, not just thin.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DQV["QualityCertificate"]
    class_class_curie: ClassVar[str] = "dqv:QualityCertificate"
    class_name: ClassVar[str] = "QualityCertificate"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.QualityCertificate

    id: Union[str, QualityCertificateId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QualityCertificateId):
            self.id = QualityCertificateId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DatasetAttribution(Attribution):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Attribution"]
    class_class_curie: ClassVar[str] = "prov:Attribution"
    class_name: ClassVar[str] = "DatasetAttribution"
    class_model_uri: ClassVar[URIRef] = HEALTH_DCAT_AP_PLUS.DatasetAttribution

    attribution_agent: Union[dict, Agent] = None
    attribution_had_role: Union[str, URIorCURIE] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.attribution_agent):
            self.MissingRequiredField("attribution_agent")
        if not isinstance(self.attribution_agent, Agent):
            self.attribution_agent = Agent(**as_dict(self.attribution_agent))

        if self._is_empty(self.attribution_had_role):
            self.MissingRequiredField("attribution_had_role")
        if not isinstance(self.attribution_had_role, URIorCURIE):
            self.attribution_had_role = URIorCURIE(self.attribution_had_role)

        super().__post_init__(**kwargs)


# Enumerations
class DatasetThemes(EnumDefinitionImpl):

    AGRI = PermissibleValue(
        text="AGRI",
        description="Agriculture, fisheries, forestry and food",
        meaning=None)
    ECON = PermissibleValue(
        text="ECON",
        description="Economy and finance",
        meaning=None)
    EDUC = PermissibleValue(
        text="EDUC",
        description="Education, culture and sport",
        meaning=None)
    ENER = PermissibleValue(
        text="ENER",
        description="Energy",
        meaning=None)
    ENVI = PermissibleValue(
        text="ENVI",
        description="Environment",
        meaning=None)
    GOVE = PermissibleValue(
        text="GOVE",
        description="Government and public sector",
        meaning=None)
    HEAL = PermissibleValue(
        text="HEAL",
        description="Health",
        meaning=None)
    INTR = PermissibleValue(
        text="INTR",
        description="International issues",
        meaning=None)
    JUST = PermissibleValue(
        text="JUST",
        description="Justice, legal system and public safety",
        meaning=None)
    OP_DATPRO = PermissibleValue(
        text="OP_DATPRO",
        description="Provisional data",
        meaning=None)
    REGI = PermissibleValue(
        text="REGI",
        description="Regions and cities",
        meaning=None)
    SOCI = PermissibleValue(
        text="SOCI",
        description="Population and society",
        meaning=None)
    TECH = PermissibleValue(
        text="TECH",
        description="Science and technology",
        meaning=None)
    TRAN = PermissibleValue(
        text="TRAN",
        description="Transport",
        meaning=None)

    _defn = EnumDefinition(
        name="DatasetThemes",
    )

class TopLevelMediaTypes(EnumDefinitionImpl):

    application = PermissibleValue(text="application")
    audio = PermissibleValue(text="audio")
    example = PermissibleValue(text="example")
    font = PermissibleValue(text="font")
    haptics = PermissibleValue(text="haptics")
    image = PermissibleValue(text="image")
    message = PermissibleValue(text="message")
    model = PermissibleValue(text="model")
    multipart = PermissibleValue(text="multipart")
    text = PermissibleValue(text="text")
    video = PermissibleValue(text="video")

    _defn = EnumDefinition(
        name="TopLevelMediaTypes",
    )

class QUDTQuantityKindEnum(EnumDefinitionImpl):
    """
    Possible kinds of quantifiable attribute types provided as QUDT QualityKind instances.
    """
    _defn = EnumDefinition(
        name="QUDTQuantityKindEnum",
        description="Possible kinds of quantifiable attribute types provided as QUDT QualityKind instances.",
    )

class QUDTUnitEnum(EnumDefinitionImpl):
    """
    Possible kinds of QUDT unit instances.
    """
    _defn = EnumDefinition(
        name="QUDTUnitEnum",
        description="Possible kinds of QUDT unit instances.",
    )

# Slots
class slots:
    pass

slots.qualified_association = Slot(uri=PROV.qualifiedAssociation, name="qualified_association", curie=PROV.curie('qualifiedAssociation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.qualified_association, domain=None, range=Optional[Union[Union[dict, Association], list[Union[dict, Association]]]])

slots.agent = Slot(uri=PROV.agent, name="agent", curie=PROV.curie('agent'),
                   model_uri=HEALTH_DCAT_AP_PLUS.agent, domain=None, range=Union[dict, AgenticEntity])

slots.association_had_role = Slot(uri=PROV.hadRole, name="association_had_role", curie=PROV.curie('hadRole'),
                   model_uri=HEALTH_DCAT_AP_PLUS.association_had_role, domain=None, range=Union[str, URIorCURIE])

slots.access_URL = Slot(uri=DCAT.accessURL, name="access_URL", curie=DCAT.curie('accessURL'),
                   model_uri=HEALTH_DCAT_AP_PLUS.access_URL, domain=None, range=Optional[str])

slots.access_rights = Slot(uri=DCTERMS.accessRights, name="access_rights", curie=DCTERMS.curie('accessRights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.access_rights, domain=None, range=Optional[str])

slots.access_service = Slot(uri=DCAT.accessService, name="access_service", curie=DCAT.curie('accessService'),
                   model_uri=HEALTH_DCAT_AP_PLUS.access_service, domain=None, range=Optional[str])

slots.algorithm = Slot(uri=SPDX.algorithm, name="algorithm", curie=SPDX.curie('algorithm'),
                   model_uri=HEALTH_DCAT_AP_PLUS.algorithm, domain=None, range=Optional[str])

slots.applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.applicable_legislation, domain=None, range=Optional[str])

slots.application_profile = Slot(uri=DCTERMS.conformsTo, name="application_profile", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.application_profile, domain=None, range=Optional[str])

slots.availability = Slot(uri=DCATAP.availability, name="availability", curie=DCATAP.curie('availability'),
                   model_uri=HEALTH_DCAT_AP_PLUS.availability, domain=None, range=Optional[str])

slots.bbox = Slot(uri=DCAT.bbox, name="bbox", curie=DCAT.curie('bbox'),
                   model_uri=HEALTH_DCAT_AP_PLUS.bbox, domain=None, range=Optional[str])

slots.beginning = Slot(uri=TIME.hasBeginning, name="beginning", curie=TIME.curie('hasBeginning'),
                   model_uri=HEALTH_DCAT_AP_PLUS.beginning, domain=None, range=Optional[str])

slots.byte_size = Slot(uri=DCAT.byteSize, name="byte_size", curie=DCAT.curie('byteSize'),
                   model_uri=HEALTH_DCAT_AP_PLUS.byte_size, domain=None, range=Optional[str])

slots.carried_out_by = Slot(uri=PROV.wasAssociatedWith, name="carried_out_by", curie=PROV.curie('wasAssociatedWith'),
                   model_uri=HEALTH_DCAT_AP_PLUS.carried_out_by, domain=None, range=Optional[Union[dict[Union[str, AgenticEntityId], Union[dict, AgenticEntity]], list[Union[dict, AgenticEntity]]]])

slots.catalogue = Slot(uri=DCAT.catalog, name="catalogue", curie=DCAT.curie('catalog'),
                   model_uri=HEALTH_DCAT_AP_PLUS.catalogue, domain=None, range=Optional[str])

slots.centroid = Slot(uri=DCAT.centroid, name="centroid", curie=DCAT.curie('centroid'),
                   model_uri=HEALTH_DCAT_AP_PLUS.centroid, domain=None, range=Optional[str])

slots.change_type = Slot(uri=ADMS.status, name="change_type", curie=ADMS.curie('status'),
                   model_uri=HEALTH_DCAT_AP_PLUS.change_type, domain=None, range=Optional[str])

slots.checksum = Slot(uri=SPDX.checksum, name="checksum", curie=SPDX.curie('checksum'),
                   model_uri=HEALTH_DCAT_AP_PLUS.checksum, domain=None, range=Optional[str])

slots.checksum_value = Slot(uri=SPDX.checksumValue, name="checksum_value", curie=SPDX.curie('checksumValue'),
                   model_uri=HEALTH_DCAT_AP_PLUS.checksum_value, domain=None, range=Optional[str])

slots.compression_format = Slot(uri=DCAT.compressFormat, name="compression_format", curie=DCAT.curie('compressFormat'),
                   model_uri=HEALTH_DCAT_AP_PLUS.compression_format, domain=None, range=Optional[str])

slots.conforms_to = Slot(uri=DCTERMS.conformsTo, name="conforms_to", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.conforms_to, domain=None, range=Optional[str])

slots.contact_point = Slot(uri=DCAT.contactPoint, name="contact_point", curie=DCAT.curie('contactPoint'),
                   model_uri=HEALTH_DCAT_AP_PLUS.contact_point, domain=None, range=Optional[str])

slots.creator = Slot(uri=DCTERMS.creator, name="creator", curie=DCTERMS.curie('creator'),
                   model_uri=HEALTH_DCAT_AP_PLUS.creator, domain=None, range=Optional[str])

slots.dataset_distribution = Slot(uri=DCAT.distribution, name="dataset_distribution", curie=DCAT.curie('distribution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.dataset_distribution, domain=None, range=Optional[str])

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.description, domain=None, range=Optional[str])

slots.documentation = Slot(uri=FOAF.page, name="documentation", curie=FOAF.curie('page'),
                   model_uri=HEALTH_DCAT_AP_PLUS.documentation, domain=None, range=Optional[str])

slots.download_URL = Slot(uri=DCAT.downloadURL, name="download_URL", curie=DCAT.curie('downloadURL'),
                   model_uri=HEALTH_DCAT_AP_PLUS.download_URL, domain=None, range=Optional[str])

slots.end = Slot(uri=TIME.hasEnd, name="end", curie=TIME.curie('hasEnd'),
                   model_uri=HEALTH_DCAT_AP_PLUS.end, domain=None, range=Optional[str])

slots.end_date = Slot(uri=DCAT.endDate, name="end_date", curie=DCAT.curie('endDate'),
                   model_uri=HEALTH_DCAT_AP_PLUS.end_date, domain=None, range=Optional[str])

slots.endpoint_URL = Slot(uri=DCAT.endpointURL, name="endpoint_URL", curie=DCAT.curie('endpointURL'),
                   model_uri=HEALTH_DCAT_AP_PLUS.endpoint_URL, domain=None, range=Optional[str])

slots.endpoint_description = Slot(uri=DCAT.endpointDescription, name="endpoint_description", curie=DCAT.curie('endpointDescription'),
                   model_uri=HEALTH_DCAT_AP_PLUS.endpoint_description, domain=None, range=Optional[str])

slots.evaluated_activity = Slot(uri=PROV.wasInformedBy, name="evaluated_activity", curie=PROV.curie('wasInformedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.evaluated_activity, domain=None, range=Optional[Union[dict[Union[str, EvaluatedActivityId], Union[dict, EvaluatedActivity]], list[Union[dict, EvaluatedActivity]]]])

slots.evaluated_entity = Slot(uri=PROV.used, name="evaluated_entity", curie=PROV.curie('used'),
                   model_uri=HEALTH_DCAT_AP_PLUS.evaluated_entity, domain=None, range=Optional[Union[dict[Union[str, EvaluatedEntityId], Union[dict, EvaluatedEntity]], list[Union[dict, EvaluatedEntity]]]])

slots.format = Slot(uri=DCTERMS.format, name="format", curie=DCTERMS.curie('format'),
                   model_uri=HEALTH_DCAT_AP_PLUS.format, domain=None, range=Optional[str])

slots.frequency = Slot(uri=DCTERMS.accrualPeriodicity, name="frequency", curie=DCTERMS.curie('accrualPeriodicity'),
                   model_uri=HEALTH_DCAT_AP_PLUS.frequency, domain=None, range=Optional[str])

slots.geographical_coverage = Slot(uri=DCTERMS.spatial, name="geographical_coverage", curie=DCTERMS.curie('spatial'),
                   model_uri=HEALTH_DCAT_AP_PLUS.geographical_coverage, domain=None, range=Optional[str])

slots.geometry = Slot(uri=LOCN.geometry, name="geometry", curie=LOCN.curie('geometry'),
                   model_uri=HEALTH_DCAT_AP_PLUS.geometry, domain=None, range=Optional[str])

slots.had_input_activity = Slot(uri=PROV.wasInformedBy, name="had_input_activity", curie=PROV.curie('wasInformedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.had_input_activity, domain=None, range=Optional[Union[dict[Union[str, ActivityId], Union[dict, Activity]], list[Union[dict, Activity]]]])

slots.had_input_entity = Slot(uri=PROV.used, name="had_input_entity", curie=PROV.curie('used'),
                   model_uri=HEALTH_DCAT_AP_PLUS.had_input_entity, domain=None, range=Optional[Union[dict[Union[str, EntityId], Union[dict, Entity]], list[Union[dict, Entity]]]])

slots.had_output_entity = Slot(uri=PROV.generated, name="had_output_entity", curie=PROV.curie('generated'),
                   model_uri=HEALTH_DCAT_AP_PLUS.had_output_entity, domain=None, range=Optional[Union[dict[Union[str, EntityId], Union[dict, Entity]], list[Union[dict, Entity]]]])

slots.had_role = Slot(uri=DCAT.hadRole, name="had_role", curie=DCAT.curie('hadRole'),
                   model_uri=HEALTH_DCAT_AP_PLUS.had_role, domain=None, range=Optional[str])

slots.has_dataset = Slot(uri=DCAT.dataset, name="has_dataset", curie=DCAT.curie('dataset'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_dataset, domain=None, range=Optional[str])

slots.has_part = Slot(uri=DCTERMS.hasPart, name="has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_part, domain=None, range=Optional[Union[str, ActivityId]])

slots.has_policy = Slot(uri=ODRL.hasPolicy, name="has_policy", curie=ODRL.curie('hasPolicy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_policy, domain=None, range=Optional[str])

slots.has_qualitative_attribute = Slot(uri=DCTERMS.relation, name="has_qualitative_attribute", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_qualitative_attribute, domain=None, range=Optional[Union[Union[dict, QualitativeAttribute], list[Union[dict, QualitativeAttribute]]]])

slots.has_quantitative_attribute = Slot(uri=DCTERMS.relation, name="has_quantitative_attribute", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_quantitative_attribute, domain=None, range=Optional[Union[Union[dict, QuantitativeAttribute], list[Union[dict, QuantitativeAttribute]]]])

slots.has_version = Slot(uri=DCAT.hasVersion, name="has_version", curie=DCAT.curie('hasVersion'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_version, domain=None, range=Optional[str])

slots.homepage = Slot(uri=FOAF.homepage, name="homepage", curie=FOAF.curie('homepage'),
                   model_uri=HEALTH_DCAT_AP_PLUS.homepage, domain=None, range=Optional[str])

slots.id = Slot(uri=DCATAPPLUS.id, name="id", curie=DCATAPPLUS.curie('id'),
                   model_uri=HEALTH_DCAT_AP_PLUS.id, domain=None, range=URIRef)

slots.identifier = Slot(uri=DCTERMS.identifier, name="identifier", curie=DCTERMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.identifier, domain=None, range=Optional[str])

slots.in_series = Slot(uri=DCAT.inSeries, name="in_series", curie=DCAT.curie('inSeries'),
                   model_uri=HEALTH_DCAT_AP_PLUS.in_series, domain=None, range=Optional[str])

slots.is_about_activity = Slot(uri=DCTERMS.subject, name="is_about_activity", curie=DCTERMS.curie('subject'),
                   model_uri=HEALTH_DCAT_AP_PLUS.is_about_activity, domain=None, range=Optional[Union[dict[Union[str, EvaluatedActivityId], Union[dict, EvaluatedActivity]], list[Union[dict, EvaluatedActivity]]]])

slots.is_about_entity = Slot(uri=DCTERMS.subject, name="is_about_entity", curie=DCTERMS.curie('subject'),
                   model_uri=HEALTH_DCAT_AP_PLUS.is_about_entity, domain=None, range=Optional[Union[dict[Union[str, EvaluatedEntityId], Union[dict, EvaluatedEntity]], list[Union[dict, EvaluatedEntity]]]])

slots.is_referenced_by = Slot(uri=DCTERMS.isReferencedBy, name="is_referenced_by", curie=DCTERMS.curie('isReferencedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.is_referenced_by, domain=None, range=Optional[str])

slots.keyword = Slot(uri=DCAT.keyword, name="keyword", curie=DCAT.curie('keyword'),
                   model_uri=HEALTH_DCAT_AP_PLUS.keyword, domain=None, range=Optional[str])

slots.landing_page = Slot(uri=DCAT.landingPage, name="landing_page", curie=DCAT.curie('landingPage'),
                   model_uri=HEALTH_DCAT_AP_PLUS.landing_page, domain=None, range=Optional[str])

slots.language = Slot(uri=DCTERMS.language, name="language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.language, domain=None, range=Optional[str])

slots.licence = Slot(uri=DCTERMS.license, name="licence", curie=DCTERMS.curie('license'),
                   model_uri=HEALTH_DCAT_AP_PLUS.licence, domain=None, range=Optional[str])

slots.linked_schemas = Slot(uri=DCTERMS.conformsTo, name="linked_schemas", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.linked_schemas, domain=None, range=Optional[str])

slots.listing_date = Slot(uri=DCTERMS.issued, name="listing_date", curie=DCTERMS.curie('issued'),
                   model_uri=HEALTH_DCAT_AP_PLUS.listing_date, domain=None, range=Optional[str])

slots.media_type = Slot(uri=DCAT.mediaType, name="media_type", curie=DCAT.curie('mediaType'),
                   model_uri=HEALTH_DCAT_AP_PLUS.media_type, domain=None, range=Optional[str])

slots.modification_date = Slot(uri=DCTERMS.modified, name="modification_date", curie=DCTERMS.curie('modified'),
                   model_uri=HEALTH_DCAT_AP_PLUS.modification_date, domain=None, range=Optional[str])

slots.name = Slot(uri=FOAF.name, name="name", curie=FOAF.curie('name'),
                   model_uri=HEALTH_DCAT_AP_PLUS.name, domain=None, range=Optional[str])

slots.notation = Slot(uri=SKOS.notation, name="notation", curie=SKOS.curie('notation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.notation, domain=None, range=Optional[str])

slots.occurred_in = Slot(uri=PROV.atLocation, name="occurred_in", curie=PROV.curie('atLocation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.occurred_in, domain=None, range=Optional[Union[dict, Surrounding]])

slots.other_identifier = Slot(uri=ADMS.identifier, name="other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.other_identifier, domain=None, range=Optional[str])

slots.packaging_format = Slot(uri=DCAT.packageFormat, name="packaging_format", curie=DCAT.curie('packageFormat'),
                   model_uri=HEALTH_DCAT_AP_PLUS.packaging_format, domain=None, range=Optional[str])

slots.part_of = Slot(uri=DCTERMS.isPartOf, name="part_of", curie=DCTERMS.curie('isPartOf'),
                   model_uri=HEALTH_DCAT_AP_PLUS.part_of, domain=None, range=Optional[Union[str, ActivityId]])

slots.preferred_label = Slot(uri=SKOS.prefLabel, name="preferred_label", curie=SKOS.curie('prefLabel'),
                   model_uri=HEALTH_DCAT_AP_PLUS.preferred_label, domain=None, range=Optional[str])

slots.primary_topic = Slot(uri=FOAF.primaryTopic, name="primary_topic", curie=FOAF.curie('primaryTopic'),
                   model_uri=HEALTH_DCAT_AP_PLUS.primary_topic, domain=None, range=Optional[str])

slots.provenance = Slot(uri=DCTERMS.provenance, name="provenance", curie=DCTERMS.curie('provenance'),
                   model_uri=HEALTH_DCAT_AP_PLUS.provenance, domain=None, range=Optional[str])

slots.publisher = Slot(uri=DCTERMS.publisher, name="publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=HEALTH_DCAT_AP_PLUS.publisher, domain=None, range=Optional[str])

slots.qualified_attribution = Slot(uri=PROV.qualifiedAttribution, name="qualified_attribution", curie=PROV.curie('qualifiedAttribution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.qualified_attribution, domain=None, range=Optional[str])

slots.qualified_relation = Slot(uri=DCAT.qualifiedRelation, name="qualified_relation", curie=DCAT.curie('qualifiedRelation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.qualified_relation, domain=None, range=Optional[str])

slots.rdf_type = Slot(uri=RDF.type, name="rdf_type", curie=RDF.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.rdf_type, domain=None, range=Optional[Union[dict, DefinedTerm]])

slots.realized_plan = Slot(uri=PROV.used, name="realized_plan", curie=PROV.curie('used'),
                   model_uri=HEALTH_DCAT_AP_PLUS.realized_plan, domain=None, range=Optional[Union[dict, Plan]])

slots.record = Slot(uri=DCAT.record, name="record", curie=DCAT.curie('record'),
                   model_uri=HEALTH_DCAT_AP_PLUS.record, domain=None, range=Optional[str])

slots.related_resource = Slot(uri=DCTERMS.relation, name="related_resource", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.related_resource, domain=None, range=Optional[str])

slots.relation = Slot(uri=DCTERMS.relation, name="relation", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.relation, domain=None, range=Optional[str])

slots.release_date = Slot(uri=DCTERMS.issued, name="release_date", curie=DCTERMS.curie('issued'),
                   model_uri=HEALTH_DCAT_AP_PLUS.release_date, domain=None, range=Optional[str])

slots.rights = Slot(uri=DCTERMS.rights, name="rights", curie=DCTERMS.curie('rights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.rights, domain=None, range=Optional[str])

slots.sample = Slot(uri=ADMS.sample, name="sample", curie=ADMS.curie('sample'),
                   model_uri=HEALTH_DCAT_AP_PLUS.sample, domain=None, range=Optional[str])

slots.serves_dataset = Slot(uri=DCAT.servesDataset, name="serves_dataset", curie=DCAT.curie('servesDataset'),
                   model_uri=HEALTH_DCAT_AP_PLUS.serves_dataset, domain=None, range=Optional[str])

slots.service = Slot(uri=DCAT.service, name="service", curie=DCAT.curie('service'),
                   model_uri=HEALTH_DCAT_AP_PLUS.service, domain=None, range=Optional[str])

slots.source = Slot(uri=DCTERMS.source, name="source", curie=DCTERMS.curie('source'),
                   model_uri=HEALTH_DCAT_AP_PLUS.source, domain=None, range=Optional[str])

slots.source_metadata = Slot(uri=DCTERMS.source, name="source_metadata", curie=DCTERMS.curie('source'),
                   model_uri=HEALTH_DCAT_AP_PLUS.source_metadata, domain=None, range=Optional[str])

slots.spatial_resolution = Slot(uri=DCAT.spatialResolutionInMeters, name="spatial_resolution", curie=DCAT.curie('spatialResolutionInMeters'),
                   model_uri=HEALTH_DCAT_AP_PLUS.spatial_resolution, domain=None, range=Optional[str])

slots.start_date = Slot(uri=DCAT.startDate, name="start_date", curie=DCAT.curie('startDate'),
                   model_uri=HEALTH_DCAT_AP_PLUS.start_date, domain=None, range=Optional[str])

slots.status = Slot(uri=ADMS.status, name="status", curie=ADMS.curie('status'),
                   model_uri=HEALTH_DCAT_AP_PLUS.status, domain=None, range=Optional[str])

slots.temporal_coverage = Slot(uri=DCTERMS.temporal, name="temporal_coverage", curie=DCTERMS.curie('temporal'),
                   model_uri=HEALTH_DCAT_AP_PLUS.temporal_coverage, domain=None, range=Optional[str])

slots.temporal_resolution = Slot(uri=DCAT.temporalResolution, name="temporal_resolution", curie=DCAT.curie('temporalResolution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.temporal_resolution, domain=None, range=Optional[str])

slots.theme = Slot(uri=DCAT.theme, name="theme", curie=DCAT.curie('theme'),
                   model_uri=HEALTH_DCAT_AP_PLUS.theme, domain=None, range=Optional[str])

slots.themes = Slot(uri=DCAT.themeTaxonomy, name="themes", curie=DCAT.curie('themeTaxonomy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.themes, domain=None, range=Optional[str])

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.title, domain=None, range=Optional[str])

slots.type = Slot(uri=DCTERMS.type, name="type", curie=DCTERMS.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.type, domain=None, range=Optional[str])

slots.value = Slot(uri=PROV.value, name="value", curie=PROV.curie('value'),
                   model_uri=HEALTH_DCAT_AP_PLUS.value, domain=None, range=Optional[str])

slots.version = Slot(uri=DCAT.version, name="version", curie=DCAT.curie('version'),
                   model_uri=HEALTH_DCAT_AP_PLUS.version, domain=None, range=Optional[str])

slots.version_notes = Slot(uri=ADMS.versionNotes, name="version_notes", curie=ADMS.curie('versionNotes'),
                   model_uri=HEALTH_DCAT_AP_PLUS.version_notes, domain=None, range=Optional[str])

slots.was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="was_generated_by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.was_generated_by, domain=None, range=Optional[str])

slots.titles = Slot(uri=CSVW.titles, name="titles", curie=CSVW.curie('titles'),
                   model_uri=HEALTH_DCAT_AP_PLUS.titles, domain=None, range=Union[str, list[str]])

slots.datatype = Slot(uri=CSVW.datatype, name="datatype", curie=CSVW.curie('datatype'),
                   model_uri=HEALTH_DCAT_AP_PLUS.datatype, domain=None, range=str)

slots.property_url = Slot(uri=CSVW.propertyUrl, name="property_url", curie=CSVW.curie('propertyUrl'),
                   model_uri=HEALTH_DCAT_AP_PLUS.property_url, domain=None, range=Optional[str])

slots.email = Slot(uri=CV.email, name="email", curie=CV.curie('email'),
                   model_uri=HEALTH_DCAT_AP_PLUS.email, domain=None, range=Optional[Union[str, list[str]]])

slots.contact_page = Slot(uri=CV.contactPage, name="contact_page", curie=CV.curie('contactPage'),
                   model_uri=HEALTH_DCAT_AP_PLUS.contact_page, domain=None, range=Optional[Union[str, list[str]]])

slots.telephone = Slot(uri=CV.telephone, name="telephone", curie=CV.curie('telephone'),
                   model_uri=HEALTH_DCAT_AP_PLUS.telephone, domain=None, range=Optional[Union[str, list[str]]])

slots.opening_hours = Slot(uri=CV.openingHours, name="opening_hours", curie=CV.curie('openingHours'),
                   model_uri=HEALTH_DCAT_AP_PLUS.opening_hours, domain=None, range=Optional[Union[Union[dict, TemporalEntity], list[Union[dict, TemporalEntity]]]])

slots.special_opening_hours_specification = Slot(uri=CV.specialOpeningHoursSpecification, name="special_opening_hours_specification", curie=CV.curie('specialOpeningHoursSpecification'),
                   model_uri=HEALTH_DCAT_AP_PLUS.special_opening_hours_specification, domain=None, range=Optional[Union[Union[dict, TemporalEntity], list[Union[dict, TemporalEntity]]]])

slots.has_purpose = Slot(uri=DPV.hasPurpose, name="has_purpose", curie=DPV.curie('hasPurpose'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_purpose, domain=None, range=Optional[Union[Union[str, PurposeId], list[Union[str, PurposeId]]]])

slots.hdab = Slot(uri=HEALTHDCATAP.hdab, name="hdab", curie=HEALTHDCATAP.curie('hdab'),
                   model_uri=HEALTH_DCAT_AP_PLUS.hdab, domain=None, range=Union[dict, HealthAgent])

slots.custodian = Slot(uri=GEODCATAP.custodian, name="custodian", curie=GEODCATAP.curie('custodian'),
                   model_uri=HEALTH_DCAT_AP_PLUS.custodian, domain=None, range=Optional[Union[dict, HealthAgent]])

slots.health_category = Slot(uri=HEALTHDCATAP.healthCategory, name="health_category", curie=HEALTHDCATAP.curie('healthCategory'),
                   model_uri=HEALTH_DCAT_AP_PLUS.health_category, domain=None, range=Union[Union[dict, Concept], list[Union[dict, Concept]]])

slots.health_theme = Slot(uri=HEALTHDCATAP.healthTheme, name="health_theme", curie=HEALTHDCATAP.curie('healthTheme'),
                   model_uri=HEALTH_DCAT_AP_PLUS.health_theme, domain=None, range=Optional[Union[Union[dict, Concept], list[Union[dict, Concept]]]])

slots.has_legal_basis = Slot(uri=DPV.hasLegalBasis, name="has_legal_basis", curie=DPV.curie('hasLegalBasis'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_legal_basis, domain=None, range=Optional[Union[Union[str, LegalBasisId], list[Union[str, LegalBasisId]]]])

slots.has_personal_data = Slot(uri=DPV.hasPersonalData, name="has_personal_data", curie=DPV.curie('hasPersonalData'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_personal_data, domain=None, range=Optional[Union[Union[str, PersonalDataId], list[Union[str, PersonalDataId]]]])

slots.has_quality_annotation = Slot(uri=DQV.hasQualityAnnotation, name="has_quality_annotation", curie=DQV.curie('hasQualityAnnotation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_quality_annotation, domain=None, range=Optional[Union[Union[str, QualityCertificateId], list[Union[str, QualityCertificateId]]]])

slots.has_structured_data = Slot(uri=HEALTHDCATAP.hasStructuredData, name="has_structured_data", curie=HEALTHDCATAP.curie('hasStructuredData'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_structured_data, domain=None, range=Union[bool, Bool])

slots.has_variables = Slot(uri=HEALTHDCATAP.hasVariables, name="has_variables", curie=HEALTHDCATAP.curie('hasVariables'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_variables, domain=None, range=Optional[Union[Union[dict, TableGroup], list[Union[dict, TableGroup]]]])

slots.analytics = Slot(uri=HEALTHDCATAP.analytics, name="analytics", curie=HEALTHDCATAP.curie('analytics'),
                   model_uri=HEALTH_DCAT_AP_PLUS.analytics, domain=None, range=Optional[Union[Union[dict, HealthDistribution], list[Union[dict, HealthDistribution]]]])

slots.has_code_values = Slot(uri=HEALTHDCATAP.hasCodeValues, name="has_code_values", curie=HEALTHDCATAP.curie('hasCodeValues'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_code_values, domain=None, range=Optional[Union[str, list[str]]])

slots.has_coding_system = Slot(uri=HEALTHDCATAP.hasCodingSystem, name="has_coding_system", curie=HEALTHDCATAP.curie('hasCodingSystem'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_coding_system, domain=None, range=Optional[Union[Union[dict, Standard], list[Union[dict, Standard]]]])

slots.min_typical_age = Slot(uri=HEALTHDCATAP.minTypicalAge, name="min_typical_age", curie=HEALTHDCATAP.curie('minTypicalAge'),
                   model_uri=HEALTH_DCAT_AP_PLUS.min_typical_age, domain=None, range=Optional[int])

slots.max_typical_age = Slot(uri=HEALTHDCATAP.maxTypicalAge, name="max_typical_age", curie=HEALTHDCATAP.curie('maxTypicalAge'),
                   model_uri=HEALTH_DCAT_AP_PLUS.max_typical_age, domain=None, range=Optional[int])

slots.number_of_records = Slot(uri=HEALTHDCATAP.numberOfRecords, name="number_of_records", curie=HEALTHDCATAP.curie('numberOfRecords'),
                   model_uri=HEALTH_DCAT_AP_PLUS.number_of_records, domain=None, range=Optional[int])

slots.number_of_unique_individuals = Slot(uri=HEALTHDCATAP.numberOfUniqueIndividuals, name="number_of_unique_individuals", curie=HEALTHDCATAP.curie('numberOfUniqueIndividuals'),
                   model_uri=HEALTH_DCAT_AP_PLUS.number_of_unique_individuals, domain=None, range=Optional[int])

slots.population_coverage = Slot(uri=HEALTHDCATAP.populationCoverage, name="population_coverage", curie=HEALTHDCATAP.curie('populationCoverage'),
                   model_uri=HEALTH_DCAT_AP_PLUS.population_coverage, domain=None, range=Optional[Union[str, list[str]]])

slots.alternative = Slot(uri=DCTERMS.alternative, name="alternative", curie=DCTERMS.curie('alternative'),
                   model_uri=HEALTH_DCAT_AP_PLUS.alternative, domain=None, range=Optional[Union[str, list[str]]])

slots.retention_period = Slot(uri=HEALTHDCATAP.retentionPeriod, name="retention_period", curie=HEALTHDCATAP.curie('retentionPeriod'),
                   model_uri=HEALTH_DCAT_AP_PLUS.retention_period, domain=None, range=Optional[Union[dict, PeriodOfTime]])

slots.agent_contact_point = Slot(uri=CV.contactPoint, name="agent_contact_point", curie=CV.curie('contactPoint'),
                   model_uri=HEALTH_DCAT_AP_PLUS.agent_contact_point, domain=None, range=Union[dict, ContactPoint])

slots.has_url = Slot(uri=VCARD.hasURL, name="has_url", curie=VCARD.curie('hasURL'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_url, domain=None, range=Optional[str])

slots.has_email = Slot(uri=VCARD.hasEmail, name="has_email", curie=VCARD.curie('hasEmail'),
                   model_uri=HEALTH_DCAT_AP_PLUS.has_email, domain=None, range=Optional[str])

slots.url = Slot(uri=CSVW.url, name="url", curie=CSVW.curie('url'),
                   model_uri=HEALTH_DCAT_AP_PLUS.url, domain=None, range=Optional[str])

slots.column = Slot(uri=CSVW.column, name="column", curie=CSVW.curie('column'),
                   model_uri=HEALTH_DCAT_AP_PLUS.column, domain=None, range=Union[Union[dict, Column], list[Union[dict, Column]]])

slots.table = Slot(uri=CSVW.table, name="table", curie=CSVW.curie('table'),
                   model_uri=HEALTH_DCAT_AP_PLUS.table, domain=None, range=Union[Union[dict, Table], list[Union[dict, Table]]])

slots.attribution_agent = Slot(uri=PROV.agent, name="attribution_agent", curie=PROV.curie('agent'),
                   model_uri=HEALTH_DCAT_AP_PLUS.attribution_agent, domain=None, range=Union[dict, Agent])

slots.attribution_had_role = Slot(uri=DCAT.hadRole, name="attribution_had_role", curie=DCAT.curie('hadRole'),
                   model_uri=HEALTH_DCAT_AP_PLUS.attribution_had_role, domain=None, range=Union[str, URIorCURIE])

slots.definedTerm__from_CV = Slot(uri=SCHEMA.inDefinedTermSet, name="definedTerm__from_CV", curie=SCHEMA.curie('inDefinedTermSet'),
                   model_uri=HEALTH_DCAT_AP_PLUS.definedTerm__from_CV, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.quantitativeAttribute__has_quantity_type = Slot(uri=QUDT.hasQuantityKind, name="quantitativeAttribute__has_quantity_type", curie=QUDT.curie('hasQuantityKind'),
                   model_uri=HEALTH_DCAT_AP_PLUS.quantitativeAttribute__has_quantity_type, domain=None, range=Union[str, DefinedTermId])

slots.quantitativeAttribute__unit = Slot(uri=QUDT.unit, name="quantitativeAttribute__unit", curie=QUDT.curie('unit'),
                   model_uri=HEALTH_DCAT_AP_PLUS.quantitativeAttribute__unit, domain=None, range=Optional[Union[str, DefinedTermId]])

slots.Activity_title = Slot(uri=DCTERMS.title, name="Activity_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_title, domain=Activity, range=Optional[Union[str, list[str]]])

slots.Activity_description = Slot(uri=DCTERMS.description, name="Activity_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_description, domain=Activity, range=Optional[Union[str, list[str]]])

slots.Activity_has_part = Slot(uri=DCTERMS.hasPart, name="Activity_has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_has_part, domain=Activity, range=Optional[Union[dict[Union[str, ActivityId], Union[dict, "Activity"]], list[Union[dict, "Activity"]]]])

slots.Activity_part_of = Slot(uri=DCTERMS.isPartOf, name="Activity_part_of", curie=DCTERMS.curie('isPartOf'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_part_of, domain=Activity, range=Optional[Union[dict[Union[str, ActivityId], Union[dict, "Activity"]], list[Union[dict, "Activity"]]]])

slots.Activity_other_identifier = Slot(uri=ADMS.identifier, name="Activity_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_other_identifier, domain=Activity, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.Activity_has_qualitative_attribute = Slot(uri=DCTERMS.relation, name="Activity_has_qualitative_attribute", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_has_qualitative_attribute, domain=Activity, range=Optional[Union[Union[dict, "QualitativeAttribute"], list[Union[dict, "QualitativeAttribute"]]]])

slots.Activity_has_quantitative_attribute = Slot(uri=DCTERMS.relation, name="Activity_has_quantitative_attribute", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_has_quantitative_attribute, domain=Activity, range=Optional[Union[Union[dict, "QuantitativeAttribute"], list[Union[dict, "QuantitativeAttribute"]]]])

slots.Activity_had_input_entity = Slot(uri=PROV.used, name="Activity_had_input_entity", curie=PROV.curie('used'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_had_input_entity, domain=Activity, range=Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]])

slots.Activity_had_output_entity = Slot(uri=PROV.generated, name="Activity_had_output_entity", curie=PROV.curie('generated'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_had_output_entity, domain=Activity, range=Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]])

slots.Activity_had_input_activity = Slot(uri=PROV.wasInformedBy, name="Activity_had_input_activity", curie=PROV.curie('wasInformedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_had_input_activity, domain=Activity, range=Optional[Union[dict[Union[str, ActivityId], Union[dict, "Activity"]], list[Union[dict, "Activity"]]]])

slots.Activity_carried_out_by = Slot(uri=PROV.wasAssociatedWith, name="Activity_carried_out_by", curie=PROV.curie('wasAssociatedWith'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Activity_carried_out_by, domain=Activity, range=Optional[Union[dict[Union[str, AgenticEntityId], Union[dict, "AgenticEntity"]], list[Union[dict, "AgenticEntity"]]]])

slots.Agent_name = Slot(uri=FOAF.name, name="Agent_name", curie=FOAF.curie('name'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Agent_name, domain=Agent, range=Union[str, list[str]])

slots.Agent_type = Slot(uri=DCTERMS.type, name="Agent_type", curie=DCTERMS.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Agent_type, domain=Agent, range=Optional[Union[dict, "Concept"]])

slots.AgenticEntity_has_part = Slot(uri=DCTERMS.hasPart, name="AgenticEntity_has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=HEALTH_DCAT_AP_PLUS.AgenticEntity_has_part, domain=AgenticEntity, range=Optional[Union[dict[Union[str, AgenticEntityId], Union[dict, "AgenticEntity"]], list[Union[dict, "AgenticEntity"]]]])

slots.AgenticEntity_part_of = Slot(uri=DCTERMS.isPartOf, name="AgenticEntity_part_of", curie=DCTERMS.curie('isPartOf'),
                   model_uri=HEALTH_DCAT_AP_PLUS.AgenticEntity_part_of, domain=AgenticEntity, range=Optional[Union[dict[Union[str, AgenticEntityId], Union[dict, "AgenticEntity"]], list[Union[dict, "AgenticEntity"]]]])

slots.AgenticEntity_other_identifier = Slot(uri=ADMS.identifier, name="AgenticEntity_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.AgenticEntity_other_identifier, domain=AgenticEntity, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.AnalysisDataset_was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="AnalysisDataset_was_generated_by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.AnalysisDataset_was_generated_by, domain=AnalysisDataset, range=Optional[Union[dict[Union[str, DataAnalysisId], Union[dict, DataAnalysis]], list[Union[dict, DataAnalysis]]]])

slots.AnalysisSourceData_was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="AnalysisSourceData_was_generated_by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.AnalysisSourceData_was_generated_by, domain=AnalysisSourceData, range=Optional[Union[dict[Union[str, DataGeneratingActivityId], Union[dict, DataGeneratingActivity]], list[Union[dict, DataGeneratingActivity]]]])

slots.Catalogue_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="Catalogue_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_applicable_legislation, domain=Catalogue, range=Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]])

slots.Catalogue_catalogue = Slot(uri=DCAT.catalog, name="Catalogue_catalogue", curie=DCAT.curie('catalog'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_catalogue, domain=Catalogue, range=Optional[Union[Union[dict, "Catalogue"], list[Union[dict, "Catalogue"]]]])

slots.Catalogue_creator = Slot(uri=DCTERMS.creator, name="Catalogue_creator", curie=DCTERMS.curie('creator'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_creator, domain=Catalogue, range=Optional[Union[dict, Agent]])

slots.Catalogue_description = Slot(uri=DCTERMS.description, name="Catalogue_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_description, domain=Catalogue, range=Union[str, list[str]])

slots.Catalogue_geographical_coverage = Slot(uri=DCTERMS.spatial, name="Catalogue_geographical_coverage", curie=DCTERMS.curie('spatial'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_geographical_coverage, domain=Catalogue, range=Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]])

slots.Catalogue_has_dataset = Slot(uri=DCAT.dataset, name="Catalogue_has_dataset", curie=DCAT.curie('dataset'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_has_dataset, domain=Catalogue, range=Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]])

slots.Catalogue_has_part = Slot(uri=DCTERMS.hasPart, name="Catalogue_has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_has_part, domain=Catalogue, range=Optional[Union[Union[dict, "Catalogue"], list[Union[dict, "Catalogue"]]]])

slots.Catalogue_homepage = Slot(uri=FOAF.homepage, name="Catalogue_homepage", curie=FOAF.curie('homepage'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_homepage, domain=Catalogue, range=Optional[Union[dict, "Document"]])

slots.Catalogue_language = Slot(uri=DCTERMS.language, name="Catalogue_language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_language, domain=Catalogue, range=Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]])

slots.Catalogue_licence = Slot(uri=DCTERMS.license, name="Catalogue_licence", curie=DCTERMS.curie('license'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_licence, domain=Catalogue, range=Optional[Union[dict, "LicenseDocument"]])

slots.Catalogue_modification_date = Slot(uri=DCTERMS.modified, name="Catalogue_modification_date", curie=DCTERMS.curie('modified'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_modification_date, domain=Catalogue, range=Optional[Union[str, XSDDate]])

slots.Catalogue_publisher = Slot(uri=DCTERMS.publisher, name="Catalogue_publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_publisher, domain=Catalogue, range=Union[dict, Agent])

slots.Catalogue_record = Slot(uri=DCAT.record, name="Catalogue_record", curie=DCAT.curie('record'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_record, domain=Catalogue, range=Optional[Union[Union[dict, "CatalogueRecord"], list[Union[dict, "CatalogueRecord"]]]])

slots.Catalogue_release_date = Slot(uri=DCTERMS.issued, name="Catalogue_release_date", curie=DCTERMS.curie('issued'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_release_date, domain=Catalogue, range=Optional[Union[str, XSDDate]])

slots.Catalogue_rights = Slot(uri=DCTERMS.rights, name="Catalogue_rights", curie=DCTERMS.curie('rights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_rights, domain=Catalogue, range=Optional[Union[dict, "RightsStatement"]])

slots.Catalogue_service = Slot(uri=DCAT.service, name="Catalogue_service", curie=DCAT.curie('service'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_service, domain=Catalogue, range=Optional[Union[Union[dict, "DataService"], list[Union[dict, "DataService"]]]])

slots.Catalogue_temporal_coverage = Slot(uri=DCTERMS.temporal, name="Catalogue_temporal_coverage", curie=DCTERMS.curie('temporal'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_temporal_coverage, domain=Catalogue, range=Optional[Union[Union[dict, "PeriodOfTime"], list[Union[dict, "PeriodOfTime"]]]])

slots.Catalogue_themes = Slot(uri=DCAT.themeTaxonomy, name="Catalogue_themes", curie=DCAT.curie('themeTaxonomy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_themes, domain=Catalogue, range=Optional[Union[Union[dict, "ConceptScheme"], list[Union[dict, "ConceptScheme"]]]])

slots.Catalogue_title = Slot(uri=DCTERMS.title, name="Catalogue_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Catalogue_title, domain=Catalogue, range=Union[str, list[str]])

slots.CatalogueRecord_application_profile = Slot(uri=DCTERMS.conformsTo, name="CatalogueRecord_application_profile", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_application_profile, domain=CatalogueRecord, range=Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]])

slots.CatalogueRecord_change_type = Slot(uri=ADMS.status, name="CatalogueRecord_change_type", curie=ADMS.curie('status'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_change_type, domain=CatalogueRecord, range=Optional[Union[dict, "Concept"]])

slots.CatalogueRecord_description = Slot(uri=DCTERMS.description, name="CatalogueRecord_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_description, domain=CatalogueRecord, range=Optional[Union[str, list[str]]])

slots.CatalogueRecord_language = Slot(uri=DCTERMS.language, name="CatalogueRecord_language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_language, domain=CatalogueRecord, range=Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]])

slots.CatalogueRecord_listing_date = Slot(uri=DCTERMS.issued, name="CatalogueRecord_listing_date", curie=DCTERMS.curie('issued'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_listing_date, domain=CatalogueRecord, range=Optional[Union[str, XSDDate]])

slots.CatalogueRecord_modification_date = Slot(uri=DCTERMS.modified, name="CatalogueRecord_modification_date", curie=DCTERMS.curie('modified'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_modification_date, domain=CatalogueRecord, range=Union[str, XSDDate])

slots.CatalogueRecord_primary_topic = Slot(uri=FOAF.primaryTopic, name="CatalogueRecord_primary_topic", curie=FOAF.curie('primaryTopic'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_primary_topic, domain=CatalogueRecord, range=Union[dict, Any])

slots.CatalogueRecord_source_metadata = Slot(uri=DCTERMS.source, name="CatalogueRecord_source_metadata", curie=DCTERMS.curie('source'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_source_metadata, domain=CatalogueRecord, range=Optional[Union[dict, "CatalogueRecord"]])

slots.CatalogueRecord_title = Slot(uri=DCTERMS.title, name="CatalogueRecord_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.CatalogueRecord_title, domain=CatalogueRecord, range=Optional[Union[str, list[str]]])

slots.Checksum_algorithm = Slot(uri=SPDX.algorithm, name="Checksum_algorithm", curie=SPDX.curie('algorithm'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Checksum_algorithm, domain=Checksum, range=Union[dict, "ChecksumAlgorithm"])

slots.Checksum_checksum_value = Slot(uri=SPDX.checksumValue, name="Checksum_checksum_value", curie=SPDX.curie('checksumValue'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Checksum_checksum_value, domain=Checksum, range=str)

slots.ClassifierMixin_type = Slot(uri=DCTERMS.type, name="ClassifierMixin_type", curie=DCTERMS.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.ClassifierMixin_type, domain=None, range=Optional[Union[dict, "DefinedTerm"]])

slots.Concept_preferred_label = Slot(uri=SKOS.prefLabel, name="Concept_preferred_label", curie=SKOS.curie('prefLabel'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Concept_preferred_label, domain=Concept, range=Union[str, list[str]])

slots.ConceptScheme_title = Slot(uri=DCTERMS.title, name="ConceptScheme_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.ConceptScheme_title, domain=ConceptScheme, range=Union[str, list[str]])

slots.DataAnalysis_evaluated_entity = Slot(uri=PROV.used, name="DataAnalysis_evaluated_entity", curie=PROV.curie('used'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataAnalysis_evaluated_entity, domain=DataAnalysis, range=Optional[Union[dict[Union[str, AnalysisSourceDataId], Union[dict, "AnalysisSourceData"]], list[Union[dict, "AnalysisSourceData"]]]])

slots.DataService_access_rights = Slot(uri=DCTERMS.accessRights, name="DataService_access_rights", curie=DCTERMS.curie('accessRights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_access_rights, domain=DataService, range=Optional[Union[dict, "RightsStatement"]])

slots.DataService_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="DataService_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_applicable_legislation, domain=DataService, range=Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]])

slots.DataService_conforms_to = Slot(uri=DCTERMS.conformsTo, name="DataService_conforms_to", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_conforms_to, domain=DataService, range=Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]])

slots.DataService_contact_point = Slot(uri=DCAT.contactPoint, name="DataService_contact_point", curie=DCAT.curie('contactPoint'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_contact_point, domain=DataService, range=Optional[Union[Union[dict, "Kind"], list[Union[dict, "Kind"]]]])

slots.DataService_description = Slot(uri=DCTERMS.description, name="DataService_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_description, domain=DataService, range=Optional[Union[str, list[str]]])

slots.DataService_documentation = Slot(uri=FOAF.page, name="DataService_documentation", curie=FOAF.curie('page'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_documentation, domain=DataService, range=Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]])

slots.DataService_endpoint_URL = Slot(uri=DCAT.endpointURL, name="DataService_endpoint_URL", curie=DCAT.curie('endpointURL'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_endpoint_URL, domain=DataService, range=Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]])

slots.DataService_endpoint_description = Slot(uri=DCAT.endpointDescription, name="DataService_endpoint_description", curie=DCAT.curie('endpointDescription'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_endpoint_description, domain=DataService, range=Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]])

slots.DataService_format = Slot(uri=DCTERMS.format, name="DataService_format", curie=DCTERMS.curie('format'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_format, domain=DataService, range=Optional[Union[Union[dict, "MediaTypeOrExtent"], list[Union[dict, "MediaTypeOrExtent"]]]])

slots.DataService_keyword = Slot(uri=DCAT.keyword, name="DataService_keyword", curie=DCAT.curie('keyword'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_keyword, domain=DataService, range=Optional[Union[str, list[str]]])

slots.DataService_landing_page = Slot(uri=DCAT.landingPage, name="DataService_landing_page", curie=DCAT.curie('landingPage'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_landing_page, domain=DataService, range=Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]])

slots.DataService_licence = Slot(uri=DCTERMS.license, name="DataService_licence", curie=DCTERMS.curie('license'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_licence, domain=DataService, range=Optional[Union[dict, "LicenseDocument"]])

slots.DataService_publisher = Slot(uri=DCTERMS.publisher, name="DataService_publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_publisher, domain=DataService, range=Optional[Union[dict, Agent]])

slots.DataService_serves_dataset = Slot(uri=DCAT.servesDataset, name="DataService_serves_dataset", curie=DCAT.curie('servesDataset'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_serves_dataset, domain=DataService, range=Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]])

slots.DataService_theme = Slot(uri=DCAT.theme, name="DataService_theme", curie=DCAT.curie('theme'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_theme, domain=DataService, range=Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]])

slots.DataService_title = Slot(uri=DCTERMS.title, name="DataService_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DataService_title, domain=DataService, range=Union[str, list[str]])

slots.Dataset_access_rights = Slot(uri=DCTERMS.accessRights, name="Dataset_access_rights", curie=DCTERMS.curie('accessRights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_access_rights, domain=Dataset, range=Optional[Union[dict, "RightsStatement"]])

slots.Dataset_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="Dataset_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_applicable_legislation, domain=Dataset, range=Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]])

slots.Dataset_conforms_to = Slot(uri=DCTERMS.conformsTo, name="Dataset_conforms_to", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_conforms_to, domain=Dataset, range=Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]])

slots.Dataset_contact_point = Slot(uri=DCAT.contactPoint, name="Dataset_contact_point", curie=DCAT.curie('contactPoint'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_contact_point, domain=Dataset, range=Optional[Union[Union[dict, "Kind"], list[Union[dict, "Kind"]]]])

slots.Dataset_creator = Slot(uri=DCTERMS.creator, name="Dataset_creator", curie=DCTERMS.curie('creator'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_creator, domain=Dataset, range=Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]])

slots.Dataset_dataset_distribution = Slot(uri=DCAT.distribution, name="Dataset_dataset_distribution", curie=DCAT.curie('distribution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_dataset_distribution, domain=Dataset, range=Optional[Union[Union[dict, "Distribution"], list[Union[dict, "Distribution"]]]])

slots.Dataset_description = Slot(uri=DCTERMS.description, name="Dataset_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_description, domain=Dataset, range=Union[str, list[str]])

slots.Dataset_documentation = Slot(uri=FOAF.page, name="Dataset_documentation", curie=FOAF.curie('page'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_documentation, domain=Dataset, range=Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]])

slots.Dataset_frequency = Slot(uri=DCTERMS.accrualPeriodicity, name="Dataset_frequency", curie=DCTERMS.curie('accrualPeriodicity'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_frequency, domain=Dataset, range=Optional[Union[dict, "Frequency"]])

slots.Dataset_geographical_coverage = Slot(uri=DCTERMS.spatial, name="Dataset_geographical_coverage", curie=DCTERMS.curie('spatial'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_geographical_coverage, domain=Dataset, range=Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]])

slots.Dataset_has_version = Slot(uri=DCAT.hasVersion, name="Dataset_has_version", curie=DCAT.curie('hasVersion'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_has_version, domain=Dataset, range=Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]])

slots.Dataset_identifier = Slot(uri=DCTERMS.identifier, name="Dataset_identifier", curie=DCTERMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_identifier, domain=Dataset, range=Optional[Union[str, list[str]]])

slots.Dataset_in_series = Slot(uri=DCAT.inSeries, name="Dataset_in_series", curie=DCAT.curie('inSeries'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_in_series, domain=Dataset, range=Optional[Union[Union[dict, "DatasetSeries"], list[Union[dict, "DatasetSeries"]]]])

slots.Dataset_is_referenced_by = Slot(uri=DCTERMS.isReferencedBy, name="Dataset_is_referenced_by", curie=DCTERMS.curie('isReferencedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_is_referenced_by, domain=Dataset, range=Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]])

slots.Dataset_keyword = Slot(uri=DCAT.keyword, name="Dataset_keyword", curie=DCAT.curie('keyword'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_keyword, domain=Dataset, range=Optional[Union[str, list[str]]])

slots.Dataset_landing_page = Slot(uri=DCAT.landingPage, name="Dataset_landing_page", curie=DCAT.curie('landingPage'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_landing_page, domain=Dataset, range=Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]])

slots.Dataset_language = Slot(uri=DCTERMS.language, name="Dataset_language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_language, domain=Dataset, range=Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]])

slots.Dataset_modification_date = Slot(uri=DCTERMS.modified, name="Dataset_modification_date", curie=DCTERMS.curie('modified'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_modification_date, domain=Dataset, range=Optional[Union[str, XSDDate]])

slots.Dataset_other_identifier = Slot(uri=ADMS.identifier, name="Dataset_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_other_identifier, domain=Dataset, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.Dataset_provenance = Slot(uri=DCTERMS.provenance, name="Dataset_provenance", curie=DCTERMS.curie('provenance'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_provenance, domain=Dataset, range=Optional[Union[Union[dict, "ProvenanceStatement"], list[Union[dict, "ProvenanceStatement"]]]])

slots.Dataset_publisher = Slot(uri=DCTERMS.publisher, name="Dataset_publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_publisher, domain=Dataset, range=Optional[Union[dict, Agent]])

slots.Dataset_qualified_attribution = Slot(uri=PROV.qualifiedAttribution, name="Dataset_qualified_attribution", curie=PROV.curie('qualifiedAttribution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_qualified_attribution, domain=Dataset, range=Optional[Union[Union[dict, "Attribution"], list[Union[dict, "Attribution"]]]])

slots.Dataset_qualified_relation = Slot(uri=DCAT.qualifiedRelation, name="Dataset_qualified_relation", curie=DCAT.curie('qualifiedRelation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_qualified_relation, domain=Dataset, range=Optional[Union[Union[dict, "Relationship"], list[Union[dict, "Relationship"]]]])

slots.Dataset_related_resource = Slot(uri=DCTERMS.relation, name="Dataset_related_resource", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_related_resource, domain=Dataset, range=Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]])

slots.Dataset_release_date = Slot(uri=DCTERMS.issued, name="Dataset_release_date", curie=DCTERMS.curie('issued'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_release_date, domain=Dataset, range=Optional[Union[str, XSDDate]])

slots.Dataset_sample = Slot(uri=ADMS.sample, name="Dataset_sample", curie=ADMS.curie('sample'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_sample, domain=Dataset, range=Optional[Union[Union[dict, "Distribution"], list[Union[dict, "Distribution"]]]])

slots.Dataset_source = Slot(uri=DCTERMS.source, name="Dataset_source", curie=DCTERMS.curie('source'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_source, domain=Dataset, range=Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]])

slots.Dataset_spatial_resolution = Slot(uri=DCAT.spatialResolutionInMeters, name="Dataset_spatial_resolution", curie=DCAT.curie('spatialResolutionInMeters'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_spatial_resolution, domain=Dataset, range=Optional[Decimal])

slots.Dataset_temporal_coverage = Slot(uri=DCTERMS.temporal, name="Dataset_temporal_coverage", curie=DCTERMS.curie('temporal'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_temporal_coverage, domain=Dataset, range=Optional[Union[Union[dict, "PeriodOfTime"], list[Union[dict, "PeriodOfTime"]]]])

slots.Dataset_temporal_resolution = Slot(uri=DCAT.temporalResolution, name="Dataset_temporal_resolution", curie=DCAT.curie('temporalResolution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_temporal_resolution, domain=Dataset, range=Optional[str])

slots.Dataset_theme = Slot(uri=DCAT.theme, name="Dataset_theme", curie=DCAT.curie('theme'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_theme, domain=Dataset, range=Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]])

slots.Dataset_title = Slot(uri=DCTERMS.title, name="Dataset_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_title, domain=Dataset, range=Union[str, list[str]])

slots.Dataset_type = Slot(uri=DCTERMS.type, name="Dataset_type", curie=DCTERMS.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_type, domain=Dataset, range=Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]])

slots.Dataset_version = Slot(uri=DCAT.version, name="Dataset_version", curie=DCAT.curie('version'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_version, domain=Dataset, range=Optional[str])

slots.Dataset_version_notes = Slot(uri=ADMS.versionNotes, name="Dataset_version_notes", curie=ADMS.curie('versionNotes'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_version_notes, domain=Dataset, range=Optional[Union[str, list[str]]])

slots.Dataset_was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="Dataset_was_generated_by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Dataset_was_generated_by, domain=Dataset, range=Union[dict[Union[str, DataGeneratingActivityId], Union[dict, DataGeneratingActivity]], list[Union[dict, DataGeneratingActivity]]])

slots.DatasetSeries_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="DatasetSeries_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_applicable_legislation, domain=DatasetSeries, range=Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]])

slots.DatasetSeries_contact_point = Slot(uri=DCAT.contactPoint, name="DatasetSeries_contact_point", curie=DCAT.curie('contactPoint'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_contact_point, domain=DatasetSeries, range=Optional[Union[Union[dict, "Kind"], list[Union[dict, "Kind"]]]])

slots.DatasetSeries_description = Slot(uri=DCTERMS.description, name="DatasetSeries_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_description, domain=DatasetSeries, range=Union[str, list[str]])

slots.DatasetSeries_frequency = Slot(uri=DCTERMS.accrualPeriodicity, name="DatasetSeries_frequency", curie=DCTERMS.curie('accrualPeriodicity'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_frequency, domain=DatasetSeries, range=Optional[Union[dict, "Frequency"]])

slots.DatasetSeries_geographical_coverage = Slot(uri=DCTERMS.spatial, name="DatasetSeries_geographical_coverage", curie=DCTERMS.curie('spatial'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_geographical_coverage, domain=DatasetSeries, range=Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]])

slots.DatasetSeries_modification_date = Slot(uri=DCTERMS.modified, name="DatasetSeries_modification_date", curie=DCTERMS.curie('modified'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_modification_date, domain=DatasetSeries, range=Optional[Union[str, XSDDate]])

slots.DatasetSeries_publisher = Slot(uri=DCTERMS.publisher, name="DatasetSeries_publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_publisher, domain=DatasetSeries, range=Optional[Union[dict, Agent]])

slots.DatasetSeries_release_date = Slot(uri=DCTERMS.issued, name="DatasetSeries_release_date", curie=DCTERMS.curie('issued'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_release_date, domain=DatasetSeries, range=Optional[Union[str, XSDDate]])

slots.DatasetSeries_temporal_coverage = Slot(uri=DCTERMS.temporal, name="DatasetSeries_temporal_coverage", curie=DCTERMS.curie('temporal'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_temporal_coverage, domain=DatasetSeries, range=Optional[Union[Union[dict, "PeriodOfTime"], list[Union[dict, "PeriodOfTime"]]]])

slots.DatasetSeries_title = Slot(uri=DCTERMS.title, name="DatasetSeries_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DatasetSeries_title, domain=DatasetSeries, range=Union[str, list[str]])

slots.DefinedTerm_title = Slot(uri=SCHEMA.name, name="DefinedTerm_title", curie=SCHEMA.curie('name'),
                   model_uri=HEALTH_DCAT_AP_PLUS.DefinedTerm_title, domain=DefinedTerm, range=Optional[str])

slots.Device_has_part = Slot(uri=DCTERMS.hasPart, name="Device_has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Device_has_part, domain=Device, range=Optional[Union[dict[Union[str, DeviceId], Union[dict, "Device"]], list[Union[dict, "Device"]]]])

slots.Device_other_identifier = Slot(uri=ADMS.identifier, name="Device_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Device_other_identifier, domain=Device, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.Distribution_access_URL = Slot(uri=DCAT.accessURL, name="Distribution_access_URL", curie=DCAT.curie('accessURL'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_access_URL, domain=Distribution, range=Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]])

slots.Distribution_access_service = Slot(uri=DCAT.accessService, name="Distribution_access_service", curie=DCAT.curie('accessService'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_access_service, domain=Distribution, range=Optional[Union[Union[dict, DataService], list[Union[dict, DataService]]]])

slots.Distribution_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="Distribution_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_applicable_legislation, domain=Distribution, range=Optional[Union[dict[Union[str, LegalResourceId], Union[dict, "LegalResource"]], list[Union[dict, "LegalResource"]]]])

slots.Distribution_availability = Slot(uri=DCATAP.availability, name="Distribution_availability", curie=DCATAP.curie('availability'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_availability, domain=Distribution, range=Optional[Union[dict, "Concept"]])

slots.Distribution_byte_size = Slot(uri=DCAT.byteSize, name="Distribution_byte_size", curie=DCAT.curie('byteSize'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_byte_size, domain=Distribution, range=Optional[int])

slots.Distribution_checksum = Slot(uri=SPDX.checksum, name="Distribution_checksum", curie=SPDX.curie('checksum'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_checksum, domain=Distribution, range=Optional[Union[dict, Checksum]])

slots.Distribution_compression_format = Slot(uri=DCAT.compressFormat, name="Distribution_compression_format", curie=DCAT.curie('compressFormat'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_compression_format, domain=Distribution, range=Optional[Union[dict, "MediaType"]])

slots.Distribution_description = Slot(uri=DCTERMS.description, name="Distribution_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_description, domain=Distribution, range=Optional[Union[str, list[str]]])

slots.Distribution_documentation = Slot(uri=FOAF.page, name="Distribution_documentation", curie=FOAF.curie('page'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_documentation, domain=Distribution, range=Optional[Union[dict[Union[str, DocumentId], Union[dict, "Document"]], list[Union[dict, "Document"]]]])

slots.Distribution_download_URL = Slot(uri=DCAT.downloadURL, name="Distribution_download_URL", curie=DCAT.curie('downloadURL'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_download_URL, domain=Distribution, range=Optional[Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]]])

slots.Distribution_format = Slot(uri=DCTERMS.format, name="Distribution_format", curie=DCTERMS.curie('format'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_format, domain=Distribution, range=Optional[Union[dict, "MediaTypeOrExtent"]])

slots.Distribution_has_policy = Slot(uri=ODRL.hasPolicy, name="Distribution_has_policy", curie=ODRL.curie('hasPolicy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_has_policy, domain=Distribution, range=Optional[Union[dict, "Policy"]])

slots.Distribution_language = Slot(uri=DCTERMS.language, name="Distribution_language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_language, domain=Distribution, range=Optional[Union[Union[dict, "LinguisticSystem"], list[Union[dict, "LinguisticSystem"]]]])

slots.Distribution_licence = Slot(uri=DCTERMS.license, name="Distribution_licence", curie=DCTERMS.curie('license'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_licence, domain=Distribution, range=Optional[Union[dict, "LicenseDocument"]])

slots.Distribution_linked_schemas = Slot(uri=DCTERMS.conformsTo, name="Distribution_linked_schemas", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_linked_schemas, domain=Distribution, range=Optional[Union[Union[dict, "Standard"], list[Union[dict, "Standard"]]]])

slots.Distribution_media_type = Slot(uri=DCAT.mediaType, name="Distribution_media_type", curie=DCAT.curie('mediaType'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_media_type, domain=Distribution, range=Optional[Union[dict, "MediaType"]])

slots.Distribution_modification_date = Slot(uri=DCTERMS.modified, name="Distribution_modification_date", curie=DCTERMS.curie('modified'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_modification_date, domain=Distribution, range=Optional[Union[str, XSDDate]])

slots.Distribution_packaging_format = Slot(uri=DCAT.packageFormat, name="Distribution_packaging_format", curie=DCAT.curie('packageFormat'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_packaging_format, domain=Distribution, range=Optional[Union[dict, "MediaType"]])

slots.Distribution_release_date = Slot(uri=DCTERMS.issued, name="Distribution_release_date", curie=DCTERMS.curie('issued'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_release_date, domain=Distribution, range=Optional[Union[str, XSDDate]])

slots.Distribution_rights = Slot(uri=DCTERMS.rights, name="Distribution_rights", curie=DCTERMS.curie('rights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_rights, domain=Distribution, range=Optional[Union[dict, "RightsStatement"]])

slots.Distribution_spatial_resolution = Slot(uri=DCAT.spatialResolutionInMeters, name="Distribution_spatial_resolution", curie=DCAT.curie('spatialResolutionInMeters'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_spatial_resolution, domain=Distribution, range=Optional[Decimal])

slots.Distribution_status = Slot(uri=ADMS.status, name="Distribution_status", curie=ADMS.curie('status'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_status, domain=Distribution, range=Optional[Union[dict, "Concept"]])

slots.Distribution_temporal_resolution = Slot(uri=DCAT.temporalResolution, name="Distribution_temporal_resolution", curie=DCAT.curie('temporalResolution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_temporal_resolution, domain=Distribution, range=Optional[str])

slots.Distribution_title = Slot(uri=DCTERMS.title, name="Distribution_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Distribution_title, domain=Distribution, range=Optional[Union[str, list[str]]])

slots.Entity_title = Slot(uri=DCTERMS.title, name="Entity_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Entity_title, domain=Entity, range=Optional[str])

slots.Entity_description = Slot(uri=DCTERMS.description, name="Entity_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Entity_description, domain=Entity, range=Optional[str])

slots.Entity_other_identifier = Slot(uri=ADMS.identifier, name="Entity_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Entity_other_identifier, domain=Entity, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.Entity_has_part = Slot(uri=DCTERMS.hasPart, name="Entity_has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Entity_has_part, domain=Entity, range=Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]])

slots.Entity_part_of = Slot(uri=DCTERMS.isPartOf, name="Entity_part_of", curie=DCTERMS.curie('isPartOf'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Entity_part_of, domain=Entity, range=Optional[Union[dict[Union[str, EntityId], Union[dict, "Entity"]], list[Union[dict, "Entity"]]]])

slots.EvaluatedActivity_other_identifier = Slot(uri=ADMS.identifier, name="EvaluatedActivity_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.EvaluatedActivity_other_identifier, domain=EvaluatedActivity, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.EvaluatedEntity_title = Slot(uri=DCTERMS.title, name="EvaluatedEntity_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.EvaluatedEntity_title, domain=EvaluatedEntity, range=Optional[str])

slots.EvaluatedEntity_description = Slot(uri=DCTERMS.description, name="EvaluatedEntity_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.EvaluatedEntity_description, domain=EvaluatedEntity, range=Optional[str])

slots.EvaluatedEntity_was_generated_by = Slot(uri=PROV.wasGeneratedBy, name="EvaluatedEntity_was_generated_by", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=HEALTH_DCAT_AP_PLUS.EvaluatedEntity_was_generated_by, domain=EvaluatedEntity, range=Optional[Union[dict[Union[str, ActivityId], Union[dict, Activity]], list[Union[dict, Activity]]]])

slots.EvaluatedEntity_other_identifier = Slot(uri=ADMS.identifier, name="EvaluatedEntity_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.EvaluatedEntity_other_identifier, domain=EvaluatedEntity, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.Identifier_notation = Slot(uri=SKOS.notation, name="Identifier_notation", curie=SKOS.curie('notation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Identifier_notation, domain=Identifier, range=str)

slots.LicenseDocument_type = Slot(uri=DCTERMS.type, name="LicenseDocument_type", curie=DCTERMS.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.LicenseDocument_type, domain=LicenseDocument, range=Optional[Union[Union[dict, Concept], list[Union[dict, Concept]]]])

slots.Location_bbox = Slot(uri=DCAT.bbox, name="Location_bbox", curie=DCAT.curie('bbox'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Location_bbox, domain=Location, range=Optional[str])

slots.Location_centroid = Slot(uri=DCAT.centroid, name="Location_centroid", curie=DCAT.curie('centroid'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Location_centroid, domain=Location, range=Optional[str])

slots.Location_geometry = Slot(uri=LOCN.geometry, name="Location_geometry", curie=LOCN.curie('geometry'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Location_geometry, domain=Location, range=Optional[Union[dict, "Geometry"]])

slots.PeriodOfTime_beginning = Slot(uri=TIME.hasBeginning, name="PeriodOfTime_beginning", curie=TIME.curie('hasBeginning'),
                   model_uri=HEALTH_DCAT_AP_PLUS.PeriodOfTime_beginning, domain=PeriodOfTime, range=Optional[Union[dict, "TimeInstant"]])

slots.PeriodOfTime_end = Slot(uri=TIME.hasEnd, name="PeriodOfTime_end", curie=TIME.curie('hasEnd'),
                   model_uri=HEALTH_DCAT_AP_PLUS.PeriodOfTime_end, domain=PeriodOfTime, range=Optional[Union[dict, "TimeInstant"]])

slots.PeriodOfTime_end_date = Slot(uri=DCAT.endDate, name="PeriodOfTime_end_date", curie=DCAT.curie('endDate'),
                   model_uri=HEALTH_DCAT_AP_PLUS.PeriodOfTime_end_date, domain=PeriodOfTime, range=Optional[Union[str, XSDDate]])

slots.PeriodOfTime_start_date = Slot(uri=DCAT.startDate, name="PeriodOfTime_start_date", curie=DCAT.curie('startDate'),
                   model_uri=HEALTH_DCAT_AP_PLUS.PeriodOfTime_start_date, domain=PeriodOfTime, range=Optional[Union[str, XSDDate]])

slots.QualitativeAttribute_value = Slot(uri=PROV.value, name="QualitativeAttribute_value", curie=PROV.curie('value'),
                   model_uri=HEALTH_DCAT_AP_PLUS.QualitativeAttribute_value, domain=QualitativeAttribute, range=str)

slots.QuantitativeAttribute_value = Slot(uri=PROV.value, name="QuantitativeAttribute_value", curie=PROV.curie('value'),
                   model_uri=HEALTH_DCAT_AP_PLUS.QuantitativeAttribute_value, domain=QuantitativeAttribute, range=float)

slots.Relationship_had_role = Slot(uri=DCAT.hadRole, name="Relationship_had_role", curie=DCAT.curie('hadRole'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Relationship_had_role, domain=Relationship, range=Union[Union[dict, "Role"], list[Union[dict, "Role"]]])

slots.Relationship_relation = Slot(uri=DCTERMS.relation, name="Relationship_relation", curie=DCTERMS.curie('relation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Relationship_relation, domain=Relationship, range=Union[dict[Union[str, ResourceId], Union[dict, "Resource"]], list[Union[dict, "Resource"]]])

slots.Software_has_part = Slot(uri=DCTERMS.hasPart, name="Software_has_part", curie=DCTERMS.curie('hasPart'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Software_has_part, domain=Software, range=Optional[Union[dict[Union[str, SoftwareId], Union[dict, "Software"]], list[Union[dict, "Software"]]]])

slots.Software_other_identifier = Slot(uri=ADMS.identifier, name="Software_other_identifier", curie=ADMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Software_other_identifier, domain=Software, range=Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]])

slots.HealthCatalogue_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="HealthCatalogue_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthCatalogue_applicable_legislation, domain=HealthCatalogue, range=Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]])

slots.HealthCatalogue_language = Slot(uri=DCTERMS.language, name="HealthCatalogue_language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthCatalogue_language, domain=HealthCatalogue, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthCatalogue_publisher = Slot(uri=DCTERMS.publisher, name="HealthCatalogue_publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthCatalogue_publisher, domain=HealthCatalogue, range=Union[str, URIorCURIE])

slots.HealthCatalogue_geographical_coverage = Slot(uri=DCTERMS.spatial, name="HealthCatalogue_geographical_coverage", curie=DCTERMS.curie('spatial'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthCatalogue_geographical_coverage, domain=HealthCatalogue, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.Column_name = Slot(uri=FOAF.name, name="Column_name", curie=FOAF.curie('name'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Column_name, domain=Column, range=Union[str, list[str]])

slots.Column_description = Slot(uri=DCTERMS.description, name="Column_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Column_description, domain=Column, range=Union[str, list[str]])

slots.HealthDataset_access_rights = Slot(uri=DCTERMS.accessRights, name="HealthDataset_access_rights", curie=DCTERMS.curie('accessRights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_access_rights, domain=HealthDataset, range=Union[str, URIorCURIE])

slots.HealthDataset_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="HealthDataset_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_applicable_legislation, domain=HealthDataset, range=Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]])

slots.HealthDataset_dataset_distribution = Slot(uri=DCAT.distribution, name="HealthDataset_dataset_distribution", curie=DCAT.curie('distribution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_dataset_distribution, domain=HealthDataset, range=Union[Union[dict, "HealthDistribution"], list[Union[dict, "HealthDistribution"]]])

slots.HealthDataset_identifier = Slot(uri=DCTERMS.identifier, name="HealthDataset_identifier", curie=DCTERMS.curie('identifier'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_identifier, domain=HealthDataset, range=Union[str, list[str]])

slots.HealthDataset_publisher = Slot(uri=DCTERMS.publisher, name="HealthDataset_publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_publisher, domain=HealthDataset, range=Optional[Union[dict, "HealthPublisherAgent"]])

slots.HealthDataset_sample = Slot(uri=ADMS.sample, name="HealthDataset_sample", curie=ADMS.curie('sample'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_sample, domain=HealthDataset, range=Optional[Union[Union[dict, "HealthDistribution"], list[Union[dict, "HealthDistribution"]]]])

slots.HealthDataset_theme = Slot(uri=DCAT.theme, name="HealthDataset_theme", curie=DCAT.curie('theme'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_theme, domain=HealthDataset, range=Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]])

slots.HealthDataset_contact_point = Slot(uri=DCAT.contactPoint, name="HealthDataset_contact_point", curie=DCAT.curie('contactPoint'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_contact_point, domain=HealthDataset, range=Union[Union[dict, "HealthKind"], list[Union[dict, "HealthKind"]]])

slots.HealthDataset_keyword = Slot(uri=DCAT.keyword, name="HealthDataset_keyword", curie=DCAT.curie('keyword'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_keyword, domain=HealthDataset, range=Union[str, list[str]])

slots.HealthDataset_type = Slot(uri=DCTERMS.type, name="HealthDataset_type", curie=DCTERMS.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_type, domain=HealthDataset, range=Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]])

slots.HealthDataset_provenance = Slot(uri=DCTERMS.provenance, name="HealthDataset_provenance", curie=DCTERMS.curie('provenance'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_provenance, domain=HealthDataset, range=Union[Union[dict, ProvenanceStatement], list[Union[dict, ProvenanceStatement]]])

slots.HealthDataset_frequency = Slot(uri=DCTERMS.accrualPeriodicity, name="HealthDataset_frequency", curie=DCTERMS.curie('accrualPeriodicity'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_frequency, domain=HealthDataset, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDataset_source = Slot(uri=DCTERMS.source, name="HealthDataset_source", curie=DCTERMS.curie('source'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_source, domain=HealthDataset, range=Optional[Union[dict[Union[str, HealthDatasetId], Union[dict, "HealthDataset"]], list[Union[dict, "HealthDataset"]]]])

slots.HealthDataset_temporal_resolution = Slot(uri=DCAT.temporalResolution, name="HealthDataset_temporal_resolution", curie=DCAT.curie('temporalResolution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_temporal_resolution, domain=HealthDataset, range=Optional[Union[str, list[str]]])

slots.HealthDataset_language = Slot(uri=DCTERMS.language, name="HealthDataset_language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_language, domain=HealthDataset, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDataset_geographical_coverage = Slot(uri=DCTERMS.spatial, name="HealthDataset_geographical_coverage", curie=DCTERMS.curie('spatial'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_geographical_coverage, domain=HealthDataset, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDataset_health_category = Slot(uri=HEALTHDCATAP.healthCategory, name="HealthDataset_health_category", curie=HEALTHDCATAP.curie('healthCategory'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_health_category, domain=HealthDataset, range=Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]])

slots.HealthDataset_has_coding_system = Slot(uri=HEALTHDCATAP.hasCodingSystem, name="HealthDataset_has_coding_system", curie=HEALTHDCATAP.curie('hasCodingSystem'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_has_coding_system, domain=HealthDataset, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDataset_conforms_to = Slot(uri=DCTERMS.conformsTo, name="HealthDataset_conforms_to", curie=DCTERMS.curie('conformsTo'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_conforms_to, domain=HealthDataset, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDataset_health_theme = Slot(uri=HEALTHDCATAP.healthTheme, name="HealthDataset_health_theme", curie=HEALTHDCATAP.curie('healthTheme'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_health_theme, domain=HealthDataset, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDataset_qualified_attribution = Slot(uri=PROV.qualifiedAttribution, name="HealthDataset_qualified_attribution", curie=PROV.curie('qualifiedAttribution'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataset_qualified_attribution, domain=HealthDataset, range=Optional[Union[Union[dict, "DatasetAttribution"], list[Union[dict, "DatasetAttribution"]]]])

slots.HealthDatasetSeries_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="HealthDatasetSeries_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDatasetSeries_applicable_legislation, domain=HealthDatasetSeries, range=Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]])

slots.HealthDistribution_applicable_legislation = Slot(uri=DCATAP.applicableLegislation, name="HealthDistribution_applicable_legislation", curie=DCATAP.curie('applicableLegislation'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDistribution_applicable_legislation, domain=HealthDistribution, range=Union[dict[Union[str, LegalResourceId], Union[dict, LegalResource]], list[Union[dict, LegalResource]]])

slots.HealthDistribution_format = Slot(uri=DCTERMS.format, name="HealthDistribution_format", curie=DCTERMS.curie('format'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDistribution_format, domain=HealthDistribution, range=Optional[Union[str, URIorCURIE]])

slots.HealthDistribution_language = Slot(uri=DCTERMS.language, name="HealthDistribution_language", curie=DCTERMS.curie('language'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDistribution_language, domain=HealthDistribution, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDistribution_status = Slot(uri=ADMS.status, name="HealthDistribution_status", curie=ADMS.curie('status'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDistribution_status, domain=HealthDistribution, range=Optional[Union[str, URIorCURIE]])

slots.HealthDistribution_availability = Slot(uri=DCATAP.availability, name="HealthDistribution_availability", curie=DCATAP.curie('availability'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDistribution_availability, domain=HealthDistribution, range=Optional[Union[str, URIorCURIE]])

slots.Table_title = Slot(uri=DCTERMS.title, name="Table_title", curie=DCTERMS.curie('title'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Table_title, domain=Table, range=Union[str, list[str]])

slots.Table_keyword = Slot(uri=DCAT.keyword, name="Table_keyword", curie=DCAT.curie('keyword'),
                   model_uri=HEALTH_DCAT_AP_PLUS.Table_keyword, domain=Table, range=Optional[Union[str, list[str]]])

slots.TemporalEntity_description = Slot(uri=DCTERMS.description, name="TemporalEntity_description", curie=DCTERMS.curie('description'),
                   model_uri=HEALTH_DCAT_AP_PLUS.TemporalEntity_description, domain=TemporalEntity, range=Union[str, list[str]])

slots.TemporalEntity_frequency = Slot(uri=DCTERMS.accrualPeriodicity, name="TemporalEntity_frequency", curie=DCTERMS.curie('accrualPeriodicity'),
                   model_uri=HEALTH_DCAT_AP_PLUS.TemporalEntity_frequency, domain=TemporalEntity, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthLicenseDocument_type = Slot(uri=DCTERMS.type, name="HealthLicenseDocument_type", curie=DCTERMS.curie('type'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthLicenseDocument_type, domain=HealthLicenseDocument, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.HealthDataService_access_rights = Slot(uri=DCTERMS.accessRights, name="HealthDataService_access_rights", curie=DCTERMS.curie('accessRights'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataService_access_rights, domain=HealthDataService, range=Optional[Union[str, URIorCURIE]])

slots.HealthDataService_format = Slot(uri=DCTERMS.format, name="HealthDataService_format", curie=DCTERMS.curie('format'),
                   model_uri=HEALTH_DCAT_AP_PLUS.HealthDataService_format, domain=HealthDataService, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

# Maritime Manufacturing Metadata Design

## 1. Purpose and Scope

The Maritime Manufacturing Metadata Catalog demonstrates a structured approach to organizing, classifying, validating, and retrieving manufacturing metadata.

The system consists of two complementary metadata models:

- A component catalog for describing and classifying maritime manufacturing components.
- A manufacturing knowledge graph for representing relationships between facilities, production cells, machines, sensors, and industrial signals.

All manufacturing data is synthetic and does not represent proprietary information or actual manufacturing operations.

## 2. Metadata Standards

The system uses established metadata and semantic web standards to promote consistency, interoperability, and maintainability.

| Standard | Application |
|---|---|
| JSON | Component metadata schema definition |
| Dublin Core | Standardized descriptive metadata |
| RDF | Representation of entities and relationships |
| RDFS | Class hierarchies, labels, domains, and ranges |
| SKOS | Controlled vocabularies and hierarchical classification |
| OWL | Formal ontology modeling and semantic inference |
| SPARQL | Metadata retrieval and relationship traversal |
| SHACL | RDF graph validation and constraint enforcement |
| Turtle | Human-readable RDF serialization |

## 3. Component Metadata Schema

The component metadata schema is defined in `metadata/schema.json`.

**Schema name:** Maritime Component Metadata  
**Version:** 1.0

| Field | Data Type | Required | Purpose |
|---|---|---|---|
| component_id | String | Yes | Unique component identifier |
| name | String | Yes | Standardized component name |
| category | String | Yes | Primary classification |
| subcategory | String | Yes | More specific classification |
| manufacturer | String | No | Component manufacturer |
| status | String | Yes | Component lifecycle status |

Permitted lifecycle statuses are:

- Active
- Discontinued
- Under Review

Component identifiers must be unique. Required fields must be populated, and category and subcategory assignments must conform to the controlled vocabulary.

Manufacturer information is optional to accommodate records for which manufacturer information is unavailable.

The schema is a project-specific JSON metadata specification. Validation is implemented through Python rather than a formal JSON Schema validation engine.

## 4. Controlled Vocabulary and Taxonomy

The component classification system is represented using SKOS in `metadata/taxonomy.ttl`.

The taxonomy contains one concept scheme, four top-level categories, and eight subcategories.

| Category | Subcategories |
|---|---|
| Propulsion | Electric Motors, Propellers |
| Electrical | Batteries, Controllers |
| Structural | Brackets, Hull Panels |
| Navigation | GPS Systems, Sensors |

The taxonomy uses the following SKOS properties:

| Property | Purpose |
|---|---|
| skos:ConceptScheme | Defines the overall classification scheme |
| skos:Concept | Represents an individual classification concept |
| skos:prefLabel | Defines the preferred human-readable label |
| skos:broader | Identifies a broader classification concept |
| skos:narrower | Identifies a narrower classification concept |
| skos:inScheme | Associates a concept with its concept scheme |
| skos:topConceptOf | Identifies a top-level concept within a scheme |
| skos:hasTopConcept | Associates a scheme with its top-level concepts |

The controlled vocabulary separates classification concepts from individual component records. This allows multiple records to reference the same standardized classification without independently defining category meanings.

Category and subcategory combinations are validated against the taxonomy to prevent inconsistent classification.

The taxonomy is intentionally limited in scope and can be extended as additional component classifications are introduced.

## 5. RDF Representation

RDF represents metadata as subject-predicate-object triples.

The project uses the following namespace for project-specific entities and properties:

`https://example.org/maritime/`

This namespace is intended for demonstration purposes and is not a production identifier service.

Dublin Core and RDFS properties are reused where appropriate rather than creating unnecessary project-specific equivalents.

Examples include:

- `dcterms:identifier` for entity identifiers.
- `dcterms:description` for descriptive information.
- `rdfs:label` for human-readable entity names.

The component catalog and manufacturing equipment graph are maintained as separate RDF datasets.

## 6. Manufacturing Ontology

The manufacturing ontology is defined in `metadata/manufacturing_ontology.ttl` and was developed using Protégé.

**Ontology IRI:** `https://example.org/maritime/ontology`

### 6.1 Class Definitions

| Class | Definition |
|---|---|
| PhysicalAsset | General class representing physical manufacturing assets |
| Facility | Manufacturing site containing production cells |
| ProductionCell | Manufacturing area containing machines |
| Machine | Physical equipment used in manufacturing operations |
| Sensor | Physical device associated with a machine |
| IndustrialSignal | Information generated by a sensor |

### 6.2 Class Hierarchy

```text
owl:Thing
├── PhysicalAsset
│   ├── Facility
│   ├── ProductionCell
│   ├── Machine
│   └── Sensor
└── IndustrialSignal
```

Facilities, production cells, machines, and sensors are subclasses of PhysicalAsset.

IndustrialSignal is modeled separately because a signal represents information rather than a physical manufacturing asset.

The class hierarchy represents classification relationships, not physical containment. Physical containment is represented through object properties.

### 6.3 Object Properties

| Property | Domain | Range | Purpose |
|---|---|---|---|
| partOf | PhysicalAsset | PhysicalAsset | Represents physical asset membership |
| locatedAt | Machine | ProductionCell | Identifies a machine's production location |
| generatedBy | IndustrialSignal | Sensor | Identifies the sensor responsible for a signal |

Object properties connect RDF entities to other RDF entities.

The general domain and range of `partOf` allow the property to be reused across multiple levels of the manufacturing hierarchy.

### 6.4 Datatype Properties

| Property | Domain | Range |
|---|---|---|
| assetIdentifier | PhysicalAsset | xsd:string |
| signalIdentifier | IndustrialSignal | xsd:string |
| measurementUnit | IndustrialSignal | xsd:string |

Datatype properties associate entities with literal values.

Although the ontology defines `assetIdentifier` and `signalIdentifier`, the current equipment graph uses `dcterms:identifier` for both physical assets and industrial signals.

The custom identifier properties are currently unused. Future revisions should determine whether to retain, align, or remove these properties to avoid redundant identifier representations.

### 6.5 Logical Restrictions

The ontology defines the following existential restrictions:

| Class | Restriction |
|---|---|
| IndustrialSignal | generatedBy some Sensor |
| Sensor | partOf some Machine |
| Machine | locatedAt some ProductionCell |
| ProductionCell | partOf some Facility |

These restrictions express the intended semantic relationships between manufacturing entities.

For example, an IndustrialSignal must be generated by at least one Sensor under the ontology's interpretation.

Existential restrictions do not require that the corresponding relationship be explicitly recorded in an RDF dataset. Explicit metadata completeness is enforced separately through SHACL.

### 6.6 Class Disjointness

The ontology defines IndustrialSignal and PhysicalAsset as disjoint classes.

Facility, ProductionCell, Machine, and Sensor are also mutually disjoint.

These axioms establish that an individual cannot simultaneously belong to incompatible manufacturing classes.

Disjointness supports logical consistency checking and helps identify contradictory classifications.

## 7. Manufacturing Relationship Model

The equipment graph represents the following manufacturing relationship structure:

```text
IndustrialSignal
    │ generatedBy
    ▼
Sensor
    │ partOf
    ▼
Machine
    │ partOf / locatedAt
    ▼
ProductionCell
    │ partOf
    ▼
Facility
```

This relationship model supports tracing industrial signals to their physical equipment origins and manufacturing locations.

For example, a signal can be associated with its generating sensor, the machine containing that sensor, the production cell containing that machine, and the corresponding facility.

SPARQL queries enable this relationship traversal without duplicating the complete manufacturing hierarchy in each signal record.

## 8. Semantic Reasoning

The system uses OWL-RL reasoning to derive implicit information from the ontology and equipment graph.

Reasoning supports:

- Inferring PhysicalAsset membership from subclass relationships.
- Inferring entity classifications from property domains and ranges.
- Deriving additional semantic relationships supported by the ontology.

The ontology was also developed and evaluated using the HermiT reasoner in Protégé.

OWL-RL inference is implemented separately from SHACL validation. The inferred graph is not used as a replacement for explicitly recorded manufacturing metadata.

## 9. Metadata Validation

The project implements two complementary validation approaches.

### 9.1 Component Metadata Validation

Python-based validation checks component records for:

- Missing required fields.
- Duplicate component identifiers.
- Invalid lifecycle statuses.
- Invalid category and subcategory relationships.

Invalid component records are excluded from the validated component catalog and documented in data quality reports.

### 9.2 Manufacturing Graph Validation

SHACL constraints are defined in `metadata/manufacturing_shapes.ttl`.

| Entity | Validation Requirements |
|---|---|
| Physical assets | Exactly one nonempty string identifier and label |
| Facility | No parent asset |
| ProductionCell | Exactly one parent facility |
| Machine | Exactly one parent production cell and matching location |
| Sensor | Exactly one parent machine |
| IndustrialSignal | Exactly one identifier, label, generating sensor, and measurement unit |

SHACL validation is performed without additional inference to evaluate explicitly recorded metadata.

Validation results are serialized as an RDF report in `metadata/shacl_validation_report.ttl`.

### 9.3 OWL and SHACL Responsibilities

OWL and SHACL serve different purposes.

OWL defines semantic meaning, logical relationships, and conditions for inference. Its open-world assumption allows information to exist even when it has not been explicitly recorded.

SHACL evaluates whether the recorded RDF data conforms to specified constraints.

For example, an industrial signal without a recorded `generatedBy` relationship does not necessarily create an OWL inconsistency. However, it violates the SHACL requirement that the relationship be explicitly present.

Using both standards separates semantic modeling from operational data quality requirements.

## 10. Design Principles

The metadata architecture follows these principles:

- **Consistency:** Standardized field definitions and controlled classification values.
- **Interoperability:** Reuse of established metadata and semantic web standards.
- **Traceability:** Explicit relationships between industrial signals and physical equipment.
- **Data integrity:** Automated validation of required metadata and relationships.
- **Maintainability:** Separation of schemas, taxonomies, ontologies, validation rules, and data processing scripts.
- **Extensibility:** Support for additional classifications, manufacturing entities, and validation requirements.
- **Reproducibility:** Script-based data processing and automated testing.

## 11. Limitations and Assumptions

The current implementation is a demonstration-scale metadata system rather than a production manufacturing platform.

Its limitations include:

- All manufacturing records are synthetic.
- The component taxonomy contains a limited number of classifications.
- The component catalog and equipment graph are separate datasets without explicit cross-dataset relationships.
- Manufacturing relationships assume a simplified, single-parent hierarchy.
- Measurement units are represented as strings rather than standardized unit vocabulary identifiers.
- SHACL constraints enforce the project's specified requirements rather than comprehensive manufacturing data governance policies.
- OWL-RL reasoning does not replace full OWL description logic consistency checking.

Future extensions should preserve the distinction between semantic definitions, operational validation requirements, and individual manufacturing records.

## 12. Related Metadata Resources

| File | Responsibility |
|---|---|
| metadata/schema.json | Component metadata specification |
| metadata/taxonomy.ttl | SKOS controlled vocabulary |
| metadata/catalog.ttl | Component RDF catalog |
| metadata/equipment_graph.ttl | Manufacturing equipment and signal relationships |
| metadata/manufacturing_ontology.ttl | OWL semantic model |
| metadata/manufacturing_shapes.ttl | SHACL validation constraints |
| metadata/shacl_validation_report.ttl | Structured graph validation results |

Changes to metadata definitions should be evaluated against existing data, validation rules, query functionality, and automated tests before being incorporated into the catalog.
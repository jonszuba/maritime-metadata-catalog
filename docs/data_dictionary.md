# Maritime Manufacturing Metadata Data Dictionary

## 1. Purpose

This data dictionary defines the metadata fields, identifier conventions, controlled values, relationships, and validation requirements used throughout the Maritime Manufacturing Metadata Catalog.

It serves as a reference for individuals responsible for maintaining, extending, validating, or consuming catalog metadata.

All records represent synthetic manufacturing data.

## 2. Dataset Inventory

| Dataset | Description |
|---|---|
| raw_components.csv | Original synthetic component records, including intentionally introduced metadata errors |
| standardized_components.csv | Component records following cleaning and standardization |
| valid_components.csv | Component records that satisfy validation requirements |
| equipment.csv | Physical manufacturing assets and their relationships |
| signals.csv | Industrial signals and their associated sensors |
| validation_report.csv | Record-level component validation errors |
| quality_summary.csv | Aggregated component quality metrics by category |

## 3. Component Metadata

Component metadata is governed by `metadata/schema.json`, version 1.0.

### 3.1 Field Definitions

| Field | Data Type | Required | Definition | Example |
|---|---|---|---|---|
| component_id | String | Yes | Unique identifier assigned to a component record | CMP-0001 |
| name | String | Yes | Standardized descriptive component name | High-Torque Motor Model 350 |
| category | String | Yes | Primary component classification | Propulsion |
| subcategory | String | Yes | More specific classification within a category | Electric Motors |
| manufacturer | String | No | Organization responsible for manufacturing the component | NavTech |
| status | String | Yes | Component lifecycle or review status | Active |

### 3.2 Field Requirements

**component_id**

- Must be populated.
- Must be unique within the component dataset.
- Uses the identifier convention `CMP-NNNN`.
- Should remain stable when descriptive metadata changes.

**name**

- Must be populated.
- Should provide a recognizable description of the component.
- Does not need to be unique.

**category**

- Must be populated.
- Must match an approved top-level taxonomy concept.
- Must use the standardized preferred label.

**subcategory**

- Must be populated.
- Must correspond to a valid narrower concept under the assigned category.
- Must use the standardized preferred label.

**manufacturer**

- May be empty when manufacturer information is unavailable.
- Should use a consistent organization name.
- Is not currently governed by a controlled manufacturer vocabulary.

**status**

- Must be populated.
- Must match an approved lifecycle status.

## 4. Controlled Values

### 4.1 Component Classification

Component classifications are governed by the SKOS taxonomy in `metadata/taxonomy.ttl`.

| Category | Permitted Subcategories |
|---|---|
| Propulsion | Electric Motors, Propellers |
| Electrical | Batteries, Controllers |
| Structural | Brackets, Hull Panels |
| Navigation | GPS Systems, Sensors |

A valid subcategory must belong to its assigned category.

For example:

- Propulsion → Electric Motors: valid.
- Propulsion → Controllers: invalid.
- Electrical → Controllers: valid.

The classification hierarchy is enforced by checking the corresponding `skos:broader` relationship in the taxonomy graph.

### 4.2 Component Lifecycle Status

| Value | Intended Meaning |
|---|---|
| Active | Component is currently active within the catalog's modeled lifecycle |
| Discontinued | Component is no longer active within the modeled lifecycle |
| Under Review | Component requires further evaluation before its lifecycle status is finalized |

These definitions describe the intended interpretation of the controlled values. The current implementation validates permitted status values but does not enforce lifecycle transitions.

## 5. Equipment Metadata

Physical manufacturing assets are defined in `data/equipment.csv`.

### 5.1 Field Definitions

| Field | Data Type | Expected Population | Definition | Example |
|---|---|---|---|---|
| equipment_id | String | All assets | Unique identifier assigned to a physical asset | EQ-001 |
| name | String | All assets | Human-readable equipment name | Motor Testing Station |
| equipment_type | String | All assets | Physical asset classification | Machine |
| parent_id | String | Non-facility assets | Identifier of the immediate parent asset | CELL-001 |
| facility_id | String | Non-facility assets | Identifier of the associated manufacturing facility | FAC-001 |

### 5.2 Equipment Types

| Source Value | OWL Class | Identifier Convention |
|---|---|---|
| Facility | ex:Facility | FAC-NNN |
| Production Cell | ex:ProductionCell | CELL-NNN |
| Machine | ex:Machine | EQ-NNN |
| Sensor | ex:Sensor | SEN-NNN |

The source equipment type is mapped to the corresponding OWL class when the equipment graph is generated.

### 5.3 Parent Relationships

| Equipment Type | Permitted Immediate Parent |
|---|---|
| Facility | None |
| Production Cell | Facility |
| Machine | Production Cell |
| Sensor | Machine |

The equipment graph builder checks whether referenced parent identifiers exist in the equipment dataset.

SHACL validation additionally checks whether the referenced parent belongs to the correct manufacturing class and whether the required relationship cardinality is satisfied.

### 5.4 Facility Association

The `facility_id` field identifies the facility associated with a physical asset.

For the current dataset, all non-facility assets reference `FAC-001`.

The graph builder checks that populated facility identifiers reference existing equipment identifiers. However, the field is not directly serialized as an RDF relationship.

Facility membership can instead be retrieved by traversing the equipment containment hierarchy.

The current implementation does not independently verify that `facility_id` matches the facility reached through the complete parent hierarchy.

## 6. Industrial Signal Metadata

Industrial signal metadata is defined in `data/signals.csv`.

### 6.1 Field Definitions

| Field | Data Type | Expected Population | Definition | Example |
|---|---|---|---|---|
| signal_id | String | All signals | Unique catalog identifier assigned to a signal | SIG-001 |
| signal_name | String | All signals | Operational name or tag associated with a signal | PLC4_TT_1142 |
| sensor_id | String | All signals | Identifier of the sensor generating the signal | SEN-001 |
| unit | String | All signals | Measurement unit associated with the signal | Celsius |
| description | String | Recommended | Human-readable explanation of the signal's purpose | Motor operating temperature |

### 6.2 Signal Identifiers and Operational Names

The `signal_id` and `signal_name` fields serve different purposes.

- `signal_id` provides the catalog identifier used to construct the signal's RDF URI.
- `signal_name` provides the operational name used to describe and retrieve the signal.

For example:

| Attribute | Value |
|---|---|
| Catalog identifier | SIG-001 |
| Operational signal name | PLC4_TT_1142 |
| RDF URI | https://example.org/maritime/SIG-001 |
| Generating sensor | SEN-001 |
| Measurement unit | Celsius |

Operational signal names should not be substituted for catalog identifiers when constructing RDF entity references.

### 6.3 Measurement Units

The current dataset contains the following measurement units:

| Unit | Measurement |
|---|---|
| Celsius | Temperature |
| mm/s | Vibration velocity |
| mm | Position or displacement |

Measurement units are represented as string literals.

SHACL requires each industrial signal to have exactly one nonempty string measurement unit. It does not currently enforce a controlled unit vocabulary or validate compatibility between a measurement unit and a signal's measurement type.

### 6.4 Signal Relationships

Each industrial signal must reference exactly one generating sensor.

The graph builder verifies that the referenced equipment identifier exists. SHACL additionally verifies that the referenced entity is classified as a Sensor.

The signal description provides contextual information but is not currently required by the SHACL shapes.

## 7. Identifier Conventions

| Entity | Convention | Example |
|---|---|---|
| Component | CMP-NNNN | CMP-0001 |
| Facility | FAC-NNN | FAC-001 |
| Production Cell | CELL-NNN | CELL-001 |
| Machine | EQ-NNN | EQ-001 |
| Sensor | SEN-NNN | SEN-001 |
| Industrial Signal | SIG-NNN | SIG-001 |

Identifiers should remain stable throughout an entity's lifecycle.

The project uses the namespace:

`https://example.org/maritime/`

An equipment or signal identifier is appended to this namespace to construct its RDF URI.

Example:

`https://example.org/maritime/EQ-001`

Identifier prefixes and numeric lengths are conventions used by the current datasets. They are not enforced through regular-expression validation.

Component identifier uniqueness is checked by the Python validation system. The manufacturing SHACL shapes enforce one identifier value per targeted entity but do not independently enforce identifier uniqueness across all entities.

## 8. RDF Metadata Mappings

### 8.1 Equipment Metadata

| Source Field | RDF Representation |
|---|---|
| equipment_id | Entity URI and dcterms:identifier |
| name | rdfs:label |
| equipment_type | rdf:type |
| parent_id | ex:partOf |
| parent_id for machines | ex:locatedAt, in addition to ex:partOf |
| facility_id | Reference checked during graph construction; not directly serialized |

### 8.2 Industrial Signal Metadata

| Source Field | RDF Representation |
|---|---|
| signal_id | Entity URI and dcterms:identifier |
| signal_name | rdfs:label |
| sensor_id | ex:generatedBy |
| unit | ex:measurementUnit |
| description | dcterms:description |

Each signal is explicitly classified as `ex:IndustrialSignal` using `rdf:type`.

The use of standardized descriptive properties allows metadata to be represented consistently across manufacturing entity types.

## 9. Validation Report Metadata

### 9.1 Record-Level Validation Report

Component validation errors are recorded in `data/validation_report.csv`.

| Field | Data Type | Definition |
|---|---|---|
| component_id | String | Identifier of the component associated with the validation errors |
| errors | String | Human-readable description of one or more validation errors |

Multiple validation errors associated with the same record are separated by semicolons.

Example:

```text
CMP-0100,Missing required field: status; Invalid taxonomy relationship: Brackets does not belong under Electrical
```

### 9.2 Validation Error Types

| Error Type | Condition |
|---|---|
| Duplicate component ID | Identifier has already been encountered during validation |
| Missing required field | Required metadata is empty or absent |
| Invalid category | Category does not match an allowed value |
| Invalid status | Lifecycle status does not match an allowed value |
| Invalid taxonomy relationship | Subcategory does not belong to the assigned category |

Validation removes leading and trailing whitespace from field values before evaluating requirements.

A record can contain multiple validation errors.

## 10. Quality Summary Metadata

Aggregated component quality metrics are recorded in `data/quality_summary.csv`.

| Field | Data Type | Definition |
|---|---|---|
| category | String | Component classification being evaluated |
| total_records | Integer | Total number of component records in the category |
| invalid_records | Integer | Number of records that failed validation |
| valid_records | Integer | Number of records that passed validation |
| failure_rate_percent | Decimal | Percentage of records that failed validation |

### 10.1 Metric Definitions

Valid records:

`valid_records = total_records - invalid_records`

Failure rate:

`failure_rate_percent = (invalid_records / total_records) × 100`

### 10.2 Current Dataset Quality Summary

| Category | Total | Invalid | Valid | Failure Rate |
|---|---:|---:|---:|---:|
| Electrical | 248 | 11 | 237 | 4.44% |
| Navigation | 254 | 3 | 251 | 1.18% |
| Propulsion | 256 | 9 | 247 | 3.52% |
| Structural | 242 | 1 | 241 | 0.41% |
| Total | 1,000 | 24 | 976 | 2.40% |

The overall validation pass rate is 97.60%.

These metrics describe the quality of the current synthetic dataset. They do not represent the predictive accuracy of the validation system or the quality of actual manufacturing operations.

## 11. Manufacturing Graph Validation Report

Manufacturing graph validation results are stored in `metadata/shacl_validation_report.ttl`.

The report uses the SHACL validation report vocabulary.

| Property or Class | Purpose |
|---|---|
| sh:ValidationReport | Represents the overall validation report |
| sh:conforms | Indicates whether the data graph satisfies the shapes |
| sh:ValidationResult | Represents an individual validation result |
| sh:focusNode | Identifies the entity being evaluated |
| sh:resultPath | Identifies the property associated with a violation |
| sh:resultMessage | Provides a human-readable explanation |
| sh:resultSeverity | Indicates the severity of the validation result |
| sh:sourceConstraintComponent | Identifies the type of constraint responsible for a result |

Individual validation result properties are populated as applicable when violations occur.

The RDF report provides a machine-readable representation of graph validation results.

## 12. Metadata Governance and Maintenance

The following practices should be followed when maintaining the catalog:

- Preserve existing identifiers when updating descriptive metadata.
- Use approved preferred labels for controlled classifications.
- Update the schema and taxonomy when introducing new classifications.
- Maintain consistency between equipment types, ontology classes, and SHACL constraints.
- Distinguish catalog identifiers from operational signal names.
- Regenerate derived datasets and validation reports following source data changes.
- Execute automated tests before committing metadata model changes.
- Update this data dictionary whenever field definitions or validation requirements change.

## 13. Known Validation Limitations

The current implementation does not enforce every documented metadata convention.

Known limitations include:

- Identifier formatting conventions are not validated through regular expressions.
- Manufacturing identifier uniqueness is not independently enforced across entities.
- Manufacturer names are not governed by a controlled vocabulary.
- Measurement units are not governed by a controlled vocabulary.
- Component lifecycle transitions are not validated.
- Facility identifier consistency with the complete equipment hierarchy is not independently validated.
- The component schema describes string data types, but the Python validator does not implement a separate general-purpose datatype validation mechanism.

These limitations define the current implementation scope and provide potential directions for future development.

## 14. Related Documentation

- [Metadata Design](metadata-design.md)
- [Maintenance Guide](maintenance-guide.md)
- [Project README](../README.md)
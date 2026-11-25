# Maritime Manufacturing Metadata Catalog — Maintenance Guide

## 1. Purpose

This guide provides instructions for operating, maintaining, troubleshooting, and extending the Maritime Manufacturing Metadata Catalog.

It is intended to support continuity of the system without requiring assistance from its original developer.

For metadata definitions and architectural decisions, refer to the [Metadata Design](metadata-design.md) and [Data Dictionary](data-dictionary.md).

## 2. Environment Setup

### 2.1 Prerequisites

- Python 3.14 (development environment)
- Git
- Terminal or command-line access
- Protégé for graphical ontology editing (optional)
- Web browser for interactive graph visualization

### 2.2 Repository Installation

Clone the repository:

```bash
git clone https://github.com/jonszuba/maritime-metadata-catalog.git
cd maritime-metadata-catalog
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### 2.3 Dependencies

| Dependency | Responsibility |
|---|---|
| RDFLib | RDF graph construction, serialization, and SPARQL queries |
| OWL-RL | Rule-based semantic inference |
| PyVis | Interactive knowledge graph visualization |
| PySHACL | RDF graph constraint validation |

Dependency requirements are maintained in `requirements.txt`.

## 3. Repository Organization

```text
maritime-metadata-catalog/
├── data/
├── docs/
├── metadata/
├── src/
├── tests/
├── visualizations/
├── requirements.txt
└── README.md
```

| Directory | Responsibility |
|---|---|
| data/ | Source datasets, processed datasets, and quality reports |
| docs/ | Technical documentation and maintenance instructions |
| metadata/ | Schemas, taxonomies, ontologies, RDF graphs, and SHACL constraints |
| src/ | Data processing, validation, querying, reasoning, and visualization scripts |
| tests/ | Automated integrity and validation tests |
| visualizations/ | Generated interactive graph visualization |

## 4. Component Catalog Workflow

Execute the following commands from the repository root.

### 4.1 Generate Synthetic Data

```bash
python src/generate_data.py
```

Generates the synthetic component dataset, including intentionally introduced metadata errors.

This step is intended for recreating the demonstration dataset. Do not execute it when preserving manually modified source records.

### 4.2 Standardize Component Metadata

```bash
python src/clean_data.py
```

Processes the raw component dataset and produces standardized component records.

### 4.3 Generate the Controlled Vocabulary

```bash
python src/build_taxonomy.py
```

Generates the SKOS component taxonomy used for classification and validation.

### 4.4 Validate Component Records

```bash
python src/quality_control.py
```

Evaluates component records against the metadata schema and controlled vocabulary.

Produces validated component records and a record-level validation report.

Invalid records are excluded from the validated dataset.

### 4.5 Build the RDF Component Catalog

```bash
python src/build_catalog.py
```

Converts validated component metadata into an RDF catalog.

### 4.6 Generate Quality Metrics

```bash
python src/quality_report.py
```

Produces aggregated component quality metrics, including validation failure rates by category.

### 4.7 Search the Catalog

```bash
python src/search.py
```

Provides access to component metadata through SPARQL-based search functionality.

## 5. Manufacturing Knowledge Graph Workflow

The manufacturing equipment graph is maintained separately from the component catalog.

### 5.1 Maintain Source Records

Manufacturing source records are stored in:

- `data/equipment.csv`
- `data/signals.csv`

Consult the data dictionary before introducing or modifying records.

### 5.2 Build the Equipment Graph

```bash
python src/build_equipment_graph.py
```

Generates `metadata/equipment_graph.ttl` from equipment and signal records.

The graph builder maps equipment types to ontology classes and establishes manufacturing relationships using RDF object properties.

### 5.3 Validate the Equipment Graph

```bash
python src/validate_graph.py
```

Validates the equipment graph against the constraints in `metadata/manufacturing_shapes.ttl`.

The script produces:

- Overall SHACL conformance status.
- Number of validation violations.
- Human-readable validation results.
- A structured RDF validation report.

The validation report is saved to `metadata/shacl_validation_report.ttl`.

A nonconforming graph causes the script to return a nonzero exit status.

Resolve validation violations before treating the graph as conforming.

### 5.4 Execute Semantic Reasoning

```bash
python src/reason_ontology.py
```

Loads the manufacturing ontology and equipment graph, then applies OWL-RL reasoning.

The script reports inferred RDF triples and demonstrates inferred PhysicalAsset classifications.

Semantic reasoning is separate from SHACL validation and does not replace operational data quality checks.

### 5.5 Search Industrial Signals

```bash
python src/search_signals.py
```

Retrieves industrial signal metadata and associated manufacturing relationships through SPARQL queries.

For example, the operational signal name `PLC4_TT_1142` corresponds to the catalog identifier `SIG-001` and can be traced through its generating sensor, machine, production cell, and facility.

### 5.6 Generate the Interactive Visualization

```bash
python src/visualize_graph.py
```

Generates:

`visualizations/equipment_graph.html`

Open the HTML file in a web browser to inspect the manufacturing knowledge graph.

The visualization is a derived representation of the RDF graph. Modify source metadata or graph generation logic rather than manually editing generated visualization content.

## 6. Extending the Component Catalog

### 6.1 Adding a Component Record

1. Assign a unique component identifier.
2. Populate all required metadata fields.
3. Select an approved category and subcategory.
4. Assign a permitted lifecycle status.
5. Add the record to the source component dataset.
6. Rerun standardization and component validation.
7. Rebuild the RDF catalog and quality reports.
8. Execute the automated test suite.

Avoid regenerating the synthetic source dataset when preserving manually added records.

### 6.2 Adding a Subcategory

When introducing a new subcategory:

1. Determine the appropriate broader classification.
2. Update the taxonomy generation logic in `src/build_taxonomy.py`.
3. Define a consistent preferred label and concept URI.
4. Regenerate `metadata/taxonomy.ttl`.
5. Review any hard-coded classification mappings in data generation and standardization scripts.
6. Update the data dictionary and metadata design documentation.
7. Revalidate existing component records.
8. Execute the automated test suite.

### 6.3 Adding a Top-Level Category

Introducing a top-level category requires coordinated changes to:

- The allowed category values in `metadata/schema.json`.
- The taxonomy generation logic.
- Relevant data generation and standardization mappings.
- Classification-dependent tests.
- Metadata documentation.

Review existing records for compatibility before adopting the revised taxonomy.

### 6.4 Modifying Metadata Fields

When adding or modifying a component metadata field, review:

- Field definitions and requirements in the schema.
- Source dataset structure.
- Standardization logic.
- Validation logic.
- RDF catalog mappings.
- Search functionality.
- Automated tests.
- Metadata documentation.

Schema changes should be versioned and evaluated for compatibility with existing records.

## 7. Extending the Manufacturing Knowledge Graph

### 7.1 Adding Physical Equipment

To introduce a new physical asset:

1. Assign a unique equipment identifier.
2. Provide a descriptive name.
3. Select an approved equipment type.
4. Specify the appropriate parent asset.
5. Specify the associated facility where applicable.
6. Add the record to `data/equipment.csv`.
7. Rebuild and validate the equipment graph.
8. Regenerate the visualization.
9. Review and execute automated tests.

Parent relationships must conform to the manufacturing hierarchy.

| Equipment Type | Required Parent |
|---|---|
| Facility | None |
| Production Cell | Facility |
| Machine | Production Cell |
| Sensor | Machine |

### 7.2 Adding an Industrial Signal

To introduce a new industrial signal:

1. Assign a unique signal identifier.
2. Provide an operational signal name.
3. Reference an existing sensor identifier.
4. Specify the measurement unit.
5. Provide a descriptive explanation.
6. Add the record to `data/signals.csv`.
7. Rebuild and validate the equipment graph.
8. Verify signal retrieval through the search functionality.
9. Regenerate the visualization.
10. Review and execute automated tests.

Catalog identifiers and operational signal names must not be treated as interchangeable.

### 7.3 Adding a Manufacturing Entity Type

Introducing a new manufacturing entity type requires reviewing and potentially updating:

- OWL class definitions and logical restrictions.
- Equipment type mappings in the graph builder.
- SHACL target classes and property constraints.
- SPARQL queries.
- Visualization class colors and hierarchy levels.
- Automated tests.
- Metadata documentation.

A new class should be introduced only when existing classes cannot adequately represent the intended entity.

## 8. Ontology Maintenance

The manufacturing ontology is stored in:

`metadata/manufacturing_ontology.ttl`

It can be maintained through Protégé or direct Turtle editing.

When modifying the ontology:

1. Review existing class and property definitions.
2. Preserve established entity URIs where possible.
3. Define appropriate superclass relationships.
4. Review object property domains and ranges.
5. Evaluate existential restrictions and disjointness axioms.
6. Use an appropriate reasoner to evaluate logical consistency.
7. Save the ontology using Turtle serialization.
8. Execute the ontology compatibility and semantic reasoning tests.

Changes to ontology definitions should also be evaluated against the SHACL constraints.

OWL axioms and SHACL constraints serve different purposes and should be maintained as complementary metadata resources.

## 9. SHACL Constraint Maintenance

SHACL constraints are stored in:

`metadata/manufacturing_shapes.ttl`

When modifying validation requirements:

1. Identify the entity class and property being evaluated.
2. Determine the required constraint.
3. Update the relevant SHACL node or property shape.
4. Provide a descriptive validation message.
5. Validate the existing equipment graph.
6. Add or update automated tests for conforming and nonconforming data.
7. Review the generated validation report.
8. Update the metadata documentation.

Validation should continue to evaluate explicitly recorded metadata unless a deliberate change to the inference policy is documented.

## 10. Automated Testing

Run the complete test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The current implementation contains 30 automated tests.

| Test File | Responsibility | Tests |
|---|---|---:|
| test_catalog.py | Component catalog integrity | 5 |
| test_validation.py | Component metadata validation | 5 |
| test_equipment.py | Manufacturing graph integrity | 5 |
| test_ontology.py | Ontology compatibility | 5 |
| test_reasoning.py | Semantic inference | 3 |
| test_shacl.py | Manufacturing graph constraint validation | 7 |
| Total | | 30 |

SHACL tests introduce invalid metadata into temporary in-memory graphs without modifying the stored equipment graph.

Some tests verify expected counts and known relationships in the demonstration dataset. Intentional dataset extensions may require corresponding updates to those expectations.

Do not change test expectations solely to suppress unexpected failures.

## 11. Reference Baseline

The following results describe the current demonstration dataset.

| Metric | Expected Baseline |
|---|---:|
| Synthetic component records | 1,000 |
| Valid component records | 976 |
| Invalid component records | 24 |
| Component validation pass rate | 97.6% |
| Physical manufacturing assets | 10 |
| Industrial signals | 4 |
| Manufacturing graph entities | 14 |
| Manufacturing graph RDF triples | 66 |
| SHACL validation violations | 0 |
| Passing automated tests | 30 |

These values provide a reference for detecting unexpected changes.

The 24 invalid component records are intentionally introduced demonstration errors. Their presence in the component validation report is expected.

The manufacturing equipment graph, by contrast, is expected to conform to its SHACL constraints.

## 12. Troubleshooting

| Issue | Potential Cause | Recommended Action |
|---|---|---|
| ModuleNotFoundError | Dependencies missing or incorrect Python environment | Activate the virtual environment and install requirements |
| FileNotFoundError | Missing source or generated file | Verify repository structure and execute prerequisite scripts |
| Turtle parsing error | Invalid RDF syntax | Review the reported file and syntax location |
| Invalid taxonomy relationship | Inconsistent category and subcategory assignment | Review the SKOS taxonomy and component record |
| Duplicate component identifier | Identifier reused across component records | Investigate the duplicate and assign appropriate identifiers |
| Unknown equipment reference | Parent, facility, or sensor identifier does not exist | Correct the source relationship |
| SHACL conformance failure | Missing or invalid manufacturing metadata | Inspect the focus node, result path, and validation message |
| Unexpected ontology inference | Incorrect class or property definition | Review ontology axioms and reasoning tests |
| Signal search returns no results | Incorrect identifier, operational name, or missing relationship | Inspect the source record and RDF representation |
| Outdated visualization | Equipment graph changed without regenerating HTML | Rerun the visualization script |
| Automated test failure | Regression or changed dataset assumptions | Investigate the failure before modifying test expectations |

## 13. Version Control

Git is used to maintain a history of source code, metadata definitions, documentation, tests, and generated artifacts.

Recommended maintenance workflow:

```bash
git status
git diff
python -m unittest discover -s tests -v
```

After reviewing and validating the changes:

```bash
git add <modified-files>
git commit -m "Describe the completed change"
git push
```

Commit messages should describe a specific feature, correction, or documentation update.

Avoid committing virtual environments, credentials, proprietary information, or unrelated temporary files.

## 14. Change Review Checklist

Before committing a metadata model or processing change, confirm that:

- [ ] Source records use consistent identifiers.
- [ ] Required metadata fields are populated.
- [ ] Classification values conform to the controlled vocabulary.
- [ ] RDF graphs can be parsed successfully.
- [ ] Manufacturing relationships reference appropriate entity classes.
- [ ] SHACL validation produces the expected results.
- [ ] Semantic reasoning produces the expected classifications.
- [ ] Automated tests pass.
- [ ] Affected generated artifacts have been refreshed.
- [ ] Metadata documentation reflects the implementation.
- [ ] No sensitive or proprietary information has been introduced.

## 15. Operational Limitations

The catalog is a demonstration-scale system using synthetic data.

The current implementation does not provide production database infrastructure, access controls, automated ingestion from manufacturing systems, or comprehensive enterprise metadata governance.

Validation constraints reflect the documented requirements of the demonstration model.

Production adoption would require additional requirements analysis, governance policies, security controls, scalability evaluation, and integration testing.

## 16. Related Documentation

- [Metadata Design](metadata-design.md)
- [Data Dictionary](data-dictionary.md)
- [Project README](../README.md)
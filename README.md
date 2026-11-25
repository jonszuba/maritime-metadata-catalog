# Maritime Manufacturing Metadata Catalog

A Python-based metadata management system for standardizing, validating, organizing, and searching fictional maritime manufacturing data using semantic web technologies.

The project demonstrates how metadata schemas, controlled vocabularies, and knowledge graphs can improve data quality, classification, and traceability in industrial environments.

## Project Overview

This independent project implements an end-to-end metadata management pipeline for 1,000 synthetic maritime manufacturing components.

The system cleans inconsistent records, validates metadata against a JSON schema and SKOS taxonomy, generates an RDF knowledge graph, and provides interactive search capabilities.

An additional manufacturing equipment graph connects facilities, production cells, machines, sensors, and industrial signals, allowing raw signal identifiers to be traced back to their physical context.

All data is fictional and generated for demonstration purposes.

## Technologies

- **Python:** Data processing, validation, reporting, and search
- **RDFLib:** RDF graph construction and querying
- **SKOS:** Controlled vocabularies and hierarchical classification
- **Dublin Core:** Standardized metadata properties
- **SPARQL:** Querying semantic relationships
- **JSON and CSV:** Metadata schemas and structured datasets
- **unittest:** Automated validation and graph integrity testing
- **Git and GitHub:** Version control and project documentation

## Key Features

### 1. Metadata Standardization and Validation

Processes 1,000 synthetic component records through a reproducible Python pipeline.

- Standardizes inconsistent category and status values
- Validates required fields and permitted values
- Detects duplicate component identifiers
- Verifies category-subcategory relationships using SKOS
- Separates valid and invalid records
- Generates detailed validation reports

### 2. SKOS Taxonomy and RDF Catalog

Organizes components into four primary categories:

- Propulsion
- Electrical
- Structural
- Navigation

Uses RDF and Dublin Core metadata properties to represent component information and SKOS relationships to organize the classification hierarchy.

The resulting component catalog contains **4,942 RDF triples**.

### 3. Interactive Metadata Search

Provides a Python command-line interface for searching the component catalog by:

- Category
- Manufacturer
- Operational status

Search results are retrieved from the RDF graph using SPARQL.

### 4. Manufacturing Equipment Knowledge Graph

Models a fictional manufacturing environment containing:

| Asset type | Count |
|---|---:|
| Manufacturing facilities | 1 |
| Production cells | 2 |
| Machines | 3 |
| Sensors | 4 |
| Industrial signals | 4 |

Custom RDF relationships such as `partOf`, `locatedAt`, and `generatedBy` connect assets and establish their manufacturing context.

The equipment graph is stored separately in `metadata/equipment_graph.ttl`.

### 5. Industrial Signal Traceability

Implements a SPARQL-based lookup tool that resolves raw industrial signal identifiers to their associated equipment hierarchy.

For example, searching for `PLC4_TT_1142` returns:

| Metadata field | Value |
|---|---|
| Signal | PLC4_TT_1142 |
| Measurement unit | Celsius |
| Sensor | Motor Temperature Sensor |
| Machine | Motor Testing Station |
| Production cell | Propulsion Assembly Cell |
| Facility | Maritime Assembly Facility |

This demonstrates how semantic relationships can make otherwise ambiguous industrial data more discoverable and interpretable.

### 6. Metadata Quality Analytics

Generates a quality report summarizing validation results, error frequencies, category distributions, and failure rates.

Results can also be exported to `data/quality_summary.csv` for additional analysis.

## Project Results

The system processed a reproducible dataset of 1,000 synthetic maritime manufacturing components.

| Metric | Result |
|---|---:|
| Total component records | 1,000 |
| Valid component records | 976 |
| Invalid component records | 24 |
| Validation success rate | 97.6% |
| Component catalog RDF triples | 4,942 |
| Automated tests | 15 |

### Data Quality Findings

The validation system detected:

- 20 missing required-field errors
- 16 invalid taxonomy relationships
- 24 component records containing one or more validation errors

Some records contained multiple errors.

| Category | Total records | Invalid records | Failure rate |
|---|---:|---:|---:|
| Electrical | 248 | 11 | 4.44% |
| Propulsion | 256 | 9 | 3.52% |
| Navigation | 254 | 3 | 1.18% |
| Structural | 242 | 1 | 0.41% |

These results reflect deliberately introduced errors in synthetic data, not measurements from a real manufacturing facility.

## Project Structure

```text
maritime-metadata-catalog/
├── data/
│   ├── raw_components.csv
│   ├── standardized_components.csv
│   ├── valid_components.csv
│   ├── validation_report.csv
│   ├── quality_summary.csv
│   ├── equipment.csv
│   └── signals.csv
├── metadata/
│   ├── schema.json
│   ├── taxonomy.ttl
│   ├── catalog.ttl
│   └── equipment_graph.ttl
├── src/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── build_taxonomy.py
│   ├── validation_rules.py
│   ├── quality_control.py
│   ├── build_catalog.py
│   ├── build_equipment_graph.py
│   ├── quality_report.py
│   ├── search.py
│   └── search_signals.py
├── tests/
│   ├── test_catalog.py
│   ├── test_validation.py
│   └── test_equipment.py
├── requirements.txt
└── README.md
```

## Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/jonszuba/maritime-metadata-catalog.git
cd maritime-metadata-catalog
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Generate and process component data

```bash
python src/generate_data.py
python src/clean_data.py
python src/build_taxonomy.py
python src/quality_control.py
python src/build_catalog.py
python src/quality_report.py
```

The data generator uses a fixed random seed to produce reproducible results.

### 5. Build the manufacturing equipment graph

```bash
python src/build_equipment_graph.py
```

### 6. Search component metadata

```bash
python src/search.py
```

### 7. Trace industrial signals

```bash
python src/search_signals.py
```

Example input:

```text
PLC4_TT_1142
```

### 8. Run automated tests

```bash
python -m unittest discover -s tests -v
```

The test suite contains 15 tests covering metadata validation, identifier uniqueness, taxonomy relationships, RDF catalog integrity, and manufacturing equipment traceability.

## Future Improvements

Potential extensions include:

- More comprehensive equipment hierarchy validation
- Detection of circular equipment relationships
- Additional metadata provenance and ownership fields
- Automated data-quality visualization
- Support for larger and more complex industrial datasets

## Project Purpose

This independent project applies information science principles to fictional maritime manufacturing data, emphasizing metadata standardization, semantic modeling, controlled vocabularies, information retrieval, and industrial data contextualization.

It was developed as a technical portfolio project to explore metadata management challenges in manufacturing environments.

All datasets, equipment identifiers, and manufacturing relationships are fictional and do not represent proprietary industrial systems.
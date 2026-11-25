# Maritime Manufacturing Metadata Catalog

A Python-based metadata management system that standardizes, validates, organizes, and searches fictional maritime manufacturing component records using semantic web technologies.

## Project Overview

This project demonstrates how structured metadata and controlled vocabularies can improve data consistency, classification, and discoverability in a manufacturing environment.

The system processes component records through a pipeline that cleans inconsistent data, validates metadata quality, organizes components using a SKOS taxonomy, and generates a searchable RDF knowledge graph.

## Technologies

- **Python:** Data processing, validation, and search functionality
- **RDFLib:** RDF graph creation and querying
- **SKOS:** Controlled vocabularies and hierarchical classification
- **Dublin Core:** Standardized metadata properties
- **SPARQL:** Structured queries against RDF data
- **JSON and CSV:** Metadata schemas and component records
- **unittest:** Automated catalog integrity tests

## Data Processing Pipeline

Raw Component Data (CSV)  
↓  
Data Cleaning and Standardization  
↓  
Metadata Schema Validation  
↓  
SKOS Taxonomy Validation  
↓  
RDF Catalog Generation  
↓  
Interactive Search

## Key Features

### Metadata Standardization

Normalizes inconsistent category and status values to improve consistency across component records.

### Metadata Quality Control

Validates required fields, permitted values, unique component identifiers, and category-subcategory relationships.

Generates a CSV report identifying records that fail validation.

### SKOS Taxonomy

Organizes manufacturing components into hierarchical categories, including propulsion, electrical, structural, and navigation systems.

### RDF Knowledge Graph

Represents component metadata using RDF triples and established metadata standards.

### Interactive Search

Provides a command-line interface to search components by category, manufacturer, or operational status.

### Automated Testing

Includes automated checks for record completeness, identifier uniqueness, taxonomy relationships, and catalog integrity.

## Example Results

Using the initial fictional dataset:

- 10 component records processed
- 9 records passed validation
- 1 record flagged for missing required metadata
- 4 top-level component categories
- 5 automated catalog integrity tests

## Running the Project

Create and activate a Python virtual environment, then install RDFLib:

```bash
pip install rdflib
```

Run the pipeline:

```bash
python src/clean_data.py
python src/build_taxonomy.py
python src/quality_control.py
python src/build_catalog.py
python src/search.py
```

Run the tests:

```bash
python -m unittest discover -s tests -v
```

## Project Purpose

This independent project explores how information science principles can be applied to manufacturing metadata management, including controlled vocabularies, data quality, semantic relationships, and information retrieval.

All component records are fictional and are used for educational and demonstration purposes.
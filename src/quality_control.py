
import csv
import json
from pathlib import Path

from rdflib import Graph

from validation_rules import validate_component

BASE_DIR = Path(__file__).resolve().parent.parent

SCHEMA_PATH = BASE_DIR / "metadata" / "schema.json"
TAXONOMY_PATH = BASE_DIR / "metadata" / "taxonomy.ttl"
DATA_PATH = BASE_DIR / "data" / "standardized_components.csv"
VALID_PATH = BASE_DIR / "data" / "valid_components.csv"
REPORT_PATH = BASE_DIR / "data" / "validation_report.csv"

# Load metadata schema
with open(SCHEMA_PATH, encoding="utf-8") as file:
    schema = json.load(file)

# Load SKOS taxonomy
taxonomy_graph = Graph()
taxonomy_graph.parse(TAXONOMY_PATH, format="turtle")

# Load standardized component records
with open(DATA_PATH, newline="", encoding="utf-8-sig") as file:
    components = list(csv.DictReader(file))

seen_ids = set()
valid_components = []
invalid_components = []

# Validate every component
for component in components:
    errors = validate_component(
        component,
        schema,
        taxonomy_graph,
        seen_ids
    )

    if errors:
        invalid_components.append({
            "component_id": component["component_id"],
            "errors": "; ".join(errors)
        })
    else:
        valid_components.append(component)

# Export validated components
with open(VALID_PATH, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=list(schema["fields"].keys())
    )
    writer.writeheader()
    writer.writerows(valid_components)

# Export validation errors
with open(REPORT_PATH, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["component_id", "errors"]
    )
    writer.writeheader()
    writer.writerows(invalid_components)

print(f"Total records: {len(components)}")
print(f"Valid records: {len(valid_components)}")
print(f"Invalid records: {len(invalid_components)}")
print(f"Validation report saved to {REPORT_PATH.name}")

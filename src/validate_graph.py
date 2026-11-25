from pathlib import Path

from rdflib import Graph, RDF
from rdflib.namespace import SH
from pyshacl import validate

BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_DIR = BASE_DIR / "metadata"

REPORT_PATH = METADATA_DIR / "shacl_validation_report.ttl"

# Load the manufacturing knowledge graph
data_graph = Graph()
data_graph.parse(
    METADATA_DIR / "equipment_graph.ttl",
    format="turtle"
)

# Load the SHACL validation rules
shapes_graph = Graph()
shapes_graph.parse(
    METADATA_DIR / "manufacturing_shapes.ttl",
    format="turtle"
)

# Validate explicitly recorded manufacturing metadata
conforms, results_graph, results_text = validate(
    data_graph=data_graph,
    shacl_graph=shapes_graph,
    inference="none",
    abort_on_first=False,
    meta_shacl=True
)

# Count validation violations
violations = set(
    results_graph.subjects(
        RDF.type, SH.ValidationResult
    )
)

# Save the structured RDF validation report
results_graph.serialize(
    destination=REPORT_PATH,
    format="turtle"
)

# Display validation summary
print("Manufacturing Knowledge Graph Validation")
print("-" * 45)
print(f"Data graph triples: {len(data_graph)}")
print(f"SHACL shapes triples: {len(shapes_graph)}")
print(f"Conforms to SHACL shapes: {conforms}")
print(f"Validation violations: {len(violations)}")

print("\nDetailed validation report:")
print(results_text)

print(f"Report saved to: {REPORT_PATH.name}")

if not conforms:
    raise SystemExit(1)

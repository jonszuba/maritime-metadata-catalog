from pathlib import Path

from rdflib import Graph, Namespace, RDF
from owlrl import DeductiveClosure, OWLRL_Semantics

BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_DIR = BASE_DIR / "metadata"

EX = Namespace("https://example.org/maritime/")

graph = Graph()

# Load the ontology and equipment knowledge graph
graph.parse(
    METADATA_DIR / "manufacturing_ontology.ttl",
    format="turtle"
)

graph.parse(
    METADATA_DIR / "equipment_graph.ttl",
    format="turtle"
)

# Record explicitly stated facts
original_triples = set(graph)

print(f"Original triples: {len(graph)}")

# Perform OWL reasoning
DeductiveClosure(OWLRL_Semantics).expand(graph)

# Identify newly inferred facts
inferred_triples = set(graph) - original_triples

print(f"Total triples after reasoning: {len(graph)}")
print(f"Inferred triples: {len(inferred_triples)}")

# Identify inferred physical assets
print("\nInferred physical assets:")

for subject in sorted(
    graph.subjects(RDF.type, EX.PhysicalAsset)
):
    if (subject, RDF.type, EX.PhysicalAsset) in inferred_triples:
        print(f"  {subject.split('/')[-1]}")

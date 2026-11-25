import csv
from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from rdflib.namespace import DCTERMS, SKOS

BASE_DIR = Path(__file__).resolve().parent.parent

EX = Namespace("https://example.org/maritime/")

# Load the taxonomy we created earlier
graph = Graph()
graph.parse(
    BASE_DIR / "metadata" / "taxonomy.ttl",
    format="turtle"
)

graph.bind("ex", EX)
graph.bind("dcterms", DCTERMS)

# Load our standardized component records
with open(
    BASE_DIR / "data" / "valid_components.csv",
    newline="",
    encoding="utf-8-sig"
) as file:
    components = list(csv.DictReader(file))

# Add component metadata to our RDF graph
for component in components:

    component_id = component["component_id"]
    component_uri = EX[f"component/{component_id}"]

    category_uri = EX[component["category"].replace(" ", "_")]
    subcategory_uri = EX[component["subcategory"].replace(" ", "_")]

    # Verify the category exists in the taxonomy
    if (category_uri, RDF.type, SKOS.Concept) not in graph:
        print(f"Skipping {component_id}: unknown category")
        continue

    # Verify the subcategory belongs to that category
    if (subcategory_uri, SKOS.broader, category_uri) not in graph:
        print(f"Skipping {component_id}: invalid subcategory")
        continue

    # Add Dublin Core metadata
    graph.add((
        component_uri,
        DCTERMS.identifier,
        Literal(component_id)
    ))

    graph.add((
        component_uri,
        DCTERMS.title,
        Literal(component["name"])
    ))

    graph.add((
        component_uri,
        DCTERMS.subject,
        subcategory_uri
    ))

    if component["manufacturer"]:
        graph.add((
            component_uri,
            DCTERMS.publisher,
            Literal(component["manufacturer"])
        ))

    # Add custom manufacturing metadata
    graph.add((
        component_uri,
        EX.status,
        Literal(component["status"])
    ))

# Save the complete catalog
output_path = BASE_DIR / "metadata" / "catalog.ttl"

graph.serialize(
    destination=str(output_path),
    format="turtle"
)

print(f"Processed {len(components)} component records.")
print(f"Catalog contains {len(graph)} RDF triples.")
print(f"Saved to {output_path.name}")

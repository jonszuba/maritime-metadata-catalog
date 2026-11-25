from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF
from rdflib.namespace import SKOS

BASE_DIR = Path(__file__).resolve().parent.parent

# Create an RDF graph
graph = Graph()

# Define our custom namespace
EX = Namespace("https://example.org/maritime/")

graph.bind("ex", EX)
graph.bind("skos", SKOS)

# Define our taxonomy structure
taxonomy = {
    "Propulsion": [
        "Electric Motors",
        "Propellers"
    ],
    "Electrical": [
        "Batteries",
        "Controllers"
    ],
    "Structural": [
        "Hull Panels",
        "Brackets"
    ],
    "Navigation": [
        "GPS Systems",
        "Sensors"
    ]
}

# Create a concept scheme
scheme = EX.MaritimeComponents

graph.add((scheme, RDF.type, SKOS.ConceptScheme))
graph.add((scheme, SKOS.prefLabel, Literal("Maritime Components")))

# Create category and subcategory concepts
for category, subcategories in taxonomy.items():

    category_uri = EX[category.replace(" ", "_")]

    graph.add((category_uri, RDF.type, SKOS.Concept))
    graph.add((category_uri, SKOS.prefLabel, Literal(category)))
    graph.add((category_uri, SKOS.inScheme, scheme))
    graph.add((scheme, SKOS.hasTopConcept, category_uri))
    graph.add((category_uri, SKOS.topConceptOf, scheme))

    for subcategory in subcategories:

        subcategory_uri = EX[subcategory.replace(" ", "_")]

        graph.add((subcategory_uri, RDF.type, SKOS.Concept))
        graph.add((subcategory_uri, SKOS.prefLabel, Literal(subcategory)))
        graph.add((subcategory_uri, SKOS.broader, category_uri))
        graph.add((category_uri, SKOS.narrower, subcategory_uri))
        graph.add((subcategory_uri, SKOS.inScheme, scheme))

# Export taxonomy as Turtle
output_path = BASE_DIR / "metadata" / "taxonomy.ttl"

graph.serialize(destination=str(output_path), format="turtle")

print(f"Created {len(graph)} RDF triples.")
print(f"Taxonomy saved to {output_path.name}")

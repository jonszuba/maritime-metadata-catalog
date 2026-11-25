from pathlib import Path
from html import escape

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.namespace import DCTERMS
from pyvis.network import Network

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "visualizations"
OUTPUT_PATH = OUTPUT_DIR / "equipment_graph.html"

EX = Namespace("https://example.org/maritime/")

graph = Graph()
graph.parse(
    BASE_DIR / "metadata" / "equipment_graph.ttl",
    format="turtle"
)

OUTPUT_DIR.mkdir(exist_ok=True)

# Configure the interactive network
network = Network(
    height="800px",
    width="100%",
    directed=True,
    bgcolor="#0f172a",
    font_color="#ffffff",
    cdn_resources="in_line",
    select_menu=True
)

# Assign a color to each manufacturing class
CLASS_COLORS = {
    EX.Facility: "#ef4444",
    EX.ProductionCell: "#f59e0b",
    EX.Machine: "#3b82f6",
    EX.Sensor: "#22c55e",
    EX.IndustrialSignal: "#a855f7",
}

# Add manufacturing entities as nodes
for entity, entity_class in graph.subject_objects(RDF.type):

    if entity_class not in CLASS_COLORS:
        continue

    identifier = str(entity).split("/")[-1]
    label = str(graph.value(entity, RDFS.label) or identifier)
    class_name = str(entity_class).split("/")[-1]

    description = graph.value(entity, DCTERMS.description)
    unit = graph.value(entity, EX.measurementUnit)

    tooltip = (
        f"Name: {escape(label)}<br>"
        f"ID: {escape(identifier)}<br>"
        f"Class: {escape(class_name)}"
    )

    if description:
        tooltip += f"<br>Description: {escape(str(description))}"

    if unit:
        tooltip += f"<br>Measurement unit: {escape(str(unit))}"

    network.add_node(
        str(entity),
        label=label,
        title=tooltip,
        color=CLASS_COLORS[entity_class],
        shape="dot",
        size=25
    )

# Add semantic relationships as directed edges
relationships = [
    EX.generatedBy,
    EX.partOf,
    EX.locatedAt
]

node_ids = set(network.get_nodes())

for relationship in relationships:

    relationship_name = str(relationship).split("/")[-1]

    for subject, obj in graph.subject_objects(relationship):

        if str(subject) in node_ids and str(obj) in node_ids:

            network.add_edge(
                str(subject),
                str(obj),
                label=relationship_name,
                title=relationship_name,
                arrows="to"
            )

# Configure the graph layout
network.barnes_hut(
    gravity=-8000,
    central_gravity=0.3,
    spring_length=220,
    spring_strength=0.04,
    damping=0.09
)

# Export a standalone interactive HTML file
network.write_html(
    str(OUTPUT_PATH),
    notebook=False,
    open_browser=False
)

print(f"Created {len(network.nodes)} nodes.")
print(f"Created {len(network.edges)} edges.")
print(f"Visualization saved to {OUTPUT_PATH}")

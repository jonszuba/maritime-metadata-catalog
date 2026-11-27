
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
    select_menu=True,
    heading=""
)

# Assign a color to each manufacturing class
CLASS_COLORS = {
    EX.Facility: "#ef4444",
    EX.ProductionCell: "#f59e0b",
    EX.Machine: "#3b82f6",
    EX.Sensor: "#22c55e",
    EX.IndustrialSignal: "#a855f7",
}

# Define hierarchical levels
CLASS_LEVELS = {
    EX.Facility: 0,
    EX.ProductionCell: 1,
    EX.Machine: 2,
    EX.Sensor: 3,
    EX.IndustrialSignal: 4,
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
        level=CLASS_LEVELS[entity_class],
        shape="dot",
        size=25,
        font={
            "size": 16,
            "color": "#ffffff"
        }
    )

# Define semantic relationships
relationships = [
    EX.generatedBy,
    EX.partOf,
    EX.locatedAt
]

node_ids = set(network.get_nodes())
edge_labels = {}

# Collect relationships between each pair of nodes
for relationship in relationships:

    relationship_name = str(relationship).split("/")[-1]

    for subject, obj in graph.subject_objects(relationship):

        if str(subject) in node_ids and str(obj) in node_ids:

            edge = (str(subject), str(obj))

            edge_labels.setdefault(edge, []).append(
                relationship_name
            )

# Combine parallel relationships into single visual edges
for (source, target), labels in edge_labels.items():

    combined_label = " / ".join(labels)

    network.add_edge(
        source,
        target,
        label=combined_label,
        title=combined_label,
        arrows="to"
    )

# Configure hierarchical layout and interaction
network.set_options("""
{
    "layout": {
        "hierarchical": {
            "enabled": true,
            "direction": "UD",
            "levelSeparation": 150,
            "nodeSpacing": 250,
            "treeSpacing": 280,
            "sortMethod": "hubsize",
            "blockShifting": true,
            "edgeMinimization": true,
            "parentCentralization": true
        }
    },
    "physics": {
        "enabled": false
    },
    "edges": {
        "color": {
            "color": "#94a3b8",
            "inherit": false
        },
        "font": {
            "size": 13,
            "color": "#cbd5e1",
            "strokeWidth": 0
        },
        "smooth": {
            "enabled": true,
            "type": "cubicBezier",
            "forceDirection": "vertical",
            "roundness": 0.4
        }
    },
    "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
    }
}
""")

# Export standalone interactive HTML
network.write_html(
    str(OUTPUT_PATH),
    notebook=False,
    open_browser=False
)

# Define human-readable class names for the legend
CLASS_NAMES = {
    EX.Facility: "Facility",
    EX.ProductionCell: "Production Cell",
    EX.Machine: "Machine",
    EX.Sensor: "Sensor",
    EX.IndustrialSignal: "Industrial Signal",
}

# Generate the color legend dynamically
legend_items = ""

for entity_class, color in CLASS_COLORS.items():

    class_name = CLASS_NAMES[entity_class]

    legend_items += f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="
                display: inline-block;
                width: 14px;
                height: 14px;
                border-radius: 50%;
                background: {color};
            "></span>
            {escape(class_name)}
        </div>
    """

legend_html = f"""
<div style="
    background: #0f172a;
    color: #ffffff;
    padding: 20px;
    font-family: Arial, sans-serif;
    border-bottom: 1px solid #334155;
">
    <p style="
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 20px;
    ">
        Interactive RDF knowledge graph of synthetic maritime
        manufacturing assets and industrial signals.
        Select or hover over an entity to explore its metadata.
    </p>

    <div style="
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 25px;
        font-size: 14px;
    ">
        {legend_items}
    </div>
</div>
"""

# Insert the legend into the generated HTML
html_content = OUTPUT_PATH.read_text(encoding="utf-8")

body_start = html_content.find("<body")

if body_start == -1:
    raise ValueError("HTML body element not found.")

body_end = html_content.index(">", body_start) + 1

html_content = (
    html_content[:body_end]
    + legend_html
    + html_content[body_end:]
)

OUTPUT_PATH.write_text(html_content, encoding="utf-8")

# Display generation summary
print(f"Created {len(network.nodes)} nodes.")
print(f"Created {len(network.edges)} visual edges.")
print(
    f"Represented {sum(len(labels) for labels in edge_labels.values())} "
    "semantic relationships."
)
print(f"Visualization saved to {OUTPUT_PATH}")

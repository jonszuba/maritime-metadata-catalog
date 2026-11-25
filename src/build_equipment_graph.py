import csv
from pathlib import Path

from rdflib import Graph, Namespace, Literal, RDF
from rdflib.namespace import DCTERMS, RDFS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_PATH = BASE_DIR / "metadata" / "equipment_graph.ttl"

EX = Namespace("https://example.org/maritime/")

graph = Graph()
graph.bind("ex", EX)
graph.bind("dcterms", DCTERMS)
graph.bind("rdfs", RDFS)


def read_csv(filename):
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


equipment = read_csv("equipment.csv")
signals = read_csv("signals.csv")

equipment_ids = {item["equipment_id"] for item in equipment}

# Add equipment metadata and hierarchy
for item in equipment:
    equipment_id = item["equipment_id"]
    uri = EX[equipment_id]

    graph.add((uri, RDF.type, EX.EquipmentAsset))
    graph.add((uri, DCTERMS.identifier, Literal(equipment_id)))
    graph.add((uri, RDFS.label, Literal(item["name"])))
    graph.add((uri, EX.equipmentType, Literal(item["equipment_type"])))

    parent_id = item["parent_id"].strip()

    if parent_id:
        if parent_id not in equipment_ids:
            raise ValueError(
                f"Unknown parent {parent_id} for {equipment_id}"
            )

        graph.add((uri, EX.partOf, EX[parent_id]))

    facility_id = item["facility_id"].strip()

    if facility_id:
        if facility_id not in equipment_ids:
            raise ValueError(
                f"Unknown facility {facility_id} for {equipment_id}"
            )

        graph.add((uri, EX.locatedAt, EX[facility_id]))

# Add industrial signals
for signal in signals:
    signal_uri = EX[signal["signal_id"]]
    sensor_id = signal["sensor_id"]

    if sensor_id not in equipment_ids:
        raise ValueError(
            f"Unknown sensor {sensor_id} for signal {signal['signal_id']}"
        )

    graph.add((signal_uri, RDF.type, EX.IndustrialSignal))
    graph.add((
        signal_uri,
        DCTERMS.identifier,
        Literal(signal["signal_id"])
    ))
    graph.add((
        signal_uri,
        RDFS.label,
        Literal(signal["signal_name"])
    ))
    graph.add((
        signal_uri,
        EX.generatedBy,
        EX[sensor_id]
    ))
    graph.add((
        signal_uri,
        EX.measurementUnit,
        Literal(signal["unit"])
    ))
    graph.add((
        signal_uri,
        DCTERMS.description,
        Literal(signal["description"])
    ))

graph.serialize(destination=OUTPUT_PATH, format="turtle")

print(f"Processed {len(equipment)} equipment assets.")
print(f"Processed {len(signals)} industrial signals.")
print(f"Created {len(graph)} RDF triples.")
print(f"Saved to {OUTPUT_PATH.name}")

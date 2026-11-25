from pathlib import Path
from rdflib import Graph, Literal, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_PATH = BASE_DIR / "metadata" / "equipment_graph.ttl"

EX = Namespace("https://example.org/maritime/")

graph = Graph()
graph.parse(GRAPH_PATH, format="turtle")

print("\nINDUSTRIAL SIGNAL LOOKUP")
print("=" * 45)

signal_name = input("Enter signal identifier: ").strip()

query = """
PREFIX ex: <https://example.org/maritime/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?sensorName ?machineName ?cellName ?facilityName ?unit
WHERE {
    ?signal rdfs:label ?signalName ;
            ex:generatedBy ?sensor ;
            ex:measurementUnit ?unit .

    ?sensor rdfs:label ?sensorName ;
            ex:partOf ?machine .

    ?machine rdfs:label ?machineName ;
             ex:partOf ?cell .

    ?cell rdfs:label ?cellName ;
          ex:partOf ?facility .

    ?facility rdfs:label ?facilityName .
}
"""

results = list(
    graph.query(
        query,
        initBindings={"signalName": Literal(signal_name)}
    )
)

if not results:
    print(f"\nNo matching signal hierarchy found for: {signal_name}")
else:
    for result in results:
        print("\nSIGNAL METADATA")
        print("-" * 45)
        print(f"Signal: {signal_name}")
        print(f"Measurement unit: {result.unit}")
        print(f"Sensor: {result.sensorName}")
        print(f"Machine: {result.machineName}")
        print(f"Production cell: {result.cellName}")
        print(f"Facility: {result.facilityName}")
        print("-" * 45)

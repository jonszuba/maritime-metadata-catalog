
from pathlib import Path
from rdflib import Graph
from rdflib.namespace import DCTERMS

BASE_DIR = Path(__file__).resolve().parent.parent

graph = Graph()
graph.parse(BASE_DIR / "metadata" / "catalog.ttl", format="turtle")

print("MARITIME COMPONENT SEARCH")
print("-" * 40)

print("1. Search by category")
print("2. Search by manufacturer")
print("3. Search by status")
print("4. Show all components")

choice = input("\nSelect an option (1-4): ").strip()

if choice not in {"1", "2", "3", "4"}:
    print("Invalid option.")
    raise SystemExit(1)

search_value = ""

if choice != "4":
    search_value = input("Enter search term: ").strip()

query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX ex: <https://example.org/maritime/>

SELECT ?id ?name ?category ?manufacturer ?status
WHERE {
    ?component dcterms:identifier ?id ;
               dcterms:title ?name ;
               dcterms:subject ?subcategory ;
               ex:status ?status .

    ?subcategory skos:broader ?categoryConcept .
    ?categoryConcept skos:prefLabel ?category .

    OPTIONAL {
        ?component dcterms:publisher ?manufacturer .
    }
}
ORDER BY ?id
"""

results = graph.query(query)
matches = []

for row in results:
    record = {
        "id": str(row.id),
        "name": str(row.name),
        "category": str(row.category),
        "manufacturer": str(row.manufacturer or ""),
        "status": str(row.status)
    }

    if choice == "1" and search_value.lower() not in record["category"].lower():
        continue
    if choice == "2" and search_value.lower() not in record["manufacturer"].lower():
        continue
    if choice == "3" and search_value.lower() not in record["status"].lower():
        continue

    matches.append(record)

print(f"\nFound {len(matches)} matching components.\n")

for record in matches:
    print(f"ID: {record['id']}")
    print(f"Name: {record['name']}")
    print(f"Category: {record['category']}")
    print(f"Manufacturer: {record['manufacturer'] or 'Not specified'}")
    print(f"Status: {record['status']}")
    print("-" * 40)

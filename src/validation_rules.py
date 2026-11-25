
from rdflib import Namespace
from rdflib.namespace import SKOS

EX = Namespace("https://example.org/maritime/")


def validate_component(component, schema, taxonomy_graph, seen_ids):
    errors = []

    component_id = component.get("component_id", "").strip()

    # Check duplicate identifiers
    if component_id in seen_ids:
        errors.append("Duplicate component ID")

    seen_ids.add(component_id)

    # Validate required fields and allowed values
    for field_name, rules in schema["fields"].items():
        value = component.get(field_name, "").strip()

        if rules.get("required") and not value:
            errors.append(f"Missing required field: {field_name}")
            continue

        allowed_values = rules.get("allowed_values", [])

        if value and allowed_values and value not in allowed_values:
            errors.append(f"Invalid {field_name}: {value}")

    # Validate category-subcategory relationships
    category = component.get("category", "").strip()
    subcategory = component.get("subcategory", "").strip()

    if category and subcategory:
        category_uri = EX[category.replace(" ", "_")]
        subcategory_uri = EX[subcategory.replace(" ", "_")]

        if (subcategory_uri, SKOS.broader, category_uri) not in taxonomy_graph:
            errors.append(
                f"Invalid taxonomy relationship: {subcategory} "
                f"does not belong under {category}"
            )

    return errors

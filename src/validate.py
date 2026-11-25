
import json
import csv
from pathlib import Path

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load our metadata schema
with open(BASE_DIR / "metadata" / "schema.json") as file:
    schema = json.load(file)

# Load our manufacturing component records
with open(BASE_DIR / "data" / "standardized_components.csv") as file:
    reader = csv.DictReader(file)
    print("CSV columns:", reader.fieldnames)
    components = list(reader)

# Track validation problems
errors = []

# Check each component
for component in components:

    component_id = component["component_id"]

    # Check each field against the schema
    for field_name, rules in schema["fields"].items():

        value = component.get(field_name, "").strip()

        # Check for missing required values
        if rules.get("required") and not value:
            errors.append(
                f"{component_id}: Missing required field '{field_name}'"
            )
            continue

        # Check controlled vocabulary values
        allowed_values = rules.get("allowed_values")

        if value and allowed_values and value not in allowed_values:
            errors.append(
                f"{component_id}: Invalid '{field_name}' value: '{value}'"
            )

# Display results
print(f"Validated {len(components)} components.")
print(f"Found {len(errors)} validation errors.\n")

for error in errors:
    print(error)

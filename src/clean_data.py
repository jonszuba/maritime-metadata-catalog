import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data" / "raw_components.csv"
output_path = BASE_DIR / "data" / "standardized_components.csv"

# Approved category terminology
category_mapping = {
    "propulsion": "Propulsion",
    "electrical": "Electrical",
    "electric": "Electrical",
    "structural": "Structural",
    "navigation": "Navigation"
}

# Approved status terminology
status_mapping = {
    "active": "Active",
    "discontinued": "Discontinued",
    "under review": "Under Review"
}

cleaned_components = []
unresolved_issues = []

with open(input_path, newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(
        line for line in file if line.strip()
    )

    for component in reader:

        component_id = component["component_id"]

        # Remove extra whitespace from every field
        for field, value in component.items():
            component[field] = (value or "").strip()

        # Standardize category
        original_category = component["category"]
        category_key = original_category.lower()

        if category_key in category_mapping:
            component["category"] = category_mapping[category_key]
        else:
            unresolved_issues.append(
                f"{component_id}: Unknown category '{original_category}'"
            )

        # Standardize status
        original_status = component["status"]
        status_key = original_status.lower()

        if status_key in status_mapping:
            component["status"] = status_mapping[status_key]
        else:
            unresolved_issues.append(
                f"{component_id}: Missing or unknown status '{original_status}'"
            )

        cleaned_components.append(component)

# Save standardized records
with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "component_id",
            "name",
            "category",
            "subcategory",
            "manufacturer",
            "status"
        ]
    )

    writer.writeheader()
    writer.writerows(cleaned_components)

print(f"Standardized {len(cleaned_components)} components.")
print(f"Saved output to {output_path.name}")

print(f"\nUnresolved issues: {len(unresolved_issues)}")

for issue in unresolved_issues:
    print(issue)

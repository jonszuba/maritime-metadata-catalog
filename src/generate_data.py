import csv
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = BASE_DIR / "data" / "raw_components.csv"

random.seed(42)

components = {
    "Propulsion": {
        "Electric Motors": [
            "Electric Propulsion Motor",
            "Auxiliary Drive Motor",
            "High-Torque Motor",
            "Propulsion Motor"
        ],
        "Propellers": [
            "Marine Propeller",
            "Variable Pitch Propeller",
            "Thruster Propeller"
        ]
    },
    "Electrical": {
        "Batteries": [
            "Lithium Battery",
            "Battery Module",
            "Marine Battery Pack"
        ],
        "Controllers": [
            "Power Controller",
            "Motor Controller",
            "Voltage Regulator"
        ]
    },
    "Structural": {
        "Hull Panels": [
            "Composite Hull Panel",
            "Reinforced Hull Panel",
            "Aluminum Hull Panel"
        ],
        "Brackets": [
            "Mounting Bracket",
            "Hull Support Bracket",
            "Structural Bracket"
        ]
    },
    "Navigation": {
        "GPS Systems": [
            "GPS Receiver",
            "GPS Navigation Module",
            "Marine GPS Unit"
        ],
        "Sensors": [
            "Depth Sensor",
            "Navigation Sensor",
            "Inertial Sensor"
        ]
    }
}

manufacturers = [
    "Example Marine Systems",
    "Ocean Technologies",
    "Marine Fabrication Co",
    "NavTech",
    "Coastal Engineering",
    "Bluewater Components",
    "Atlantic Marine Electronics",
    "Harbor Systems"
]

statuses = ["Active", "Discontinued", "Under Review"]

records = []

for i in range(1, 1001):
    category = random.choice(list(components.keys()))
    subcategory = random.choice(list(components[category].keys()))
    name = random.choice(components[category][subcategory])

    record = {
        "component_id": f"CMP-{i:04d}",
        "name": f"{name} Model {random.randint(100, 999)}",
        "category": category,
        "subcategory": subcategory,
        "manufacturer": random.choice(manufacturers),
        "status": random.choice(statuses)
    }

    # Introduce intentional data-quality problems
    if i % 50 == 0:
        record["status"] = ""

    if i % 75 == 0:
        record["category"] = "propulsion"

    if i % 100 == 0:
        record["category"] = "Electrical" if category != "Electrical" else "Navigation"

    records.append(record)

fieldnames = [
    "component_id",
    "name",
    "category",
    "subcategory",
    "manufacturer",
    "status"
]

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Generated {len(records)} fictional maritime components.")
print(f"Saved to {OUTPUT_PATH}")

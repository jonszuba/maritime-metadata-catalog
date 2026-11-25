
import json
import sys
import unittest
from pathlib import Path

from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from validation_rules import validate_component

with open(BASE_DIR / "metadata" / "schema.json", encoding="utf-8") as file:
    SCHEMA = json.load(file)

TAXONOMY = Graph()
TAXONOMY.parse(
    BASE_DIR / "metadata" / "taxonomy.ttl",
    format="turtle"
)


class TestMetadataValidation(unittest.TestCase):

    def setUp(self):
        self.valid_component = {
            "component_id": "TEST-001",
            "name": "Electric Propulsion Motor",
            "category": "Propulsion",
            "subcategory": "Electric Motors",
            "manufacturer": "Example Marine Systems",
            "status": "Active"
        }

    def validate(self, component, seen_ids=None):
        if seen_ids is None:
            seen_ids = set()

        return validate_component(
            component,
            SCHEMA,
            TAXONOMY,
            seen_ids
        )

    def test_valid_component(self):
        self.assertEqual(self.validate(self.valid_component), [])

    def test_missing_required_status(self):
        component = self.valid_component.copy()
        component["status"] = ""

        errors = self.validate(component)

        self.assertTrue(
            any("Missing required field: status" in e for e in errors)
        )

    def test_invalid_status(self):
        component = self.valid_component.copy()
        component["status"] = "Unknown"

        errors = self.validate(component)

        self.assertTrue(
            any("Invalid status" in e for e in errors)
        )

    def test_invalid_taxonomy_relationship(self):
        component = self.valid_component.copy()
        component["category"] = "Electrical"

        errors = self.validate(component)

        self.assertTrue(
            any("Invalid taxonomy relationship" in e for e in errors)
        )

    def test_duplicate_component_id(self):
        errors = self.validate(
            self.valid_component,
            {"TEST-001"}
        )

        self.assertIn("Duplicate component ID", errors)


if __name__ == "__main__":
    unittest.main()

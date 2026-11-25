import csv
import unittest
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import DCTERMS, SKOS

BASE_DIR = Path(__file__).resolve().parent.parent
EX = Namespace("https://example.org/maritime/")


class TestMaritimeCatalog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        cls.graph.parse(
            BASE_DIR / "metadata" / "catalog.ttl",
            format="turtle"
        )

        with open(
            BASE_DIR / "data" / "valid_components.csv",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            cls.components = list(csv.DictReader(file))

    def test_valid_component_count(self):
        self.assertGreater(len(self.components), 900)
        self.assertLessEqual(len(self.components), 1000)

    def test_component_ids_are_unique(self):
        ids = [c["component_id"] for c in self.components]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields_are_present(self):
        required = [
            "component_id",
            "name",
            "category",
            "subcategory",
            "status"
        ]

        for component in self.components:
            for field in required:
                self.assertTrue(
                    component[field].strip(),
                    f"Missing {field} in {component['component_id']}"
                )

    def test_taxonomy_relationships(self):
        for component in self.components:
            category = EX[component["category"].replace(" ", "_")]
            subcategory = EX[component["subcategory"].replace(" ", "_")]

            self.assertIn(
                (subcategory, SKOS.broader, category),
                self.graph
            )

    def test_catalog_contains_all_valid_ids(self):
        catalog_ids = {
            str(value)
            for value in self.graph.objects(
                None, DCTERMS.identifier
            )
        }

        expected_ids = {
            component["component_id"]
            for component in self.components
        }

        self.assertEqual(catalog_ids, expected_ids)


if __name__ == "__main__":
    unittest.main()

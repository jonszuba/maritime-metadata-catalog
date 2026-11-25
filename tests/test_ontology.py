import unittest
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL

BASE_DIR = Path(__file__).resolve().parent.parent
EX = Namespace("https://example.org/maritime/")


class TestManufacturingOntology(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ontology = Graph()
        cls.ontology.parse(
            BASE_DIR / "metadata" / "manufacturing_ontology.ttl",
            format="turtle"
        )

        cls.equipment = Graph()
        cls.equipment.parse(
            BASE_DIR / "metadata" / "equipment_graph.ttl",
            format="turtle"
        )

    def test_all_classes_defined(self):
        defined_classes = set(
            self.ontology.subjects(RDF.type, OWL.Class)
        )

        used_classes = set(
            self.equipment.objects(None, RDF.type)
        )

        self.assertTrue(used_classes.issubset(defined_classes))

    def test_all_manufacturing_properties_defined(self):
        defined_properties = (
            set(self.ontology.subjects(RDF.type, OWL.ObjectProperty))
            | set(self.ontology.subjects(RDF.type, OWL.DatatypeProperty))
        )

        used_properties = {
            p for p in self.equipment.predicates()
            if str(p).startswith(str(EX))
        }

        self.assertTrue(
            used_properties.issubset(defined_properties)
        )

    def test_physical_asset_hierarchy(self):
        for asset_class in [
            EX.Facility,
            EX.ProductionCell,
            EX.Machine,
            EX.Sensor
        ]:
            self.assertIn(
                (asset_class, RDFS.subClassOf, EX.PhysicalAsset),
                self.ontology
            )

    def test_generated_by_domain_and_range(self):
        self.assertIn(
            (EX.generatedBy, RDFS.domain, EX.IndustrialSignal),
            self.ontology
        )

        self.assertIn(
            (EX.generatedBy, RDFS.range, EX.Sensor),
            self.ontology
        )

    def test_located_at_domain_and_range(self):
        self.assertIn(
            (EX.locatedAt, RDFS.domain, EX.Machine),
            self.ontology
        )

        self.assertIn(
            (EX.locatedAt, RDFS.range, EX.ProductionCell),
            self.ontology
        )


if __name__ == "__main__":
    unittest.main()

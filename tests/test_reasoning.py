import unittest
from pathlib import Path

from rdflib import Graph, Namespace, RDF
from owlrl import DeductiveClosure, OWLRL_Semantics

BASE_DIR = Path(__file__).resolve().parent.parent
EX = Namespace("https://example.org/maritime/")


class TestOntologyReasoning(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()

        cls.graph.parse(
            BASE_DIR / "metadata" / "manufacturing_ontology.ttl",
            format="turtle"
        )

        cls.graph.parse(
            BASE_DIR / "metadata" / "equipment_graph.ttl",
            format="turtle"
        )

        cls.original_triples = set(cls.graph)

        DeductiveClosure(OWLRL_Semantics).expand(cls.graph)

        cls.inferred_triples = (
            set(cls.graph) - cls.original_triples
        )

    def test_all_physical_assets_inferred(self):
        expected_assets = {
            EX["FAC-001"],
            EX["CELL-001"],
            EX["CELL-002"],
            EX["EQ-001"],
            EX["EQ-002"],
            EX["EQ-003"],
            EX["SEN-001"],
            EX["SEN-002"],
            EX["SEN-003"],
            EX["SEN-004"],
        }

        inferred_assets = {
            subject
            for subject, predicate, obj in self.inferred_triples
            if predicate == RDF.type and obj == EX.PhysicalAsset
        }

        self.assertEqual(inferred_assets, expected_assets)

    def test_signals_not_classified_as_physical_assets(self):
        for signal in self.graph.subjects(
            RDF.type, EX.IndustrialSignal
        ):
            self.assertNotIn(
                (signal, RDF.type, EX.PhysicalAsset),
                self.graph
            )

    def test_domain_and_range_inference(self):
        graph = Graph()

        graph.parse(
            BASE_DIR / "metadata" / "manufacturing_ontology.ttl",
            format="turtle"
        )

        signal = EX.TestSignal
        sensor = EX.TestSensor

        graph.add((signal, EX.generatedBy, sensor))

        DeductiveClosure(OWLRL_Semantics).expand(graph)

        self.assertIn(
            (signal, RDF.type, EX.IndustrialSignal),
            graph
        )

        self.assertIn(
            (sensor, RDF.type, EX.Sensor),
            graph
        )

        self.assertIn(
            (sensor, RDF.type, EX.PhysicalAsset),
            graph
        )


if __name__ == "__main__":
    unittest.main()
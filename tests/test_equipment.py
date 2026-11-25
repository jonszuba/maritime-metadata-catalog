import csv
import unittest
from pathlib import Path

from rdflib import Graph, Namespace, RDF

BASE_DIR = Path(__file__).resolve().parent.parent
EX = Namespace("https://example.org/maritime/")


class TestEquipmentGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        cls.graph.parse(
            BASE_DIR / "metadata" / "equipment_graph.ttl",
            format="turtle"
        )

        with open(
            BASE_DIR / "data" / "equipment.csv",
            newline="",
            encoding="utf-8"
        ) as file:
            cls.equipment = list(csv.DictReader(file))

        with open(
            BASE_DIR / "data" / "signals.csv",
            newline="",
            encoding="utf-8"
        ) as file:
            cls.signals = list(csv.DictReader(file))

    def test_all_equipment_in_graph(self):
        for item in self.equipment:
            uri = EX[item["equipment_id"]]
            self.assertIn(
                (uri, RDF.type, EX.EquipmentAsset),
                self.graph
            )

    def test_all_signals_in_graph(self):
        for signal in self.signals:
            uri = EX[signal["signal_id"]]
            self.assertIn(
                (uri, RDF.type, EX.IndustrialSignal),
                self.graph
            )

    def test_equipment_parent_relationships(self):
        for item in self.equipment:
            parent_id = item["parent_id"].strip()

            if parent_id:
                self.assertIn(
                    (
                        EX[item["equipment_id"]],
                        EX.partOf,
                        EX[parent_id]
                    ),
                    self.graph
                )

    def test_signals_reference_existing_sensors(self):
        sensor_ids = {
            item["equipment_id"]
            for item in self.equipment
            if item["equipment_type"] == "Sensor"
        }

        for signal in self.signals:
            self.assertIn(signal["sensor_id"], sensor_ids)
            self.assertIn(
                (
                    EX[signal["signal_id"]],
                    EX.generatedBy,
                    EX[signal["sensor_id"]]
                ),
                self.graph
            )

    def test_known_signal_hierarchy(self):
        query = """
        PREFIX ex: <https://example.org/maritime/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?facilityName
        WHERE {
            ?signal rdfs:label "PLC4_TT_1142" ;
                    ex:generatedBy/ex:partOf/ex:partOf/ex:partOf
                    ?facility .

            ?facility rdfs:label ?facilityName .
        }
        """

        results = list(self.graph.query(query))

        self.assertEqual(len(results), 1)
        self.assertEqual(
            str(results[0].facilityName),
            "Maritime Assembly Facility"
        )


if __name__ == "__main__":
    unittest.main()

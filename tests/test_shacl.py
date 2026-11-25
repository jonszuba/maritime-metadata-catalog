import unittest
from pathlib import Path

from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DCTERMS, SH
from pyshacl import validate

BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_DIR = BASE_DIR / "metadata"

EX = Namespace("https://example.org/maritime/")


class TestSHACLValidation(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.parse(
            METADATA_DIR / "equipment_graph.ttl",
            format="turtle"
        )

        self.shapes = Graph()
        self.shapes.parse(
            METADATA_DIR / "manufacturing_shapes.ttl",
            format="turtle"
        )

    def validate_graph(self):
        return validate(
            data_graph=self.graph,
            shacl_graph=self.shapes,
            inference="none",
            abort_on_first=False
        )

    def assert_violation(self, entity, property_uri):
        conforms, report, _ = self.validate_graph()

        self.assertFalse(conforms)

        matching_violations = [
            result
            for result in report.subjects(
                RDF.type, SH.ValidationResult
            )
            if (
                result, SH.focusNode, entity
            ) in report
            and (
                result, SH.resultPath, property_uri
            ) in report
        ]

        self.assertTrue(
            matching_violations,
            f"Expected violation for {entity} on {property_uri}"
        )

    def test_valid_manufacturing_graph(self):
        conforms, _, _ = self.validate_graph()
        self.assertTrue(conforms)

    def test_missing_signal_sensor(self):
        signal = EX["SIG-001"]

        self.graph.remove(
            (signal, EX.generatedBy, None)
        )

        self.assert_violation(signal, EX.generatedBy)

    def test_incorrect_sensor_parent(self):
        sensor = EX["SEN-001"]

        self.graph.remove(
            (sensor, EX.partOf, None)
        )

        self.graph.add(
            (sensor, EX.partOf, EX["FAC-001"])
        )

        self.assert_violation(sensor, EX.partOf)

    def test_missing_asset_identifier(self):
        machine = EX["EQ-001"]

        self.graph.remove(
            (machine, DCTERMS.identifier, None)
        )

        self.assert_violation(
            machine, DCTERMS.identifier
        )

    def test_conflicting_machine_location(self):
        machine = EX["EQ-001"]

        self.graph.remove(
            (machine, EX.locatedAt, None)
        )

        self.graph.add(
            (machine, EX.locatedAt, EX["CELL-002"])
        )

        self.assert_violation(machine, EX.partOf)

    def test_multiple_generating_sensors(self):
        signal = EX["SIG-001"]

        self.graph.add(
            (signal, EX.generatedBy, EX["SEN-002"])
        )

        self.assert_violation(signal, EX.generatedBy)

    def test_missing_measurement_unit(self):
        signal = EX["SIG-001"]

        self.graph.remove(
            (signal, EX.measurementUnit, None)
        )

        self.assert_violation(
            signal, EX.measurementUnit
        )


if __name__ == "__main__":
    unittest.main()

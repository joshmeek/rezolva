import csv
import os
import unittest

from rezolva.core.base import Entity
from rezolva.data_handlers.csv_handlers import CSVDataLoader, CSVDataSaver


class TestCSVHandlers(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_data.csv"
        self.test_data = [["id", "name", "age"], ["1", "John Doe", "30"], ["2", "Jane Smith", "25"]]
        with open(self.test_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.test_data)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_csv_data_loader(self):
        loader = CSVDataLoader()
        entities = loader.load(self.test_file)

        self.assertEqual(len(entities), 2)
        self.assertIsInstance(entities[0], Entity)
        self.assertEqual(entities[0].id, "1")
        self.assertEqual(entities[0].attributes["name"], "John Doe")
        self.assertEqual(entities[1].id, "2")
        self.assertEqual(entities[1].attributes["age"], "25")

    def test_csv_data_saver(self):
        entities = [
            Entity("3", {"name": "Alice Johnson", "age": "35"}),
            Entity("4", {"name": "Bob Williams", "age": "40"}),
        ]
        saver = CSVDataSaver()
        output_file = "output_test_data.csv"
        saver.save(entities, output_file)

        # Check if the file was created
        self.assertTrue(os.path.exists(output_file))

        # Load the saved data and verify
        with open(output_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            saved_data = list(reader)

        self.assertEqual(len(saved_data), 2)
        self.assertEqual(saved_data[0]["id"], "3")
        self.assertEqual(saved_data[0]["name"], "Alice Johnson")
        self.assertEqual(saved_data[1]["id"], "4")
        self.assertEqual(saved_data[1]["age"], "40")

        # Clean up
        os.remove(output_file)

    def test_csv_data_loader_without_id(self):
        # Create a CSV file without an 'id' column
        no_id_file = "test_data_no_id.csv"
        no_id_data = [["name", "age"], ["John Doe", "30"], ["Jane Smith", "25"]]
        with open(no_id_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(no_id_data)

        loader = CSVDataLoader()
        entities = loader.load(no_id_file)

        self.assertEqual(len(entities), 2)
        self.assertIsInstance(entities[0], Entity)
        self.assertEqual(entities[0].id, "0")
        self.assertEqual(entities[0].attributes["name"], "John Doe")
        self.assertEqual(entities[1].id, "1")
        self.assertEqual(entities[1].attributes["age"], "25")

        # Clean up
        os.remove(no_id_file)


if __name__ == "__main__":
    unittest.main()

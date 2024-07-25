import json
import os
import unittest

from rezolva.core.base import Entity
from rezolva.data_handlers.json_handlers import JSONDataLoader, JSONDataSaver


class TestJSONHandlers(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_data.json"
        self.test_data = [
            {"id": "1", "attributes": {"name": "John Doe", "age": 30}},
            {"id": "2", "attributes": {"name": "Jane Smith", "age": 25}},
        ]
        with open(self.test_file, "w") as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_json_data_loader(self):
        loader = JSONDataLoader()
        entities = loader.load(self.test_file)

        self.assertEqual(len(entities), 2)
        self.assertIsInstance(entities[0], Entity)
        self.assertEqual(entities[0].id, "1")
        self.assertEqual(entities[0].attributes["name"], "John Doe")
        self.assertEqual(entities[1].id, "2")
        self.assertEqual(entities[1].attributes["age"], 25)

    def test_json_data_saver(self):
        entities = [Entity("3", {"name": "Alice Johnson", "age": 35}), Entity("4", {"name": "Bob Williams", "age": 40})]
        saver = JSONDataSaver()
        output_file = "output_test_data.json"
        saver.save(entities, output_file)

        # Check if the file was created
        self.assertTrue(os.path.exists(output_file))

        # Load the saved data and verify
        with open(output_file, "r") as f:
            saved_data = json.load(f)

        self.assertEqual(len(saved_data), 2)
        self.assertEqual(saved_data[0]["id"], "3")
        self.assertEqual(saved_data[0]["attributes"]["name"], "Alice Johnson")
        self.assertEqual(saved_data[1]["id"], "4")
        self.assertEqual(saved_data[1]["attributes"]["age"], 40)

        # Clean up
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()

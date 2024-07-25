import unittest

from rezolva.core.base import Entity
from rezolva.model_builders.simple_model_builder import SimpleModelBuilder


class TestSimpleModelBuilder(unittest.TestCase):
    def setUp(self):
        self.model_builder = SimpleModelBuilder(["name", "age"])

    def test_train(self):
        entities = [Entity("1", {"name": "John Doe", "age": "30"}), Entity("2", {"name": "Jane Smith", "age": "25"})]
        model = self.model_builder.train(entities)

        self.assertIn("entities", model)
        self.assertIn("index", model)
        self.assertEqual(len(model["entities"]), 2)
        self.assertIn("name", model["index"])
        self.assertIn("age", model["index"])
        self.assertIn("john doe", model["index"]["name"].keys())
        self.assertIn("30", model["index"]["age"])

    def test_update(self):
        initial_entities = [Entity("1", {"name": "John Doe", "age": "30"})]
        model = self.model_builder.train(initial_entities)

        new_entities = [Entity("2", {"name": "Jane Smith", "age": "25"})]
        updated_model = self.model_builder.update(model, new_entities)

        self.assertEqual(len(updated_model["entities"]), 2)
        self.assertIn("jane smith", updated_model["index"]["name"].keys())
        self.assertIn("25", updated_model["index"]["age"])


if __name__ == "__main__":
    unittest.main()

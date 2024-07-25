import unittest

from rezolva.core.base import Entity
from rezolva.model_builders.inverted_index_model_builder import \
    InvertedIndexModelBuilder


class TestInvertedIndexModelBuilder(unittest.TestCase):
    def setUp(self):
        self.model_builder = InvertedIndexModelBuilder(["name", "description"])

    def test_train(self):
        entities = [
            Entity("1", {"name": "John Doe", "description": "Software Engineer"}),
            Entity("2", {"name": "Jane Smith", "description": "Data Scientist"}),
        ]
        model = self.model_builder.train(entities)

        self.assertIn("entities", model)
        self.assertIn("index", model)
        self.assertEqual(len(model["entities"]), 2)
        self.assertIn("john", model["index"])
        self.assertIn("software", model["index"])
        self.assertIn("data", model["index"])

    def test_update(self):
        initial_entities = [Entity("1", {"name": "John Doe", "description": "Software Engineer"})]
        model = self.model_builder.train(initial_entities)

        new_entities = [Entity("2", {"name": "Jane Smith", "description": "Data Scientist"})]
        updated_model = self.model_builder.update(model, new_entities)

        self.assertEqual(len(updated_model["entities"]), 2)
        self.assertIn("jane", updated_model["index"])
        self.assertIn("data", updated_model["index"])

    def test_tokenize(self):
        text = "Hello, World! This is a test."
        tokens = self.model_builder._tokenize(text)
        expected_tokens = ["hello", "world", "this", "is", "a", "test"]
        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()

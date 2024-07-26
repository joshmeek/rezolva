import math
import unittest

from rezolva.core.base import Entity
from rezolva.model_builders.simple_vector_model_builder import \
    SimpleVectorModelBuilder


class TestSimpleVectorModelBuilder(unittest.TestCase):
    def setUp(self):
        self.model_builder = SimpleVectorModelBuilder(["name", "description"])

    def test_train(self):
        entities = [
            Entity("1", {"name": "John Doe", "description": "Software Engineer"}),
            Entity("2", {"name": "Jane Smith", "description": "Data Scientist"}),
        ]
        model = self.model_builder.train(entities)

        self.assertIn("entities", model)
        self.assertIn("vectors", model)
        self.assertIn("idf", model)
        self.assertEqual(len(model["entities"]), 2)
        self.assertIn("1", model["vectors"])
        self.assertIn("2", model["vectors"])
        self.assertIn("john", model["idf"])
        self.assertIn("software", model["idf"])

    def test_update(self):
        initial_entities = [Entity("1", {"name": "John Doe", "description": "Software Engineer"})]
        model = self.model_builder.train(initial_entities)

        new_entities = [Entity("2", {"name": "Jane Smith", "description": "Data Scientist"})]
        updated_model = self.model_builder.update(model, new_entities)

        self.assertEqual(len(updated_model["entities"]), 2)
        self.assertIn("1", updated_model["vectors"])
        self.assertIn("2", updated_model["vectors"])
        self.assertIn("jane", updated_model["idf"])
        self.assertIn("data", updated_model["idf"])

    def test_idf_calculation(self):
        entities = [
            Entity("1", {"name": "John Doe", "description": "Software Engineer"}),
            Entity("2", {"name": "Jane Smith", "description": "Data Scientist"}),
            Entity("3", {"name": "Bob Johnson", "description": "Software Developer"}),
        ]
        model = self.model_builder.train(entities)

        expected_idf_software = math.log(3 / 3)  # appears in 2 out of 3 documents, but +1 for smoothing
        self.assertAlmostEqual(model["idf"]["software"], expected_idf_software, places=6)

        expected_idf_data = math.log(3 / 2)  # appears in 1 out of 3 documents, but +1 for smoothing
        self.assertAlmostEqual(model["idf"]["data"], expected_idf_data, places=6)

    def test_vector_calculation(self):
        entities = [
            Entity("1", {"name": "John Doe", "description": "Software Engineer"}),
            Entity("2", {"name": "Jane Smith", "description": "Data Scientist"}),
        ]
        model = self.model_builder.train(entities)

        # Check vector for "John Doe"
        john_vector = model["vectors"]["1"]
        self.assertIn("john", john_vector)
        self.assertIn("software", john_vector)
        self.assertNotIn("data", john_vector)

        # Verify TF-IDF calculation
        tf_john = 1 / 4  # "john" appears once in a total of 4 words
        idf_john = math.log(2 / 2)  # "john" appears in 1 out of 2 documents, but +1 for smoothing
        expected_tfidf_john = tf_john * idf_john
        self.assertAlmostEqual(john_vector["john"], expected_tfidf_john, places=6)

    def test_empty_entity(self):
        entities = [Entity("1", {"name": "", "description": ""})]
        model = self.model_builder.train(entities)
        self.assertEqual(len(model["vectors"]["1"]), 0)

    def test_non_string_attribute(self):
        entities = [Entity("1", {"name": "John Doe", "description": 12345})]
        model = self.model_builder.train(entities)
        self.assertIn("12345", model["vectors"]["1"])


if __name__ == "__main__":
    unittest.main()

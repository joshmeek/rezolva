import math
import unittest

from rezolva.core.base import Entity
from rezolva.matchers.cosine_similarity_matcher import CosineSimilarityMatcher


class TestCosineSimilarityMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = CosineSimilarityMatcher(threshold=0.5, attribute_weights={"title": 1.0, "description": 0.5})

    def test_match_string_based(self):
        entity = Entity("1", {"title": "iPhone", "description": "Smartphone by Apple"})
        model = {
            "entities": {
                "2": Entity("2", {"title": "iPhone", "description": "Apple's smartphone"}),
                "3": Entity("3", {"title": "Galaxy", "description": "Smartphone by Samsung"}),
            }
        }

        matches = self.matcher.match(entity, model)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "2")
        self.assertGreater(matches[0][1], 0.5)

    def test_match_vector_based(self):
        entity = Entity("1", {"title": "iPhone", "description": "Smartphone by Apple"})
        model = {
            "entities": {
                "1": entity,
                "2": Entity("2", {"title": "iPhone", "description": "Apple's smartphone"}),
                "3": Entity("3", {"title": "Galaxy", "description": "Smartphone by Samsung"}),
            },
            "vectors": {
                "1": {"iphone": 0.7, "smartphone": 0.5, "apple": 0.3},
                "2": {"iphone": 0.7, "smartphone": 0.3, "apple": 0.5},
                "3": {"galaxy": 0.7, "smartphone": 0.5, "samsung": 0.3},
            },
            "idf": {
                "iphone": math.log(3 / 2),
                "smartphone": math.log(3 / 3),
                "apple": math.log(3 / 2),
                "galaxy": math.log(3 / 1),
                "samsung": math.log(3 / 1),
            },
        }

        matches = self.matcher.match(entity, model)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "2")
        self.assertGreater(matches[0][1], 0.5)

    def test_cosine_similarity_vectors(self):
        vec1 = {"a": 1, "b": 2, "c": 3}
        vec2 = {"b": 2, "c": 3, "d": 4}
        similarity = self.matcher._cosine_similarity_vectors(vec1, vec2)
        expected_similarity = 0.6451791670811048
        self.assertAlmostEqual(similarity, expected_similarity, places=6)


if __name__ == "__main__":
    unittest.main()

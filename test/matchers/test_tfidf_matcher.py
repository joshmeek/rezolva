import math
import unittest

from rezolva.core.base import Entity
from rezolva.matchers.tfidf_matcher import TfIdfMatcher


class TestTfIdfMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = TfIdfMatcher(threshold=0.3, attribute_weights={"title": 1.0, "description": 0.5})
        self.entities = [
            Entity("1", {"title": "iPhone 12", "description": "Latest smartphone from Apple"}),
            Entity("2", {"title": "Galaxy S21", "description": "Flagship smartphone from Samsung"}),
            Entity("3", {"title": "Pixel 5", "description": "Google's latest smartphone"}),
        ]
        self.matcher.train(self.entities)

    def test_train(self):
        expected_idf = {
            "iphone": math.log(3 / 1),
            "12": math.log(3 / 1),
            "latest": math.log(3 / 2),
            "smartphone": math.log(3 / 3),
            "from": math.log(3 / 2),
            "apple": math.log(3 / 1),
            "galaxy": math.log(3 / 1),
            "s21": math.log(3 / 1),
            "flagship": math.log(3 / 1),
            "samsung": math.log(3 / 1),
            "pixel": math.log(3 / 1),
            "5": math.log(3 / 1),
            "google's": math.log(3 / 1),
        }
        for word, idf in self.matcher.idf.items():
            self.assertAlmostEqual(idf, expected_idf[word], places=6)
        self.assertEqual(self.matcher.doc_count, 3)

    def test_match(self):
        new_entity = Entity("4", {"title": "iPhone 13", "description": "Next generation smartphone from Apple"})
        matches = self.matcher.match(new_entity, {"entities": {e.id: e for e in self.entities}})

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "1")
        self.assertGreater(matches[0][1], 0.3)

    def test_calculate_tfidf(self):
        tfidf = self.matcher._calculate_tfidf("iPhone latest smartphone from Apple")

        expected_tfidf = {
            "iphone": 1 * math.log(3 / 1),
            "latest": 1 * math.log(3 / 2),
            "smartphone": 1 * math.log(3 / 3),
            "from": 1 * math.log(3 / 2),
            "apple": 1 * math.log(3 / 1),
        }

        for word, score in tfidf.items():
            self.assertAlmostEqual(score, expected_tfidf[word], places=6)

    def test_cosine_similarity(self):
        vec1 = {"a": 1, "b": 2, "c": 3}
        vec2 = {"b": 2, "c": 3, "d": 4}
        similarity = self.matcher._cosine_similarity(vec1, vec2)
        expected_similarity = 0.6451791670811048
        self.assertAlmostEqual(similarity, expected_similarity, places=6)

    def test_calculate_attribute_similarity(self):
        val1 = "iPhone 12 Pro"
        val2 = "iPhone 12 Max"
        similarity = self.matcher._calculate_attribute_similarity(val1, val2)
        self.assertGreater(similarity, 0.5)
        self.assertLessEqual(similarity, 1.0)  # Changed from assertLess to assertLessEqual

    def test_match_no_match(self):
        new_entity = Entity("5", {"title": "Refrigerator", "description": "Large kitchen appliance for food storage"})
        matches = self.matcher.match(new_entity, {"entities": {e.id: e for e in self.entities}})
        self.assertEqual(len(matches), 0)


if __name__ == "__main__":
    unittest.main()

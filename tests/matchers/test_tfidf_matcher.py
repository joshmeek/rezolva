import math
import unittest

from start_er.core.base import Entity
from start_er.matchers.tfidf_matcher import TfIdfMatcher


class TestTfIdfMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = TfIdfMatcher(threshold=0.3, attribute_weights={'title': 1.0, 'description': 0.5})

    def test_train_and_match(self):
        entities = [
            Entity("1", {"title": "iPhone 12", "description": "Latest smartphone from Apple"}),
            Entity("2", {"title": "Galaxy S21", "description": "Flagship smartphone from Samsung"}),
            Entity("3", {"title": "Pixel 5", "description": "Google's latest smartphone"})
        ]
        self.matcher.train(entities)

        new_entity = Entity("4", {"title": "iPhone 13", "description": "Next generation smartphone from Apple"})
        matches = self.matcher.match(new_entity, {'entities': {e.id: e for e in entities}})

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "1")
        self.assertGreater(matches[0][1], 0.3)

    def test_calculate_tfidf(self):
        self.matcher.idf = {
            "iphone": math.log(3/1),
            "smartphone": math.log(3/3),
            "apple": math.log(3/1),
            "latest": math.log(3/1)
        }
        self.matcher.doc_count = 3

        tfidf = self.matcher._calculate_tfidf("iPhone latest smartphone from Apple")
        
        expected_tfidf = {
            "iphone": (1/4) * math.log(3/1),
            "smartphone": (1/4) * math.log(3/3),
            "apple": (1/4) * math.log(3/1),
            "latest": (1/4) * math.log(3/1)
        }

        for word, score in tfidf.items():
            self.assertAlmostEqual(score, expected_tfidf[word], places=6)

    def test_cosine_similarity(self):
        vec1 = {"a": 1, "b": 2, "c": 3}
        vec2 = {"b": 2, "c": 3, "d": 4}
        similarity = self.matcher._cosine_similarity(vec1, vec2)
        expected_similarity = 0.9428090415820634
        self.assertAlmostEqual(similarity, expected_similarity, places=6)

if __name__ == '__main__':
    unittest.main()
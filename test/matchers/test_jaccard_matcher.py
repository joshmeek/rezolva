import unittest

from rezolva.core.base import Entity
from rezolva.matchers.jaccard_matcher import JaccardMatcher


class TestJaccardMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = JaccardMatcher(threshold=0.3, attribute_weights={"title": 1.0, "description": 0.5})

    def test_match(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest smartphone from Apple"})
        model = {
            "entities": {
                "2": Entity("2", {"title": "iPhone 12 Pro", "description": "Advanced smartphone from Apple"}),
                "3": Entity("3", {"title": "Galaxy S21", "description": "Latest smartphone from Samsung"}),
            }
        }

        matches = self.matcher.match(entity, model)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "2")
        self.assertGreater(matches[0][1], 0.3)

    def test_calculate_attribute_similarity(self):
        similarities = [
            self.matcher._calculate_attribute_similarity("hello world", "hello earth"),
            self.matcher._calculate_attribute_similarity("", ""),
            self.matcher._calculate_attribute_similarity("abc def", "abc def ghi"),
            self.matcher._calculate_attribute_similarity("completely different", "totally distinct"),
        ]

        expected_similarities = [0.3333333333333333, 1.0, 0.6666666666666666, 0.0]

        for sim, expected_sim in zip(similarities, expected_similarities):
            self.assertAlmostEqual(sim, expected_sim, places=6)


if __name__ == "__main__":
    unittest.main()

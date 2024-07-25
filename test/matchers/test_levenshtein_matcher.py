import unittest

from rezolva.core.base import Entity
from rezolva.matchers.levenshtein_matcher import LevenshteinMatcher


class TestLevenshteinMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = LevenshteinMatcher(threshold=0.7, attribute_weights={"name": 1.0, "description": 0.5})

    def test_match(self):
        entity = Entity("1", {"name": "John Doe", "description": "Software Engineer"})
        model = {
            "entities": {
                "2": Entity("2", {"name": "Jon Doe", "description": "Software Developer"}),
                "3": Entity("3", {"name": "Jane Smith", "description": "Data Scientist"}),
            }
        }

        matches = self.matcher.match(entity, model)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "2")
        self.assertGreater(matches[0][1], 0.7)

    def test_calculate_attribute_similarity(self):
        similarities = [
            self.matcher._calculate_attribute_similarity("kitten", "sitting"),
            self.matcher._calculate_attribute_similarity("", ""),
            self.matcher._calculate_attribute_similarity("book", "back"),
            self.matcher._calculate_attribute_similarity("completely different", "totally distinct"),
        ]

        expected_similarities = [0.5714285714285714, 1.0, 0.5, 0.4]

        for sim, expected_sim in zip(similarities, expected_similarities):
            self.assertAlmostEqual(sim, expected_sim, places=6)

    def test_levenshtein_distance(self):
        distances = [
            self.matcher._levenshtein_distance("kitten", "sitting"),
            self.matcher._levenshtein_distance("", ""),
            self.matcher._levenshtein_distance("book", "back"),
            self.matcher._levenshtein_distance("completely", "different"),
        ]

        expected_distances = [3, 0, 2, 8]

        for dist, expected_dist in zip(distances, expected_distances):
            self.assertEqual(dist, expected_dist)


if __name__ == "__main__":
    unittest.main()

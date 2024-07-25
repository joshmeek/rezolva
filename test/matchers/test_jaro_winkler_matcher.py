import unittest

from rezolva.core.base import Entity
from rezolva.matchers.jaro_winkler_matcher import JaroWinklerMatcher


class TestJaroWinklerMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = JaroWinklerMatcher(threshold=0.8, attribute_weights={"name": 1.0, "description": 0.5})

    def test_match(self):
        entity = Entity("1", {"name": "Martha", "description": "Software Engineer"})
        model = {
            "entities": {
                "2": Entity("2", {"name": "Marhta", "description": "Software Developer"}),
                "3": Entity("3", {"name": "John", "description": "Data Scientist"}),
            }
        }

        matches = self.matcher.match(entity, model)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "2")
        self.assertGreater(matches[0][1], 0.8)

    def test_jaro_winkler_similarity(self):
        similarities = [
            self.matcher._jaro_winkler_similarity("MARTHA", "MARHTA"),
            self.matcher._jaro_winkler_similarity("DWAYNE", "DUANE"),
            self.matcher._jaro_winkler_similarity("DIXON", "DICKSONX"),
            self.matcher._jaro_winkler_similarity("", ""),
        ]

        expected_similarities = [0.9611111111111111, 0.84, 0.8133333333333332, 1.0]

        for sim, expected_sim in zip(similarities, expected_similarities):
            self.assertAlmostEqual(sim, expected_sim, places=6)

    def test_jaro_distance(self):
        distances = [
            self.matcher._jaro_distance("MARTHA", "MARHTA"),
            self.matcher._jaro_distance("DWAYNE", "DUANE"),
            self.matcher._jaro_distance("DIXON", "DICKSONX"),
            self.matcher._jaro_distance("", ""),
        ]

        expected_distances = [0.9444444444444445, 0.8222222222222223, 0.7666666666666666, 1.0]

        for dist, expected_dist in zip(distances, expected_distances):
            self.assertAlmostEqual(dist, expected_dist, places=6)


if __name__ == "__main__":
    unittest.main()

import unittest

from rezolva.core.base import Entity
from rezolva.matchers.base_matcher import BaseAttributeMatcher


class DummyMatcher(BaseAttributeMatcher):
    def _calculate_attribute_similarity(self, val1, val2):
        return 1.0 if val1 == val2 else 0.0


class TestBaseAttributeMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = DummyMatcher(threshold=0.5, attribute_weights={"name": 1.0, "age": 0.5})

    def test_match(self):
        entity = Entity("1", {"name": "John", "age": "30"})
        model = {
            "entities": {
                "2": Entity("2", {"name": "John", "age": "31"}),
                "3": Entity("3", {"name": "Jane", "age": "30"}),
                "4": Entity("4", {"name": "John", "age": "30"}),
            }
        }

        matches = self.matcher.match(entity, model)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0][0].id, "4")
        self.assertEqual(matches[0][1], 1.0)
        self.assertEqual(matches[1][0].id, "2")
        self.assertAlmostEqual(matches[1][1], 0.6666666666666666)

    def test_calculate_weighted_similarity(self):
        entity1 = Entity("1", {"name": "John", "age": "30"})
        entity2 = Entity("2", {"name": "John", "age": "31"})

        similarity = self.matcher._calculate_weighted_similarity(entity1, entity2)
        self.assertAlmostEqual(similarity, 0.6666666666666666)


if __name__ == "__main__":
    unittest.main()

import unittest

from rezolva.core.base import Entity
from rezolva.matchers.decision_tree_matcher import DecisionTreeMatcher


class TestSimpleDecisionTreeMatcher(unittest.TestCase):
    def setUp(self):
        self.entities = [
            Entity("1", {"name": "John Doe", "age": "30", "city": "New York"}),
            Entity("2", {"name": "Jane Smith", "age": "25", "city": "Los Angeles"}),
            Entity("3", {"name": "John Smith", "age": "35", "city": "Chicago"}),
            Entity("4", {"name": "Jane Doe", "age": "28", "city": "New York"}),
        ]
        self.matcher = DecisionTreeMatcher(attributes=["name", "age", "city"])

    def test_train_and_match(self):
        pairs = [
            (self.entities[0], self.entities[1]),
            (self.entities[0], self.entities[2]),
            (self.entities[0], self.entities[3]),
            (self.entities[1], self.entities[2]),
            (self.entities[1], self.entities[3]),
            (self.entities[2], self.entities[3]),
        ]
        labels = [False, False, True, False, False, False]

        self.matcher.train(pairs, labels)
        matches = self.matcher.match(self.entities[0], self.entities[1:])

        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0][0].id, "4")  # Jane Doe should be the best match for John Doe


if __name__ == "__main__":
    unittest.main()

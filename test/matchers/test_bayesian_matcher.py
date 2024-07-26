import unittest
from unittest.mock import patch

from rezolva.core.base import Entity
from rezolva.matchers.bayesian_matcher import BayesianMatcher


class TestBayesianMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = BayesianMatcher(threshold=0.3, attribute_weights={"name": 1.0, "age": 0.5, "city": 0.8})
        self.training_data = [
            Entity("1", {"name": "John Doe", "age": "30", "city": "New York"}),
            Entity("2", {"name": "Jane Smith", "age": "25", "city": "Los Angeles"}),
            Entity("3", {"name": "John Smith", "age": "35", "city": "Chicago"}),
            Entity("4", {"name": "Alice Johnson", "age": "28", "city": "New York"}),
        ]
        self.matcher.train(self.training_data)

    def test_train(self):
        self.assertAlmostEqual(self.matcher.attribute_probabilities["name"]["John Doe"], 0.25)
        self.assertAlmostEqual(self.matcher.attribute_probabilities["city"]["New York"], 0.5)

    def test_match_exact(self):
        entity = Entity("5", {"name": "John Doe", "age": "30", "city": "New York"})
        model = {"entities": {e.id: e for e in self.training_data}}
        matches = self.matcher.match(entity, model)

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "1")
        self.assertGreater(matches[0][1], 0.6)
        self.assertLess(matches[0][1], 0.7)

    def test_match_partial(self):
        entity = Entity("5", {"name": "John Smith", "age": "30", "city": "New York"})
        model = {"entities": {e.id: e for e in self.training_data}}
        matches = self.matcher.match(entity, model)

        self.assertGreater(len(matches), 0)
        self.assertLessEqual(len(matches), 2)
        if len(matches) == 2:
            self.assertIn(matches[0][0].id, ["1", "3"])
            self.assertIn(matches[1][0].id, ["1", "3"])
        elif len(matches) == 1:
            self.assertIn(matches[0][0].id, ["1", "3"])

    def test_match_no_match(self):
        entity = Entity("5", {"name": "Bob Brown", "age": "40", "city": "Miami"})
        model = {"entities": {e.id: e for e in self.training_data}}
        matches = self.matcher.match(entity, model)

        self.assertEqual(len(matches), 0)

    def test_calculate_similarity(self):
        entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        entity2 = Entity("2", {"name": "John Smith", "age": "30", "city": "Chicago"})

        similarity = self.matcher._calculate_similarity(entity1, entity2)
        self.assertGreater(similarity, 0.3)
        self.assertLess(similarity, 0.5)

    @patch.object(BayesianMatcher, "_jaccard_similarity")
    def test_jaccard_similarity_called(self, mock_jaccard):
        mock_jaccard.return_value = 0.5
        entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        entity2 = Entity("2", {"name": "Jane Doe", "age": "30", "city": "Los Angeles"})

        self.matcher._calculate_similarity(entity1, entity2)
        mock_jaccard.assert_called()

    def test_jaccard_similarity(self):
        self.assertAlmostEqual(self.matcher._jaccard_similarity("John Doe", "John Smith"), 0.3333333333333333)
        self.assertEqual(self.matcher._jaccard_similarity("New York", "Los Angeles"), 0.0)
        self.assertEqual(self.matcher._jaccard_similarity("", ""), 0.0)


if __name__ == "__main__":
    unittest.main()

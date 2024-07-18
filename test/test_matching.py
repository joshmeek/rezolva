import unittest
from tiny_er.core.data_structures import Entity, Comparison, MatchResult
from tiny_er.matching.rule_based import ThresholdMatcher
from tiny_er.matching.probabilistic import FellegiSunterMatcher
from tiny_er.matching.machine_learning import SimpleLogisticRegressionMatcher

class TestMatching(unittest.TestCase):
    def setUp(self):
        self.entity1 = Entity("1", {"name": "John", "age": "30"})
        self.entity2 = Entity("2", {"name": "Johnny", "age": "31"})
        self.entity3 = Entity("3", {"name": "Jane", "age": "25"})
        self.comparison1 = Comparison(self.entity1, self.entity2, 0.8)
        self.comparison2 = Comparison(self.entity1, self.entity3, 0.3)

    def test_threshold_matcher(self):
        matcher = ThresholdMatcher({"threshold": 0.7})
        results = matcher.match([self.comparison1, self.comparison2])
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].is_match)
        self.assertFalse(results[1].is_match)

    def test_simple_logistic_regression_matcher(self):
        config = {
            "learning_rate": 0.01,
            "num_iterations": 100,
            "threshold": 0.5
        }
        matcher = SimpleLogisticRegressionMatcher(config)
        
        # Training data
        labeled_comparisons = [
            (Comparison(self.entity1, self.entity2, 0.8), 1),
            (Comparison(self.entity1, self.entity3, 0.3), 0)
        ]
        matcher.train(labeled_comparisons)
        
        results = matcher.match([self.comparison1, self.comparison2])
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0].confidence, float)
        self.assertIsInstance(results[1].confidence, float)

class TestFellegiSunterMatcher(unittest.TestCase):
    def setUp(self):
        self.config = {
            "m_probabilities": {"name": 0.9, "age": 0.8, "city": 0.7},
            "u_probabilities": {"name": 0.1, "age": 0.3, "city": 0.2},
            "threshold": 0
        }
        self.matcher = FellegiSunterMatcher(self.config)

    def test_exact_match(self):
        entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        entity2 = Entity("2", {"name": "John Doe", "age": "30", "city": "New York"})
        comparison = Comparison(entity1, entity2, 1.0)
        result = self.matcher._match_pair(comparison)
        self.assertTrue(result.is_match)
        self.assertGreater(result.confidence, 0)

    def test_no_match(self):
        entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        entity2 = Entity("2", {"name": "Jane Smith", "age": "25", "city": "Los Angeles"})
        comparison = Comparison(entity1, entity2, 0.0)
        result = self.matcher._match_pair(comparison)
        self.assertFalse(result.is_match)
        self.assertLess(result.confidence, 0)

    def test_partial_match(self):
        entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        entity2 = Entity("2", {"name": "John Doe", "age": "31", "city": "Boston"})
        comparison = Comparison(entity1, entity2, 0.5)
        result = self.matcher._match_pair(comparison)
        self.assertTrue(result.is_match)  # Assuming threshold is 0
        self.assertGreater(result.confidence, 0)

    def test_missing_fields(self):
        entity1 = Entity("1", {"name": "John Doe", "age": "30"})
        entity2 = Entity("2", {"name": "John Doe", "city": "New York"})
        comparison = Comparison(entity1, entity2, 0.5)
        result = self.matcher._match_pair(comparison)
        self.assertTrue(result.is_match)  # Assuming threshold is 0
        self.assertGreater(result.confidence, 0)

    def test_threshold(self):
        high_threshold_config = self.config.copy()
        high_threshold_config["threshold"] = 5
        high_threshold_matcher = FellegiSunterMatcher(high_threshold_config)

        entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        entity2 = Entity("2", {"name": "John Doe", "age": "31", "city": "Boston"})
        comparison = Comparison(entity1, entity2, 0.5)
        
        result_low_threshold = self.matcher._match_pair(comparison)
        result_high_threshold = high_threshold_matcher._match_pair(comparison)

        self.assertTrue(result_low_threshold.is_match)
        self.assertFalse(result_high_threshold.is_match)
        self.assertEqual(result_low_threshold.confidence, result_high_threshold.confidence)

    def test_multiple_comparisons(self):
        entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        entity2 = Entity("2", {"name": "Jane Smith", "age": "25", "city": "Los Angeles"})
        entity3 = Entity("3", {"name": "John Doe", "age": "31", "city": "Boston"})

        comparisons = [
            Comparison(entity1, entity2, 0.0),
            Comparison(entity1, entity3, 0.5),
            Comparison(entity2, entity3, 0.0)
        ]

        results = self.matcher.match(comparisons)
        self.assertEqual(len(results), 3)
        self.assertFalse(results[0].is_match)
        self.assertTrue(results[1].is_match)
        self.assertFalse(results[2].is_match)

if __name__ == '__main__':
    unittest.main()
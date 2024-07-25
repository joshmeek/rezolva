import unittest
from unittest.mock import Mock, patch

from rezolva import Entity, EntityResolver
from rezolva.utils.evaluation import (calculate_accuracy,
                                      calculate_precision_recall_f1,
                                      cross_validate, evaluate_resolver,
                                      generate_performance_report)


class TestEvaluationUtils(unittest.TestCase):
    def test_calculate_precision_recall_f1(self):
        # Test with some sample values
        precision, recall, f1 = calculate_precision_recall_f1(true_positives=8, false_positives=2, false_negatives=1)
        self.assertAlmostEqual(precision, 0.8, places=2)
        self.assertAlmostEqual(recall, 0.8888888888888888, places=4)
        self.assertAlmostEqual(f1, 0.8421, places=4)

        # Test with zero values
        precision, recall, f1 = calculate_precision_recall_f1(true_positives=0, false_positives=0, false_negatives=0)
        self.assertEqual(precision, 0)
        self.assertEqual(recall, 0)
        self.assertEqual(f1, 0)

    def test_calculate_accuracy(self):
        accuracy = calculate_accuracy(true_positives=80, true_negatives=15, total_comparisons=100)
        self.assertEqual(accuracy, 0.95)

        # Test with zero total comparisons
        accuracy = calculate_accuracy(true_positives=0, true_negatives=0, total_comparisons=0)
        self.assertEqual(accuracy, 0)

    @patch("rezolva.EntityResolver")
    def test_evaluate_resolver(self, mock_resolver):
        # Mock the resolver and its resolve method
        mock_resolver.resolve.return_value = [
            (Entity("1", {"name": "Entity 1"}), [(Entity("2", {"name": "Entity 2"}), 0.8)]),
            (Entity("3", {"name": "Entity 3"}), []),
        ]

        test_entities = [
            Entity("1", {"name": "Entity 1"}),
            Entity("2", {"name": "Entity 2"}),
            Entity("3", {"name": "Entity 3"}),
        ]

        ground_truth = {"1": ["2"], "2": ["1"], "3": []}

        metrics = evaluate_resolver(mock_resolver, test_entities, ground_truth)

        self.assertIn("precision", metrics)
        self.assertIn("recall", metrics)
        self.assertIn("f1", metrics)
        self.assertIn("accuracy", metrics)

    def test_generate_performance_report(self):
        metrics = {"precision": 0.8, "recall": 0.75, "f1": 0.7741, "accuracy": 0.9}

        report = generate_performance_report(metrics)

        self.assertIn("Precision: 0.800", report)
        self.assertIn("Recall: 0.750", report)
        self.assertIn("F1 Score: 0.774", report)
        self.assertIn("Accuracy: 0.900", report)

    @patch("rezolva.EntityResolver")
    @patch("rezolva.utils.evaluation.evaluate_resolver")
    def test_cross_validate(self, mock_evaluate_resolver, mock_resolver):
        # Mock the evaluate_resolver function
        mock_evaluate_resolver.return_value = {"precision": 0.8, "recall": 0.75, "f1": 0.7741, "accuracy": 0.9}

        entities = [Entity(str(i), {"name": f"Entity {i}"}) for i in range(10)]
        ground_truth = {str(i): [] for i in range(10)}

        results = cross_validate(mock_resolver, entities, ground_truth, k=5)

        self.assertEqual(len(results["precision"]), 5)
        self.assertEqual(len(results["recall"]), 5)
        self.assertEqual(len(results["f1"]), 5)
        self.assertEqual(len(results["accuracy"]), 5)


if __name__ == "__main__":
    unittest.main()

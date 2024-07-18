import unittest
from tiny_er.core.data_structures import Entity, MatchResult
from tiny_er.evaluation.metrics import calculate_metrics, evaluate
from tiny_er.evaluation.cross_validation import k_fold_cross_validation, train_test_split

class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.entities = [
            Entity("1", {"name": "John Doe", "age": "30"}),
            Entity("2", {"name": "Jane Doe", "age": "28"}),
            Entity("3", {"name": "John Smith", "age": "35"}),
            Entity("4", {"name": "Jane Smith", "age": "32"})
        ]
        self.true_matches = [("1", "2"), ("3", "4")]

    def test_calculate_metrics(self):
        predicted_matches = [
            MatchResult(self.entities[0], self.entities[1], 0.9, True),
            MatchResult(self.entities[0], self.entities[2], 0.6, True),
            MatchResult(self.entities[2], self.entities[3], 0.8, True)
        ]
        metrics = calculate_metrics(self.true_matches, predicted_matches)
        
        self.assertAlmostEqual(metrics["precision"], 2/3, places=2)
        self.assertAlmostEqual(metrics["recall"], 1.0, places=2)
        self.assertAlmostEqual(metrics["f1_score"], 0.8, places=2)

    def test_evaluate(self):
        predicted_matches = [
            MatchResult(self.entities[0], self.entities[1], 0.9, True),
            MatchResult(self.entities[2], self.entities[3], 0.8, True)
        ]
        config = {"metrics": ["precision", "recall"]}
        results = evaluate(self.true_matches, predicted_matches, config)
        
        self.assertIn("precision", results)
        self.assertIn("recall", results)
        self.assertNotIn("f1_score", results)
        self.assertEqual(results["precision"], 1.0)
        self.assertEqual(results["recall"], 1.0)

    def test_k_fold_cross_validation(self):
        def mock_resolver(entities):
            results = []
            for i in range(len(entities)):
                for j in range(i + 1, len(entities)):
                    if entities[i].attributes['name'].split()[0] == entities[j].attributes['name'].split()[0]:
                        results.append(MatchResult(entities[i], entities[j], 1.0, True))
            return results

        results = k_fold_cross_validation(self.entities, mock_resolver, self.true_matches, k=2)
        
        self.assertIn("precision", results)
        self.assertIn("recall", results)
        self.assertIn("f1_score", results)
        
        print(f"K-fold cross-validation results: {results}")
        
        self.assertGreaterEqual(results["precision"], 0)
        self.assertGreaterEqual(results["recall"], 0)
        self.assertGreaterEqual(results["f1_score"], 0)
        self.assertLessEqual(results["precision"], 1)
        self.assertLessEqual(results["recall"], 1)
        self.assertLessEqual(results["f1_score"], 1)

    def test_train_test_split(self):
        train_entities, test_entities, train_matches, test_matches = train_test_split(
            self.entities, self.true_matches, test_size=0.5, random_state=42
        )
        
        self.assertEqual(len(train_entities) + len(test_entities), len(self.entities))
        self.assertGreater(len(train_matches) + len(test_matches), 0)

        # Check that all matches are valid
        for match in train_matches:
            self.assertTrue(match[0] in [e.id for e in train_entities] and match[1] in [e.id for e in train_entities])
        for match in test_matches:
            self.assertTrue(match[0] in [e.id for e in test_entities] and match[1] in [e.id for e in test_entities])

        # Print debug information
        print(f"Train entities: {[e.id for e in train_entities]}")
        print(f"Test entities: {[e.id for e in test_entities]}")
        print(f"Train matches: {train_matches}")
        print(f"Test matches: {test_matches}")

        # Additional checks
        self.assertGreaterEqual(len(train_entities), 2)
        self.assertGreaterEqual(len(test_entities), 2)
        self.assertLessEqual(len(train_matches) + len(test_matches), len(self.true_matches))

if __name__ == '__main__':
    unittest.main()
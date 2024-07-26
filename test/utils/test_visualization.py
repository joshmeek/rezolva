import unittest
from unittest.mock import Mock, patch

from rezolva import Entity, EntityResolver
from rezolva.utils.visualization import (ResolutionVisualizer,
                                         visualize_resolution_process)


class TestResolutionVisualizer(unittest.TestCase):
    def setUp(self):
        self.mock_resolver = Mock(spec=EntityResolver)
        self.mock_resolver.preprocessor = Mock()
        self.mock_resolver.blocker = Mock()
        self.mock_resolver.matcher = Mock()
        self.mock_resolver.model = {
            "entities": {
                "1": Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
                "2": Entity(
                    "2", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}
                ),
            }
        }

        self.mock_resolver.matcher.threshold = 0.5
        self.mock_resolver.matcher.attribute_weights = {"title": 2.0, "description": 1.5, "brand": 1.0}
        self.mock_resolver.preprocessor.preprocessing_functions = [
            Mock(__name__="lowercase"),
            Mock(__name__="strip_whitespace"),
        ]

        self.visualizer = ResolutionVisualizer(self.mock_resolver)

    def test_visualize_model_info(self):
        info = self.visualizer._visualize_model_info()
        self.assertIn("Total entities in model: 2", info)
        self.assertIn("Matcher threshold: 0.5", info)
        self.assertIn("Attribute weights", info)
        self.assertIn('"title": 2.0', info)
        self.assertIn('"description": 1.5', info)
        self.assertIn('"brand": 1.0', info)

    def test_visualize_preprocessing(self):
        original = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        preprocessed = Entity("1", {"title": "iphone 12", "description": "latest apple smartphone", "brand": "apple"})

        self.mock_resolver.preprocessor.preprocess.return_value = preprocessed

        viz = self.visualizer._visualize_preprocessing(original, preprocessed)
        self.assertIn("Original  ->  Preprocessed", viz)
        self.assertIn("title: iPhone 12 -> iphone 12", viz)
        self.assertIn("description: Latest Apple smartphone -> latest apple smartphone", viz)
        self.assertIn("brand: Apple -> apple", viz)
        self.assertIn("lowercase", viz)
        self.assertIn("strip_whitespace", viz)

    def test_visualize_blocking(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        blocks = {"apple": [entity, Entity("2", {"title": "iPhone 11", "brand": "Apple"})]}

        viz = self.visualizer._visualize_blocking(blocks, entity)
        self.assertIn("Block 'apple': 2 entities", viz)
        self.assertIn("Entity assigned to block: 'apple'", viz)
        self.assertIn("Entities in the same block:", viz)
        self.assertIn("- Entity 1: iPhone 12", viz)
        self.assertIn("- Entity 2: iPhone 11", viz)

    def test_visualize_matching(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        matches = [
            (Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}), 0.9),
            (Entity("3", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}), 0.3),
        ]

        self.mock_resolver.matcher._calculate_attribute_similarity.return_value = 0.8

        viz = self.visualizer._visualize_matching(matches, entity)
        self.assertIn("Top matches:", viz)
        self.assertIn("1. Entity 2 (Score: 0.9000)", viz)
        self.assertIn("2. Entity 3 (Score: 0.3000)", viz)
        self.assertIn("Similarity breakdown:", viz)
        self.assertIn("- title: 0.8000 (weight: 2.0)", viz)
        self.assertIn("- description: 0.8000 (weight: 1.5)", viz)
        self.assertIn("- brand: 0.8000 (weight: 1.0)", viz)

    def test_visualize_resolution(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})

        self.mock_resolver.preprocessor.preprocess.return_value = entity
        self.mock_resolver.blocker.create_blocks.return_value = {"apple": [entity]}
        self.mock_resolver.matcher.match.return_value = [
            (Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}), 0.9)
        ]

        # Mock the _visualize_matching method to return a predefined string
        self.visualizer._visualize_matching = Mock(return_value="Mocked matching visualization")

        viz = self.visualizer.visualize_resolution(entity)
        self.assertIn("Resolution process for Entity 1", viz)
        self.assertIn("0. Model Information", viz)
        self.assertIn("1. Preprocessing", viz)
        self.assertIn("2. Blocking", viz)
        self.assertIn("3. Matching", viz)
        self.assertIn("Mocked matching visualization", viz)

        # Verify that _visualize_matching was called with the correct arguments
        self.visualizer._visualize_matching.assert_called_once()
        call_args = self.visualizer._visualize_matching.call_args[0]
        self.assertEqual(len(call_args), 2)
        self.assertIsInstance(call_args[0], list)
        self.assertIsInstance(call_args[1], Entity)

    @patch("rezolva.utils.visualization.ResolutionVisualizer")
    def test_visualize_resolution_process(self, MockVisualizer):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})

        mock_instance = MockVisualizer.return_value
        mock_instance.visualize_resolution.return_value = "Mocked visualization"

        result = visualize_resolution_process(self.mock_resolver, entity)

        MockVisualizer.assert_called_once_with(self.mock_resolver)
        mock_instance.visualize_resolution.assert_called_once_with(entity)
        self.assertEqual(result, "Mocked visualization")


if __name__ == "__main__":
    unittest.main()

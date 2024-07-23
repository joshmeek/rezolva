import unittest
from unittest.mock import Mock, patch

from start_er import Entity, EntityResolver
from start_er.utils.visualization import (ResolutionVisualizer,
                                          visualize_resolution_process)


class TestResolutionVisualizer(unittest.TestCase):

    def setUp(self):
        # Create a mock resolver
        self.mock_resolver = Mock(spec=EntityResolver)
        self.mock_resolver.preprocessor = Mock()
        self.mock_resolver.blocker = Mock()
        self.mock_resolver.matcher = Mock()
        self.mock_resolver.model = {
            'entities': {
                '1': Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
                '2': Entity("2", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"})
            }
        }
        
        # Set up mock attributes and methods
        self.mock_resolver.matcher.threshold = 0.5
        self.mock_resolver.matcher.attribute_weights = {'title': 2.0, 'description': 1.5, 'brand': 1.0}
        self.mock_resolver.preprocessor.preprocessing_functions = [Mock(__name__='lowercase'), Mock(__name__='strip_whitespace')]
        
        self.visualizer = ResolutionVisualizer(self.mock_resolver)

    def test_visualize_model_info(self):
        info = self.visualizer._visualize_model_info()
        self.assertIn("Total entities in model: 2", info)
        self.assertIn("Matcher threshold: 0.5", info)
        self.assertIn("Attribute weights", info)

    def test_visualize_preprocessing(self):
        original = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        preprocessed = Entity("1", {"title": "iphone 12", "description": "latest apple smartphone", "brand": "apple"})
        
        self.mock_resolver.preprocessor.preprocess.return_value = preprocessed
        
        viz = self.visualizer._visualize_preprocessing(original, preprocessed)
        self.assertIn("Original  ->  Preprocessed", viz)
        self.assertIn("title: iPhone 12 -> iphone 12", viz)
        self.assertIn("lowercase", viz)
        self.assertIn("strip_whitespace", viz)

    def test_visualize_blocking(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        blocks = {'apple': [entity]}
        
        viz = self.visualizer._visualize_blocking(blocks, entity)
        self.assertIn("Block 'apple': 1 entities", viz)
        self.assertIn("Entity assigned to block: 'apple'", viz)

    def test_visualize_matching(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        matches = [
            (Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}), 0.9),
            (Entity("3", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}), 0.3)
        ]
        
        self.mock_resolver.matcher._calculate_attribute_similarity.return_value = 0.8
        
        viz = self.visualizer._visualize_matching(matches, entity)
        self.assertIn("Top matches:", viz)
        self.assertIn("Entity 2 (Score: 0.9000)", viz)
        self.assertIn("Similarity breakdown:", viz)

    def test_visualize_resolution(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        
        self.mock_resolver.preprocessor.preprocess.return_value = entity
        self.mock_resolver.blocker.create_blocks.return_value = {'apple': [entity]}
        self.mock_resolver.matcher.match.return_value = [
            (Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}), 0.9)
        ]
        
        viz = self.visualizer.visualize_resolution(entity)
        self.assertIn("Resolution process for Entity 1", viz)
        self.assertIn("0. Model Information", viz)
        self.assertIn("1. Preprocessing", viz)
        self.assertIn("2. Blocking", viz)
        self.assertIn("3. Matching", viz)

    def test_visualize_resolution_process(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"})
        
        with patch('start_er.utils.visualization.ResolutionVisualizer') as MockVisualizer:
            mock_instance = MockVisualizer.return_value
            mock_instance.visualize_resolution.return_value = "Mocked visualization"
            
            result = visualize_resolution_process(self.mock_resolver, entity)
            
            MockVisualizer.assert_called_once_with(self.mock_resolver)
            mock_instance.visualize_resolution.assert_called_once_with(entity)
            self.assertEqual(result, "Mocked visualization")

if __name__ == '__main__':
    unittest.main()
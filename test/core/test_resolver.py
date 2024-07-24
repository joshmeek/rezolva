import unittest
from unittest.mock import Mock

from start_er.core.base import Entity
from start_er.core.resolver import EntityResolver


class TestEntityResolver(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Mock()
        self.model_builder = Mock()
        self.matcher = Mock()
        self.blocker = Mock()
        self.resolver = EntityResolver(self.preprocessor, self.model_builder, self.matcher, self.blocker)

    def test_train(self):
        entities = [Entity("1", {"name": "John"}), Entity("2", {"name": "Jane"})]
        self.resolver.train(entities)
        self.preprocessor.preprocess.assert_called()
        self.model_builder.train.assert_called_once()

    def test_resolve(self):
        entities = [Entity("1", {"name": "John"})]
        self.blocker.create_blocks.return_value = {"block1": entities}
        self.matcher.match.return_value = [(Entity("2", {"name": "Jane"}), 0.8)]
        
        self.resolver.train([Entity("1", {"name": "John"})])
        results = self.resolver.resolve(entities)
        
        self.preprocessor.preprocess.assert_called()
        self.blocker.create_blocks.assert_called_once()
        self.matcher.match.assert_called_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].id, "1")
        self.assertEqual(results[0][1][0][0].id, "2")
        self.assertEqual(results[0][1][0][1], 0.8)

if __name__ == '__main__':
    unittest.main()
import pickle
import unittest
from typing import List, Tuple
from unittest.mock import Mock, patch

from rezolva.core.base import (Blocker, Entity, Matcher, ModelBuilder,
                               Preprocessor)
from rezolva.core.resolver import EntityResolver


class TestEntityResolver(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Mock(spec=Preprocessor)
        self.model_builder = Mock(spec=ModelBuilder)
        self.matcher = Mock(spec=Matcher)
        self.blocker = Mock(spec=Blocker)
        self.resolver = EntityResolver(self.preprocessor, self.model_builder, self.matcher, self.blocker)

    def test_init(self):
        self.assertIsInstance(self.resolver, EntityResolver)
        self.assertEqual(self.resolver.preprocessor, self.preprocessor)
        self.assertEqual(self.resolver.model_builder, self.model_builder)
        self.assertEqual(self.resolver.matcher, self.matcher)
        self.assertEqual(self.resolver.blocker, self.blocker)
        self.assertIsNone(self.resolver.model)
        self.assertEqual(self.resolver.preprocessed_entities, {})
        self.assertEqual(self.resolver.blocks, {})

    def test_train(self):
        entities = [Entity("1", {"name": "John"}), Entity("2", {"name": "Jane"})]
        self.preprocessor.preprocess.side_effect = lambda e: e
        self.blocker.create_blocks.return_value = {"block1": entities}

        self.resolver.train(entities)

        self.preprocessor.preprocess.assert_called()
        self.model_builder.train.assert_called_once()
        self.blocker.create_blocks.assert_called_once()
        self.assertEqual(len(self.resolver.preprocessed_entities), 2)
        self.assertEqual(self.resolver.blocks, {"block1": {"1", "2"}})

    def test_resolve(self):
        entities = [Entity("1", {"name": "John"})]
        self.resolver.model = Mock()  # Simulate a trained model
        self.preprocessor.preprocess.side_effect = lambda e: e
        self.blocker.create_blocks.return_value = {"block1": entities}
        self.matcher.match.return_value = [(Entity("2", {"name": "Jane"}), 0.8)]

        results = self.resolver.resolve(entities)

        self.preprocessor.preprocess.assert_called()
        self.blocker.create_blocks.assert_called_once()
        self.matcher.match.assert_called_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].id, "1")
        self.assertEqual(results[0][1][0][0].id, "2")
        self.assertEqual(results[0][1][0][1], 0.8)

    def test_resolve_no_model(self):
        with self.assertRaises(ValueError):
            self.resolver.resolve([Entity("1", {"name": "John"})])

    def test_update_model(self):
        initial_entities = {Entity("1", {"name": "John"})}
        new_entities = {Entity("2", {"name": "Jane"})}
        self.preprocessor.preprocess.side_effect = lambda e: e
        self.blocker.create_blocks.side_effect = [{"block1": initial_entities}, {"block1": new_entities}]
        self.resolver.train(initial_entities)
        self.resolver.update_model(new_entities)

        self.model_builder.update.assert_called_once()
        self.assertEqual(len(self.resolver.preprocessed_entities), 2)
        self.assertEqual(len(self.resolver.blocks["block1"]), 2)
        self.assertIsInstance(self.resolver.blocks["block1"], set)

    def test_bulk_resolve(self):
        entities = [Entity(str(i), {"name": f"Entity{i}"}) for i in range(10)]
        self.resolver.model = Mock()  # Simulate a trained model

        # Mock the preprocessor to return an Entity with the same ID
        def preprocess_side_effect(e):
            return Entity(e.id, {"name": f"Preprocessed{e.attributes['name']}"})

        self.preprocessor.preprocess.side_effect = preprocess_side_effect

        # Mock the blocker to return all entities in a single block
        self.blocker.create_blocks.return_value = {"block1": entities}

        # Mock the matcher to return a constant match for all entities
        self.matcher.match.return_value = [(Entity("match", {"name": "Match"}), 0.8)]

        # Train the resolver with all entities
        self.resolver.train(entities)

        # Mock the resolve method to return one result per entity
        def mock_resolve(batch, top_k):
            return [(entity, self.matcher.match.return_value) for entity in batch]

        with patch.object(self.resolver, "resolve", side_effect=mock_resolve) as mock_resolve:
            results = self.resolver.bulk_resolve(entities[5:], batch_size=3)

        self.assertEqual(len(results), 5)  # We're resolving 5 entities (entities[5:])
        self.assertEqual(mock_resolve.call_count, 2)  # 1 full batch of 3 + 1 partial batch of 2

        # Verify that each result has the expected structure
        for entity, matches in results:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0][0].id, "match")
            self.assertEqual(matches[0][1], 0.8)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("pickle.dump")
    def test_save_model(self, mock_pickle_dump, mock_open):
        self.resolver.model = Mock()
        self.resolver.preprocessed_entities = {"1": Entity("1", {"name": "John"})}
        self.resolver.blocks = {"block1": set(["1"])}

        self.resolver.save_model("model.pkl")

        mock_open.assert_called_once_with("model.pkl", "wb")
        mock_pickle_dump.assert_called_once()

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("pickle.load")
    def test_load_model(self, mock_pickle_load, mock_open):
        mock_data = {
            "model": Mock(),
            "preprocessed_entities": {"1": Entity("1", {"name": "John"})},
            "blocks": {"block1": set(["1"])},
        }
        mock_pickle_load.return_value = mock_data

        self.resolver.load_model("model.pkl")

        mock_open.assert_called_once_with("model.pkl", "rb")
        mock_pickle_load.assert_called_once()
        self.assertEqual(self.resolver.model, mock_data["model"])
        self.assertEqual(self.resolver.preprocessed_entities, mock_data["preprocessed_entities"])
        self.assertEqual(self.resolver.blocks, mock_data["blocks"])

    def test_get_stats(self):
        self.resolver.preprocessed_entities = {"1": Entity("1", {"name": "John"}), "2": Entity("2", {"name": "Jane"})}
        self.resolver.blocks = {"block1": set(["1", "2"])}
        self.model_builder.get_model_size = Mock(return_value=1000)

        stats = self.resolver.get_stats()

        self.assertEqual(stats["num_entities"], 2)
        self.assertEqual(stats["num_blocks"], 1)
        self.assertEqual(stats["avg_block_size"], 2)
        self.assertEqual(stats["model_size"], 1000)


if __name__ == "__main__":
    unittest.main()

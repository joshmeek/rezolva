import unittest
from typing import List, Tuple

from rezolva.core.base import (Blocker, DataLoader, DataSaver, Entity, Matcher,
                               ModelBuilder, Preprocessor)


class TestEntity(unittest.TestCase):
    def test_entity_creation(self):
        entity = Entity("1", {"name": "John", "age": 30})
        self.assertEqual(entity.id, "1")
        self.assertEqual(entity.attributes, {"name": "John", "age": 30})


class TestAbstractClasses(unittest.TestCase):
    def test_abstract_methods(self):
        abstract_classes = [Preprocessor, ModelBuilder, Matcher, Blocker, DataLoader, DataSaver]
        for cls in abstract_classes:
            with self.assertRaises(TypeError):
                cls()

    def test_matcher_abstract_methods(self):
        class IncompleteMatcher(Matcher):
            pass

        with self.assertRaises(TypeError):
            IncompleteMatcher()

        class CompleteMatcher(Matcher):
            def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
                return []

        # This should not raise an error
        CompleteMatcher()

    def test_matcher_clustering(self):
        class TestMatcher(Matcher):
            def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
                return [(c, 0.5) for c in candidates]

        matcher = TestMatcher()
        entity = Entity("1", {"name": "John"})
        candidates = [Entity("2", {"name": "Jane"}), Entity("3", {"name": "Bob"})]

        # Test without clustering
        result = matcher.match(entity, candidates)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)  # Two matches

        # Test with clustering (mock clustering algorithm)
        class MockClusteringAlgorithm:
            def cluster(self, matches):
                return [matches[:1], matches[1:]]

        matcher_with_clustering = TestMatcher(clustering_algorithm=MockClusteringAlgorithm())
        result = matcher_with_clustering.apply_clustering(matcher_with_clustering.match(entity, candidates))
        self.assertEqual(len(result), 2)  # Two clusters
        self.assertEqual(len(result[0]), 1)  # One match in first cluster
        self.assertEqual(len(result[1]), 1)  # One match in second cluster


if __name__ == "__main__":
    unittest.main()

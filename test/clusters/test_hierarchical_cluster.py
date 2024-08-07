import unittest
from typing import List, Tuple

from rezolva.clusters import HierarchicalCluster
from rezolva.core.base import Entity


class TestHierarchicalCluster(unittest.TestCase):
    def setUp(self):
        self.threshold = 0.5
        self.clustering = HierarchicalCluster(self.threshold)

    def test_initialization(self):
        self.assertEqual(self.clustering.threshold, 0.5)

    def test_cluster_single_entity(self):
        matches = [(Entity("1", {"name": "John"}), 0.9)]
        result = self.clustering.cluster(matches)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], matches)

    def test_cluster_two_close_entities(self):
        matches = [(Entity("1", {"name": "John"}), 0.9), (Entity("2", {"name": "Jon"}), 0.8)]
        result = self.clustering.cluster(matches)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(result[0][0], matches[0])  # Higher score should be first

    def test_cluster_two_distant_entities(self):
        matches = [(Entity("1", {"name": "John"}), 0.9), (Entity("2", {"name": "Alice"}), 0.8)]
        clustering = HierarchicalCluster(0.01)  # Very low threshold
        result = clustering.cluster(matches)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(len(result[1]), 1)

    def test_cluster_multiple_entities(self):
        matches = [
            (Entity("1", {"name": "John"}), 0.9),
            (Entity("2", {"name": "Jon"}), 0.85),
            (Entity("3", {"name": "Jane"}), 0.8),
            (Entity("4", {"name": "Alice"}), 0.75),
        ]
        result = self.clustering.cluster(matches)

        # Check that we have at least one cluster
        self.assertGreater(len(result), 0)

        # Check that all entities are present in the result
        all_entities = [entity for cluster in result for entity, _ in cluster]
        self.assertEqual(len(all_entities), len(matches))

        # Check that entities are sorted by score within each cluster
        for cluster in result:
            scores = [score for _, score in cluster]
            self.assertEqual(scores, sorted(scores, reverse=True))

        # Assert on the structure of the first cluster
        self.assertGreaterEqual(len(result[0]), 2)  # At least two entities should be clustered together
        self.assertEqual(result[0][0][1], 0.9)  # Highest score should be first
        self.assertEqual(result[0][-1][1], 0.75)  # Lowest score should be last

    def test_cluster_sorting(self):
        matches = [
            (Entity("1", {"name": "John"}), 0.8),
            (Entity("2", {"name": "Jon"}), 0.9),
            (Entity("3", {"name": "Jane"}), 0.7),
        ]
        result = self.clustering.cluster(matches)
        self.assertEqual(result[0][0][1], 0.9)  # Highest score should be first
        self.assertEqual(result[0][-1][1], 0.7)  # Lowest score should be last

    def test_calculate_cluster_distance(self):
        cluster1 = [(Entity("1", {"name": "John"}), 0.9), (Entity("2", {"name": "Jon"}), 0.8)]
        cluster2 = [(Entity("3", {"name": "Jane"}), 0.7)]
        distance = self.clustering._calculate_cluster_distance(cluster1, cluster2)
        self.assertAlmostEqual(distance, 0.1)  # 1 - 0.9 = 0.1

    def test_empty_input(self):
        result = self.clustering.cluster([])
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()

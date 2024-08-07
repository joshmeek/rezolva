from typing import List, Tuple

from ..core.base import ClusteringAlgorithm, Entity


class HierarchicalCluster(ClusteringAlgorithm):
    """
    Hierarchical clustering algorithm for entity resolution.

    This class implements a bottom-up (agglomerative) hierarchical clustering
    algorithm. It starts with each entity in its own cluster and iteratively
    merges the closest clusters until a distance threshold is reached.

    :param threshold: The maximum distance between clusters to allow merging
    """

    def __init__(self, threshold: float):
        self.threshold = threshold

    def cluster(self, matches: List[Tuple[Entity, float]]) -> List[List[Tuple[Entity, float]]]:
        clusters = [[m] for m in matches]

        while len(clusters) > 1:
            min_dist = float("inf")
            min_pair = None

            for i, cluster1 in enumerate(clusters):
                for j, cluster2 in enumerate(clusters[i + 1 :], i + 1):
                    dist = self._calculate_cluster_distance(cluster1, cluster2)
                    if dist < min_dist:
                        min_dist = dist
                        min_pair = (i, j)

            if min_dist > self.threshold:
                break

            i, j = min_pair
            clusters[i].extend(clusters[j])
            clusters.pop(j)

        return [sorted(cluster, key=lambda x: x[1], reverse=True) for cluster in clusters]

    def _calculate_cluster_distance(
        self, cluster1: List[Tuple[Entity, float]], cluster2: List[Tuple[Entity, float]]
    ) -> float:
        return min(1 - score1 for _, score1 in cluster1 for _, score2 in cluster2)

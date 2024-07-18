from typing import List, Callable, Any, Dict
from .data_structures import Entity, Cluster, Comparison, MatchResult, Block
from .base_classes import Preprocessor, Blocker, SimilarityMeasure, Matcher

class EntityResolver:
    def __init__(self,
                 preprocessor: Preprocessor,
                 blocker: Blocker,
                 similarity_measure: SimilarityMeasure,
                 matcher: Matcher,
                 config: Dict[str, Any] = None):
        self.preprocessor = preprocessor
        self.blocker = blocker
        self.similarity_measure = similarity_measure
        self.matcher = matcher
        self.config = config or {}

    def resolve(self, entities: List[Entity]) -> List[Cluster]:
        preprocessed_entities = self.preprocessor.preprocess(entities)
        blocks = self.blocker.block(preprocessed_entities)
        comparisons = self._generate_comparisons(blocks)
        matches = self.matcher.match(comparisons)
        clusters = self._group_matches(matches, preprocessed_entities)
        return clusters

    def _generate_comparisons(self, blocks: List[Block]) -> List[Comparison]:
        comparisons = []
        for block in blocks:
            for i, entity1 in enumerate(block.entities):
                for entity2 in block.entities[i+1:]:
                    similarity = self.similarity_measure.compute(entity1, entity2)
                    comparisons.append(Comparison(entity1, entity2, similarity))
        return comparisons

    def _group_matches(self, matches: List[MatchResult], entities: List[Entity]) -> List[Cluster]:
        entity_to_cluster = {}
        clusters = []

        for match in matches:
            if match.is_match:
                entity1, entity2 = match.entity1, match.entity2
                cluster1 = entity_to_cluster.get(entity1)
                cluster2 = entity_to_cluster.get(entity2)

                if cluster1 is None and cluster2 is None:
                    new_cluster = Cluster({entity1, entity2})
                    clusters.append(new_cluster)
                    entity_to_cluster[entity1] = new_cluster
                    entity_to_cluster[entity2] = new_cluster
                elif cluster1 is None:
                    cluster2.add(entity1)
                    entity_to_cluster[entity1] = cluster2
                elif cluster2 is None:
                    cluster1.add(entity2)
                    entity_to_cluster[entity2] = cluster1
                elif cluster1 != cluster2:
                    # Merge clusters
                    cluster1.merge(cluster2)
                    clusters.remove(cluster2)
                    for entity in cluster2:
                        entity_to_cluster[entity] = cluster1

        # Add singleton clusters for unmatched entities
        for entity in entities:
            if entity not in entity_to_cluster:
                singleton_cluster = Cluster({entity})
                clusters.append(singleton_cluster)
                entity_to_cluster[entity] = singleton_cluster

        return clusters

    def add_custom_step(self, step_name: str, custom_function: Callable[[Any], Any]):
        setattr(self, step_name, custom_function)

    def run_custom_step(self, step_name: str, input_data: Any) -> Any:
        if hasattr(self, step_name):
            custom_function = getattr(self, step_name)
            return custom_function(input_data)
        else:
            raise AttributeError(f"Custom step '{step_name}' not found")
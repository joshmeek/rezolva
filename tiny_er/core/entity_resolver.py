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

    def resolve(self, entities: List[Entity]) -> List[Entity]:
        preprocessed_entities = self.preprocessor.preprocess(entities)
        blocks = self.blocker.block(preprocessed_entities)
        comparisons = self._generate_comparisons(blocks)
        matches = self.matcher.match(comparisons)
        clusters = self._group_matches(matches, preprocessed_entities)
        resolved_entities = self._consolidate_clusters(clusters)
        return resolved_entities

    def _generate_comparisons(self, blocks: List[Block]) -> List[Comparison]:
        comparisons = []
        for block in blocks:
            for i, entity1 in enumerate(block.entities):
                for entity2 in block.entities[i+1:]:
                    similarity = self.similarity_measure.compute(entity1, entity2)
                    comparisons.append(Comparison(entity1, entity2, similarity))
        return comparisons

    def _group_matches(self, matches: List[MatchResult], entities: List[Entity]) -> List[Cluster]:
        clusters = []
        entity_to_cluster = {}

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
                    cluster1.merge(cluster2)
                    clusters.remove(cluster2)
                    for entity in cluster2:
                        entity_to_cluster[entity] = cluster1

        # Add remaining unmatched entities as single-entity clusters
        for entity in entities:
            if entity not in entity_to_cluster:
                cluster = Cluster({entity})
                clusters.append(cluster)
                entity_to_cluster[entity] = cluster

        return clusters

    def _consolidate_clusters(self, clusters: List[Cluster]) -> List[Entity]:
        resolved_entities = []
        for cluster in clusters:
            if cluster.entities:
                resolved_entity = self._merge_entities(list(cluster.entities))
                resolved_entities.append(resolved_entity)
        return resolved_entities

    def _merge_entities(self, entities: List[Entity]) -> Entity:
        if not entities:
            return None
        
        merged_attributes = {}
        original_ids = []
        for entity in entities:
            original_ids.extend(entity.original_ids or [entity.id])
            for attr, value in entity.attributes.items():
                if attr not in merged_attributes:
                    merged_attributes[attr] = []
                merged_attributes[attr].append(value)
        
        # Resolve conflicts by choosing the most frequent value
        for attr, values in merged_attributes.items():
            merged_attributes[attr] = max(set(values), key=values.count)
        
        return Entity(id=f"resolved_{'_'.join(sorted(set(original_ids)))}", attributes=merged_attributes, original_ids=list(set(original_ids)))


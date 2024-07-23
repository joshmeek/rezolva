# start_er/matchers/bayesian_matcher.py

import math
from typing import Dict, List, Tuple

from ..core.base import Entity, Matcher


class BayesianMatcher(Matcher):
    def __init__(self, threshold: float = 0.5, attribute_weights: Dict[str, float] = None):
        self.threshold = threshold
        self.attribute_weights = attribute_weights or {}
        self.attribute_probabilities = {}

    def train(self, entities: List[Entity]):
        total_entities = len(entities)
        for attr in self.attribute_weights.keys():
            self.attribute_probabilities[attr] = {}
            value_counts = {}
            for entity in entities:
                value = entity.attributes.get(attr, '')
                value_counts[value] = value_counts.get(value, 0) + 1
            
            for value, count in value_counts.items():
                self.attribute_probabilities[attr][value] = count / total_entities

    def match(self, entity: Entity, model: Dict) -> List[Tuple[Entity, float]]:
        matches = []
        for candidate_id, candidate in model['entities'].items():
            if candidate_id != entity.id:
                similarity = self._calculate_similarity(entity, candidate)
                if similarity >= self.threshold:
                    matches.append((candidate, similarity))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_similarity(self, entity1: Entity, entity2: Entity) -> float:
        total_similarity = 0
        total_weight = sum(self.attribute_weights.values())

        for attr, weight in self.attribute_weights.items():
            value1 = entity1.attributes.get(attr, '')
            value2 = entity2.attributes.get(attr, '')
            
            if value1 == value2:
                prob = self.attribute_probabilities[attr].get(value1, 0.5)
                similarity = 1 - prob  # Rarer matches are more significant
            else:
                similarity = self._jaccard_similarity(value1, value2)
            
            total_similarity += similarity * (weight / total_weight)

        return total_similarity

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0
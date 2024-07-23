import math
from typing import Dict, List, Tuple

from ..core.base import Entity, Matcher


class BayesianMatcher(Matcher):
    def __init__(self, threshold: float = 0.5, attribute_weights: Dict[str, float] = None):
        self.threshold = threshold
        self.attribute_weights = attribute_weights or {}
        self.priors = {}
        self.likelihoods = {}

    def train(self, entities: List[Entity]):
        # Calculate priors and likelihoods based on training data
        total_entities = len(entities)
        for attr, weight in self.attribute_weights.items():
            self.priors[attr] = {}
            self.likelihoods[attr] = {}
            for entity in entities:
                value = entity.attributes.get(attr, '')
                self.priors[attr][value] = self.priors[attr].get(value, 0) + 1
                for other_entity in entities:
                    if other_entity.id != entity.id:
                        other_value = other_entity.attributes.get(attr, '')
                        if value == other_value:
                            self.likelihoods[attr][value] = self.likelihoods[attr].get(value, 0) + 1

            # Normalize priors and likelihoods
            for value in self.priors[attr]:
                self.priors[attr][value] /= total_entities
                self.likelihoods[attr][value] = self.likelihoods[attr].get(value, 0) / (self.priors[attr][value] * total_entities)

    def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
        matches = []
        for candidate in candidates:
            if candidate.id != entity.id:
                probability = self._calculate_match_probability(entity, candidate)
                if probability >= self.threshold:
                    matches.append((candidate, probability))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_match_probability(self, entity1: Entity, entity2: Entity) -> float:
        total_probability = 1.0
        for attr, weight in self.attribute_weights.items():
            value1 = entity1.attributes.get(attr, '')
            value2 = entity2.attributes.get(attr, '')
            prior = self.priors[attr].get(value1, 1e-10)  # Small non-zero value to avoid division by zero
            likelihood = self.likelihoods[attr].get(value1, 1e-10) if value1 == value2 else 1 - self.likelihoods[attr].get(value1, 1e-10)
            attr_probability = (likelihood * prior) / ((likelihood * prior) + ((1 - likelihood) * (1 - prior)))
            total_probability *= attr_probability ** weight
        return total_probability
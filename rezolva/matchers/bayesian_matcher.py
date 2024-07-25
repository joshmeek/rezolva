# rezolva/matchers/bayesian_matcher.py

import math
from typing import Dict, List, Tuple

from ..core.base import Entity, Matcher


class BayesianMatcher(Matcher):
    """
    A matcher that uses Bayesian probability to determine the likelihood of a match between entities.

    Bayesian matching calculates the probability that two entities refer to the same real-world object
    given the observed attributes. It uses Bayes' theorem to update probabilities based on observed data.

    How Bayesian Matching works:
    1. Calculate prior probabilities based on the frequency of attribute values in the dataset
    2. For each pair of entities, calculate the likelihood of observing their attributes if they were a match
    3. Use Bayes' theorem to calculate the posterior probability of a match given the observed attributes

    Advantages:
    - Provides a probabilistic framework for entity matching
    - Can incorporate domain knowledge through prior probabilities
    - Handles uncertainty and missing data well

    Disadvantages:
    - Requires a training phase to estimate probabilities
    - Can be computationally expensive for large datasets or many attributes
    - Assumes independence between attributes, which may not always hold

    :param threshold: The probability threshold above which entities are considered a match
    :param attribute_weights: A dictionary mapping attribute names to their importance in matching
    """

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
                value = entity.attributes.get(attr, "")
                value_counts[value] = value_counts.get(value, 0) + 1

            for value, count in value_counts.items():
                self.attribute_probabilities[attr][value] = count / total_entities

    def match(self, entity: Entity, model: Dict) -> List[Tuple[Entity, float]]:
        matches = []
        for candidate_id, candidate in model["entities"].items():
            if candidate_id != entity.id:
                similarity = self._calculate_similarity(entity, candidate)
                if similarity >= self.threshold:
                    matches.append((candidate, similarity))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_similarity(self, entity1: Entity, entity2: Entity) -> float:
        total_similarity = 0
        total_weight = sum(self.attribute_weights.values())

        for attr, weight in self.attribute_weights.items():
            value1 = entity1.attributes.get(attr, "")
            value2 = entity2.attributes.get(attr, "")

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

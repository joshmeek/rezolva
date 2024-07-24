from typing import Dict, List, Tuple

from ..core.base import Entity, Matcher


class BaseAttributeMatcher(Matcher):
    """
    A base class for attribute-based matchers.

    This class provides a foundation for matchers that compare entities based on their attributes.
    It implements a basic matching algorithm and allows for attribute weighting.

    :param threshold: The similarity threshold above which entities are considered a match
    :param attribute_weights: A dictionary mapping attribute names to their importance in matching
    """

    def __init__(self, threshold: float = 0.7, attribute_weights: Dict[str, float] = None):
        self.threshold = threshold
        self.attribute_weights = attribute_weights or {}

    def match(self, entity: Entity, model: dict) -> List[Tuple[Entity, float]]:
        matches = []
        for candidate in model["entities"].values():
            if candidate.id != entity.id:
                similarity = self._calculate_weighted_similarity(entity, candidate)
                if similarity >= self.threshold:
                    matches.append((candidate, similarity))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_weighted_similarity(self, entity1: Entity, entity2: Entity) -> float:
        similarities = []
        weights = []
        for attr, weight in self.attribute_weights.items():
            val1 = str(entity1.attributes.get(attr, ""))
            val2 = str(entity2.attributes.get(attr, ""))
            similarity = self._calculate_attribute_similarity(val1, val2)
            similarities.append(similarity)
            weights.append(weight)

        if not similarities:
            return 0.0

        return sum(s * w for s, w in zip(similarities, weights)) / sum(weights)

    def _calculate_attribute_similarity(self, val1: str, val2: str) -> float:
        raise NotImplementedError("Subclasses must implement this method")

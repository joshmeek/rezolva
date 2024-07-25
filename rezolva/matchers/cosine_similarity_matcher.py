import math
from typing import Dict, List, Tuple, Union

from ..core.base import Entity
from .base_matcher import BaseAttributeMatcher


class CosineSimilarityMatcher(BaseAttributeMatcher):
    """
    A matcher that uses cosine similarity to compare entities.

    Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space.
    In the context of entity matching, these vectors represent the attributes of entities.

    How Cosine Similarity works:
    1. Convert entity attributes into numerical vectors (usually using TF-IDF weighting for text)
    2. Compute the dot product of the two vectors
    3. Divide the dot product by the product of the magnitudes of the two vectors

    Advantages:
    - Invariant to scaling, so it can handle attributes with different magnitudes well
    - Works well for sparse vectors, making it suitable for text-heavy attributes
    - Captures the similarity of direction rather than magnitude

    Disadvantages:
    - Doesn't consider the magnitude of attributes, which might be important in some cases
    - Can be computationally expensive for high-dimensional data

    :param threshold: The similarity threshold above which entities are considered a match
    :param attribute_weights: A dictionary mapping attribute names to their importance in matching
    """

    def __init__(self, threshold: float = 0.5, attribute_weights: Dict[str, float] = None):
        super().__init__(threshold, attribute_weights)

    def match(self, entity: Entity, model: dict) -> List[Tuple[Entity, float]]:
        matches = []
        if "vectors" in model:  # Vector-based approach
            entity_vector = model["vectors"].get(entity.id)
            if entity_vector is None:
                entity_vector = self._vectorize_entity(entity, model)

            for candidate_id, candidate_vector in model["vectors"].items():
                if candidate_id != entity.id:
                    similarity = self._cosine_similarity_vectors(entity_vector, candidate_vector)
                    if similarity >= self.threshold:
                        matches.append((model["entities"][candidate_id], similarity))
        else:  # String-based approach
            for candidate_id, candidate in model["entities"].items():
                if candidate_id != entity.id:
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
        return self._cosine_similarity(val1, val2)

    def _cosine_similarity(self, s1: str, s2: str) -> float:
        words1 = s1.lower().split()
        words2 = s2.lower().split()
        unique_words = set(words1 + words2)
        vec1 = [words1.count(word) for word in unique_words]
        vec2 = [words2.count(word) for word in unique_words]
        return self._cosine_similarity_vectors(
            {word: count for word, count in zip(unique_words, vec1)},
            {word: count for word, count in zip(unique_words, vec2)},
        )

    def _cosine_similarity_vectors(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        dot_product = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        magnitude1 = math.sqrt(sum1)
        magnitude2 = math.sqrt(sum2)

        if magnitude1 * magnitude2 == 0:
            return 0
        return dot_product / (magnitude1 * magnitude2)

    def _vectorize_entity(self, entity: Entity, model: dict) -> Dict[str, float]:
        vector = {}
        term_freq = {}
        for attr, value in entity.attributes.items():
            terms = str(value).lower().split()
            for term in terms:
                term_freq[term] = term_freq.get(term, 0) + 1

        for term, freq in term_freq.items():
            tf = freq / sum(term_freq.values())
            idf = model.get("idf", {}).get(term, math.log(len(model["entities"]) + 1))  # Use default IDF for new terms
            vector[term] = tf * idf

        return vector

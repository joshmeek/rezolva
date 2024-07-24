import hashlib
from typing import Dict, List, Tuple

from ..core.base import Entity, Matcher


class MinHashMatcher(Matcher):
    """
    A matcher that uses MinHash and Locality-Sensitive Hashing (LSH) for efficient similarity estimation.

    MinHash is a technique for quickly estimating how similar two sets are. It works by selecting a
    random sample of elements from each set in a way that makes it easy to estimate the Jaccard similarity.

    How MinHash Matching works:
    1. Convert each entity's attributes into a set of features (e.g., words or n-grams)
    2. Apply multiple hash functions to each feature set to create MinHash signatures
    3. Compare MinHash signatures to estimate Jaccard similarity

    Advantages:
    - Efficient for large datasets
    - Can handle high-dimensional data well
    - Provides a good approximation of Jaccard similarity with less computation

    Disadvantages:
    - Provides an estimate, not an exact similarity
    - Requires tuning of parameters (number of hash functions, threshold)

    :param threshold: The similarity threshold above which entities are considered a match
    :param num_hash_functions: The number of hash functions to use for MinHash
    :param attribute_weights: A dictionary mapping attribute names to their importance in matching
    """

    def __init__(
        self, threshold: float = 0.5, num_hash_functions: int = 100, attribute_weights: Dict[str, float] = None
    ):
        self.threshold = threshold
        self.num_hash_functions = num_hash_functions
        self.attribute_weights = attribute_weights or {}
        self.hash_functions = self._generate_hash_functions()

    def _generate_hash_functions(self):
        return [
            lambda x, i=i: int(hashlib.md5(f"{x}{i}".encode()).hexdigest(), 16) % (2**32 - 1)
            for i in range(self.num_hash_functions)
        ]

    def _minhash_signature(self, text: str) -> List[int]:
        words = set(text.lower().split())
        signature = [min(h(word) for word in words) for h in self.hash_functions]
        return signature

    def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
        matches = []
        entity_signatures = {
            attr: self._minhash_signature(str(entity.attributes.get(attr, ""))) for attr in self.attribute_weights
        }

        for candidate in candidates:
            if candidate.id != entity.id:
                similarity = self._calculate_weighted_similarity(entity_signatures, candidate)
                if similarity >= self.threshold:
                    matches.append((candidate, similarity))

        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_weighted_similarity(self, entity_signatures: Dict[str, List[int]], candidate: Entity) -> float:
        similarities = []
        weights = []

        for attr, weight in self.attribute_weights.items():
            candidate_signature = self._minhash_signature(str(candidate.attributes.get(attr, "")))
            similarity = (
                sum(a == b for a, b in zip(entity_signatures[attr], candidate_signature)) / self.num_hash_functions
            )
            similarities.append(similarity)
            weights.append(weight)

        return sum(s * w for s, w in zip(similarities, weights)) / sum(weights)

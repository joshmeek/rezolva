from .base_matcher import BaseAttributeMatcher
import math

class CosineSimilarityMatcher(BaseAttributeMatcher):
    def _calculate_attribute_similarity(self, val1: str, val2: str) -> float:
        return self._cosine_similarity(val1, val2)

    def _cosine_similarity(self, s1: str, s2: str) -> float:
        words1 = s1.lower().split()
        words2 = s2.lower().split()
        unique_words = set(words1 + words2)
        vec1 = [words1.count(word) for word in unique_words]
        vec2 = [words2.count(word) for word in unique_words]
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2))
        if magnitude1 * magnitude2 == 0:
            return 0
        return dot_product / (magnitude1 * magnitude2)
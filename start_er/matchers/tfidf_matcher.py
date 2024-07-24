
import math
from typing import Dict, List

from ..core.base import Entity
from .base_matcher import BaseAttributeMatcher


class TfIdfMatcher(BaseAttributeMatcher):
    def __init__(self, threshold: float = 0.3, attribute_weights: Dict[str, float] = None):
        super().__init__(threshold, attribute_weights)
        self.idf = {}
        self.doc_count = 0

    def train(self, entities: List[Entity]):
        self.doc_count = len(entities)
        word_doc_count = {}
        for entity in entities:
            words = set()
            for attr in self.attribute_weights.keys():
                words.update(str(entity.attributes.get(attr, '')).lower().split())
            for word in words:
                word_doc_count[word] = word_doc_count.get(word, 0) + 1
        self.idf = {word: math.log(self.doc_count / count) for word, count in word_doc_count.items()}

    def _calculate_attribute_similarity(self, val1: str, val2: str) -> float:
        if not self.idf:
            raise ValueError("TfIdfMatcher needs to be trained first. Call train() with your entities.")
        tfidf1 = self._calculate_tfidf(val1)
        tfidf2 = self._calculate_tfidf(val2)
        return self._cosine_similarity(tfidf1, tfidf2)

    def _calculate_tfidf(self, text: str) -> dict:
        words = text.lower().split()
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        max_count = max(word_count.values()) if word_count else 1
        return {word: (count / max_count) * self.idf.get(word, 0) for word, count in word_count.items()}

    def _cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        dot_product = sum(vec1[x] * vec2[x] for x in intersection)
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        if magnitude1 * magnitude2 == 0:
            return 0
        return dot_product / (magnitude1 * magnitude2)
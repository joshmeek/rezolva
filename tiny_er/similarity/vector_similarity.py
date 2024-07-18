from typing import Dict, Any, List
from ..core.data_structures import Entity
import math
from ..core.base_classes import SimilarityMeasure
from collections import Counter

class CosineSimilarity(SimilarityMeasure):
    def __init__(self, config: Dict[str, Any]):
        self.fields = config.get('fields', [])

    def compute(self, entity1: Entity, entity2: Entity) -> float:
        vectors = []
        for field in self.fields:
            vec1 = self._create_vector(entity1.attributes.get(field, ''))
            vec2 = self._create_vector(entity2.attributes.get(field, ''))
            vectors.append((vec1, vec2))
        
        similarities = [self._cosine_similarity(v1, v2) for v1, v2 in vectors]
        overall_similarity = sum(similarities) / len(similarities)
        return overall_similarity

    def _create_vector(self, value: Any) -> Dict[str, int]:
        if isinstance(value, (int, float)):
            return {str(value): 1}
        elif isinstance(value, str):
            return Counter(value.lower().split())
        else:
            return Counter()

    def _cosine_similarity(self, vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        dot_product = sum(vec1[x] * vec2[x] for x in intersection)

        sum1 = sum(vec1[x]**2 for x in vec1.keys())
        sum2 = sum(vec2[x]**2 for x in vec2.keys())
        
        magnitude = math.sqrt(sum1) * math.sqrt(sum2)
        
        if not magnitude:
            return 0.0
        
        similarity = dot_product / magnitude
        return similarity

class EuclideanDistance(SimilarityMeasure):
    def __init__(self, config: Dict[str, Any]):
        self.fields = config.get('fields', [])

    def compute(self, entity1: Entity, entity2: Entity) -> float:
        vec1 = self._create_vector(entity1)
        vec2 = self._create_vector(entity2)
        return self._euclidean_distance(vec1, vec2)

    def _create_vector(self, entity: Entity) -> List[float]:
        return [float(entity.attributes.get(field, 0)) for field in self.fields]

    def _euclidean_distance(self, vec1: List[float], vec2: List[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))

def create_vector_similarity_measure(config: Dict[str, Any]):
    method = config.get('method', 'cosine')
    if method == 'cosine':
        return CosineSimilarity(config)
    elif method == 'euclidean':
        return EuclideanDistance(config)
    else:
        raise ValueError(f"Unsupported vector similarity method: {method}")
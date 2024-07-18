from typing import Dict, Any
from ..core.data_structures import Entity
from ..core.base_classes import SimilarityMeasure

class JaccardSimilarity(SimilarityMeasure):
    def __init__(self, config: Dict[str, Any]):
        self.threshold = config.get('threshold', 0.5)
        self.fields = config.get('fields', None)

    def compute(self, entity1: Entity, entity2: Entity) -> float:
        set1 = set(self._tokenize(entity1))
        set2 = set(self._tokenize(entity2))
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0

    def _tokenize(self, entity: Entity) -> list:
        if self.fields:
            return ' '.join(str(entity.attributes.get(f, '')).lower() for f in self.fields).split()
        return ' '.join(str(v).lower() for v in entity.attributes.values()).split()

class LevenshteinSimilarity(SimilarityMeasure):
    def __init__(self, config: Dict[str, Any]):
        self.threshold = config.get('threshold', 0.7)

    def compute(self, entity1: Entity, entity2: Entity) -> float:
        str1 = ' '.join(str(v) for v in entity1.attributes.values())
        str2 = ' '.join(str(v) for v in entity2.attributes.values())
        
        distance = self._levenshtein_distance(str1, str2)
        max_length = max(len(str1), len(str2))
        
        return 1 - (distance / max_length)

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

def create_similarity_measure(config: Dict[str, Any]):
    method = config.get('method', 'jaccard')
    if method == 'jaccard':
        return JaccardSimilarity(config)
    elif method == 'levenshtein':
        return LevenshteinSimilarity(config)
    else:
        raise ValueError(f"Unsupported similarity method: {method}")
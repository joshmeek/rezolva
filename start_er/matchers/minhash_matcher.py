import hashlib
from typing import Dict, List, Tuple

from ..core.base import Entity, Matcher


class MinHashMatcher(Matcher):
    def __init__(self, threshold: float = 0.5, num_hash_functions: int = 100, attribute_weights: Dict[str, float] = None):
        self.threshold = threshold
        self.num_hash_functions = num_hash_functions
        self.attribute_weights = attribute_weights or {}
        self.hash_functions = self._generate_hash_functions()

    def _generate_hash_functions(self):
        return [lambda x, i=i: int(hashlib.md5(f"{x}{i}".encode()).hexdigest(), 16) % (2**32 - 1)
                for i in range(self.num_hash_functions)]

    def _minhash_signature(self, text: str) -> List[int]:
        words = set(text.lower().split())
        signature = [min(h(word) for word in words) for h in self.hash_functions]
        return signature

    def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
        matches = []
        entity_signatures = {attr: self._minhash_signature(str(entity.attributes.get(attr, ''))) 
                             for attr in self.attribute_weights}
        
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
            candidate_signature = self._minhash_signature(str(candidate.attributes.get(attr, '')))
            similarity = sum(a == b for a, b in zip(entity_signatures[attr], candidate_signature)) / self.num_hash_functions
            similarities.append(similarity)
            weights.append(weight)
        
        return sum(s * w for s, w in zip(similarities, weights)) / sum(weights)
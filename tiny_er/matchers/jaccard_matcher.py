from ..core.base import Matcher, Entity
from typing import List, Tuple

class JaccardMatcher(Matcher):
    def __init__(self, threshold: float = 0.3):
        self.threshold = threshold

    def match(self, entity: Entity, model: dict) -> List[Tuple[Entity, float]]:
        candidate_ids = set()
        for attr in model['index']:
            value = entity.attributes.get(attr, '').lower()
            if value in model['index'][attr]:
                candidate_ids.update(model['index'][attr][value])
        
        matches = []
        for candidate_id in candidate_ids:
            if candidate_id != entity.id:
                candidate = model['entities'][candidate_id]
                similarity = self._calculate_similarity(entity, candidate)
                if similarity >= self.threshold:
                    matches.append((candidate, similarity))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_similarity(self, entity1: Entity, entity2: Entity) -> float:
        set1 = set(str(v).lower() for v in entity1.attributes.values())
        set2 = set(str(v).lower() for v in entity2.attributes.values())
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
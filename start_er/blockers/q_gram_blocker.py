from typing import List, Dict, Callable
from collections import defaultdict
from ..core.base import Blocker, Entity

class QGramBlocker(Blocker):
    def __init__(self, q: int, key_func: Callable[[Entity], str], threshold: int):
        self.q = q
        self.key_func = key_func or default_key_func
        self.threshold = threshold

    def create_blocks(self, entities: List[Entity]) -> Dict[str, List[Entity]]:
        blocks = defaultdict(list)
        for entity in entities:
            key = self.key_func(entity)
            q_grams = self._generate_q_grams(key)
            for q_gram in q_grams:
                blocks[q_gram].append(entity)

        # Merge blocks that have more than threshold common entities
        merged_blocks = defaultdict(set)
        for q_gram, entities in blocks.items():
            if len(entities) >= self.threshold:
                merged_blocks[q_gram].update(entities)

        return {k: list(v) for k, v in merged_blocks.items()}

    def _generate_q_grams(self, string: str) -> List[str]:
        string = ' ' * (self.q - 1) + string + ' ' * (self.q - 1)
        return [string[i:i+self.q] for i in range(len(string) - self.q + 1)]

def default_key_func(entity: Entity) -> str:
    # Example key function: concatenate all attribute values
    return ' '.join(str(value) for value in entity.attributes.values())
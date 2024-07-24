from typing import List, Dict, Callable
from collections import defaultdict
from ..core.base import Blocker, Entity

class SuffixArrayBlocker(Blocker):
    def __init__(self, key_func: Callable[[Entity], str], min_suffix_length: int):
        self.key_func = key_func or default_key_func
        self.min_suffix_length = min_suffix_length

    def create_blocks(self, entities: List[Entity]) -> Dict[str, List[Entity]]:
        blocks = defaultdict(list)
        suffix_array = self._build_suffix_array(entities)

        for suffix, entity_indices in suffix_array.items():
            if len(suffix) >= self.min_suffix_length:
                for index in entity_indices:
                    blocks[suffix].append(entities[index])

        return dict(blocks)

    def _build_suffix_array(self, entities: List[Entity]) -> Dict[str, List[int]]:
        suffix_array = defaultdict(list)
        for i, entity in enumerate(entities):
            key = self.key_func(entity)
            for j in range(len(key)):
                suffix = key[j:]
                suffix_array[suffix].append(i)
        return suffix_array

def default_key_func(entity: Entity) -> str:
    # Example key function: concatenate all attribute values
    return ' '.join(str(value) for value in entity.attributes.values()).lower()
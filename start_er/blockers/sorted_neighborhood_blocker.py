from typing import Callable, Dict, List

from ..core.base import Blocker, Entity


class SortedNeighborhoodBlocker(Blocker):
    def __init__(self, key_func: Callable[[Entity], str], window_size: int):
        self.key_func = key_func or default_key_func
        self.window_size = window_size

    def create_blocks(self, entities: List[Entity]) -> Dict[str, List[Entity]]:
        # Sort entities based on the key function
        sorted_entities = sorted(entities, key=self.key_func)

        blocks = {}
        for i in range(len(sorted_entities)):
            start = max(0, i - self.window_size // 2)
            end = min(len(sorted_entities), i + self.window_size // 2 + 1)
            window = sorted_entities[start:end]
            
            key = self.key_func(sorted_entities[i])
            if key not in blocks:
                blocks[key] = []
            blocks[key].extend(window)

        # Remove duplicates from blocks
        for key in blocks:
            blocks[key] = list(set(blocks[key]))

        return blocks

def default_key_func(entity: Entity) -> str:
    # Example key function: concatenate first characters of each attribute
    return ''.join(str(value)[0].lower() for value in entity.attributes.values())
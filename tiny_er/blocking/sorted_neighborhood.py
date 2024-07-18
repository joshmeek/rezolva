from typing import List, Dict, Any
from ..core.data_structures import Entity, Block
from ..core.base_classes import Blocker

class SortedNeighborhoodBlocker(Blocker):
    def __init__(self, config: Dict[str, Any]):
        self.window_size = config.get('window_size', 3)
        self.key_function = config.get('key_function', lambda e: e.attributes.get('name', ''))

    def block(self, entities: List[Entity]) -> List[Block]:
        sorted_entities = sorted(entities, key=self.key_function)
        blocks = []

        for i in range(len(sorted_entities) - self.window_size + 1):
            window = sorted_entities[i:i + self.window_size]
            block = Block(f"block_{i}")
            for entity in window:
                block.add(entity)
            blocks.append(block)

        return blocks

def create_sorted_neighborhood_blocker(config: Dict[str, Any]) -> SortedNeighborhoodBlocker:
    return SortedNeighborhoodBlocker(config)
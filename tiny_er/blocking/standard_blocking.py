from typing import List, Dict, Any
from ..core.data_structures import Entity, Block
from ..core.base_classes import Blocker

class StandardBlocker(Blocker):
    def __init__(self, config: Dict[str, Any]):
        self.block_key = config.get('block_key', 'name')

    def block(self, entities: List[Entity]) -> List[Block]:
        blocks = {}
        for entity in entities:
            key = self._get_block_key(entity)
            if key not in blocks:
                blocks[key] = Block(key)
            blocks[key].add(entity)
        
        return list(blocks.values())

    def _get_block_key(self, entity: Entity) -> str:
        value = entity.attributes.get(self.block_key, '')
        if isinstance(value, str):
            return value[:1].lower()  # Use first character of the blocking key
        return str(value)

def create_blocker(config: Dict[str, Any]) -> StandardBlocker:
    return StandardBlocker(config)
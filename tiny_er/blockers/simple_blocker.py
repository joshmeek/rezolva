from typing import Callable, Dict, List

from ..core.base import Blocker, Entity


class SimpleBlocker(Blocker):
    def __init__(self, blocking_key: Callable[[Entity], str]):
        self.blocking_key = blocking_key

    def create_blocks(self, entities: List[Entity]) -> Dict[str, List[Entity]]:
        blocks = {}
        for entity in entities:
            key = self.blocking_key(entity)
            if key not in blocks:
                blocks[key] = []
            blocks[key].append(entity)
        return blocks
import random
from typing import Dict, List, Tuple

from ..core.base import Blocker, Entity


class CanopyBlocker(Blocker):
    def __init__(self, distance_func, t1: float, t2: float):
        self.distance_func = distance_func or euclidean_distance
        self.t1 = t1
        self.t2 = t2

    def create_blocks(self, entities: List[Entity]) -> Dict[int, List[Entity]]:
        canopies = []
        remaining = set(entities)

        while remaining:
            center = random.choice(list(remaining))
            canopy = []
            to_remove = set()

            for entity in remaining:
                distance = self.distance_func(center, entity)
                if distance < self.t1:
                    canopy.append(entity)
                    if distance < self.t2:
                        to_remove.add(entity)

            canopies.append(canopy)
            remaining -= to_remove

        return {i: canopy for i, canopy in enumerate(canopies)}

def euclidean_distance(e1: Entity, e2: Entity) -> float:
    attrs = set(e1.attributes.keys()) & set(e2.attributes.keys())
    return sum((float(e1.attributes[attr]) - float(e2.attributes[attr])) ** 2 for attr in attrs) ** 0.5
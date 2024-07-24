import random
from typing import Dict, List, Tuple

from ..core.base import Blocker, Entity


class CanopyBlocker(Blocker):
    """
    A blocking method that uses canopy clustering to create blocks of entities.

    Canopy clustering is a technique used to create overlapping blocks (canopies) of entities
    based on a cheap, approximate distance measure. It's particularly useful when dealing with
    large datasets.

    How Canopy Clustering works:
    1. Start with all entities in a single set
    2. Randomly select an entity as a canopy center
    3. Add all entities within distance t1 of the center to the canopy
    4. Remove all entities within distance t2 (where t2 < t1) from the original set
    5. Repeat steps 2-4 until the original set is empty

    Advantages:
    - Can handle large datasets efficiently
    - Creates overlapping blocks, potentially increasing recall
    - Can use different distance measures for different attributes

    Disadvantages:
    - Results can vary due to random selection of canopy centers
    - Choosing appropriate t1 and t2 thresholds can be challenging

    :param distance_func: A function that calculates the distance between two entities
    :param t1: The loose distance threshold for creating canopies
    :param t2: The tight distance threshold for removing entities from consideration
    """

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

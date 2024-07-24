from typing import Callable, Dict, List

from ..core.base import Blocker, Entity


class SortedNeighborhoodBlocker(Blocker):
    """
    A blocking method that uses the sorted neighborhood approach to create blocks of entities.

    The Sorted Neighborhood method sorts entities based on a sorting key and then moves a window
    of fixed size over the sorted list to create blocks.

    How Sorted Neighborhood Blocking works:
    1. Apply a sorting key function to each entity
    2. Sort the entities based on this key
    3. Move a window of fixed size over the sorted list
    4. Entities within the same window form a block

    Advantages:
    - Can handle large datasets efficiently
    - Adjustable window size allows for trade-off between recall and efficiency
    - Effective when similar entities have similar sorting keys

    Disadvantages:
    - Sensitive to errors or variations at the beginning of the sorting key
    - Fixed window size may not be optimal for all parts of the sorted list

    :param key_func: A function that takes an Entity and returns a sortable key
    :param window_size: The size of the sliding window
    """

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
    return "".join(str(value)[0].lower() for value in entity.attributes.values())

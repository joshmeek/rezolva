from typing import Callable, Dict, List

from ..core.base import Blocker, Entity


class SimpleBlocker(Blocker):
    """
    A simple blocking method that creates blocks based on a user-defined blocking key function.

    The SimpleBlocker is a straightforward approach to grouping entities into blocks. It uses
    a user-defined function to generate a blocking key for each entity, and then groups entities
    with the same blocking key together.

    This method is flexible and can be adapted to various scenarios by changing the blocking
    key function. For example:
    - Grouping by the first letter of a name
    - Grouping by year in a date field
    - Grouping by category or any other attribute

    How SimpleBlocker works:
    1. Apply the blocking key function to each entity
    2. Group entities with the same blocking key together

    Advantages:
    - Simple to understand and implement
    - Flexible, can be adapted to different scenarios
    - Fast, as it only requires one pass through the data

    Disadvantages:
    - May miss matches if the blocking key is too specific
    - Can create imbalanced blocks if the blocking key is not well-chosen

    :param blocking_key: A function that takes an Entity and returns a blocking key
    """

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

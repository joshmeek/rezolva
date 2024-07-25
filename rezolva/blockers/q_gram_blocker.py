from collections import defaultdict
from typing import Callable, Dict, List

from ..core.base import Blocker, Entity


class QGramBlocker(Blocker):
    """
    A blocking method that uses Q-grams to create blocks of entities.

    Q-grams (also known as N-grams) are contiguous sequences of Q characters from a given string.
    This blocker creates blocks based on the Q-grams of a specified attribute of the entities.

    How QGramBlocker works:
    1. For each entity, generate Q-grams from the specified attribute
    2. For each Q-gram, add the entity to the corresponding block
    3. Merge blocks that have more than a threshold number of common entities

    Advantages:
    - Robust to minor spelling variations and typos
    - Can capture similarity even with small attribute values
    - Adjustable precision by changing the Q value

    Disadvantages:
    - Can create many small blocks for large Q values
    - May create large blocks for small Q values, reducing efficiency

    :param q: The length of the Q-grams
    :param key_func: A function that takes an Entity and returns the value to generate Q-grams from
    :param threshold: The minimum number of entities required to form a block
    """

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
        string = " " * (self.q - 1) + string + " " * (self.q - 1)
        return [string[i : i + self.q] for i in range(len(string) - self.q + 1)]


def default_key_func(entity: Entity) -> str:
    # Example key function: concatenate all attribute values
    return " ".join(str(value) for value in entity.attributes.values())

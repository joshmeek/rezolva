from collections import defaultdict
from typing import Callable, Dict, List

from ..core.base import Blocker, Entity


class SuffixArrayBlocker(Blocker):
    """
    A blocking method that uses suffix arrays to create blocks of entities.

    Suffix arrays are efficient data structures for string processing tasks. This blocker
    creates blocks based on common suffixes of a specified attribute of the entities.

    How SuffixArrayBlocker works:
    1. For each entity, generate all suffixes of the specified attribute
    2. Create a suffix array by sorting these suffixes
    3. Group entities that share suffixes longer than a minimum length

    Advantages:
    - Efficient for string-based blocking
    - Can capture similarities even when differences occur at the beginning of strings
    - Adjustable minimum suffix length allows for trade-off between recall and efficiency

    Disadvantages:
    - May create large blocks for short minimum suffix lengths
    - Not effective for attributes with high variability at the end of strings

    :param key_func: A function that takes an Entity and returns the value to generate suffixes from
    :param min_suffix_length: The minimum length of suffixes to consider for blocking
    """

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
    return " ".join(str(value) for value in entity.attributes.values()).lower()

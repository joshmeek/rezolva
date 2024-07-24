import hashlib
from typing import Callable, Dict, List

from ..core.base import Blocker, Entity


class LSHBlocker(Blocker):
    """
    A blocking method that uses Locality-Sensitive Hashing (LSH) to create blocks of entities.

    LSH is a technique used to group similar items together. In the context of entity resolution,
    it helps to reduce the number of comparisons needed by grouping potentially similar entities
    into the same block.

    How LSH works:
    1. Convert each entity's attribute into a set of features (e.g., words or n-grams)
    2. Use multiple hash functions to create a signature for each entity
    3. Divide the signature into bands
    4. For each band, hash the band to a bucket
    5. Entities that share at least one bucket are considered candidates for comparison

    This implementation uses MinHash as the LSH technique, which is especially good for
    estimating the Jaccard similarity between sets.

    :param num_hash_functions: The number of hash functions to use for MinHash
    :param band_size: The size of each band for LSH
    :param attribute: The attribute to use for blocking
    """

    def __init__(self, num_hash_functions: int, band_size: int, attribute: str):
        self.num_hash_functions = num_hash_functions
        self.band_size = band_size
        self.attribute = attribute
        self.hash_functions = self._generate_hash_functions()

    def _generate_hash_functions(self):
        return [
            lambda x, i=i: int(hashlib.md5(f"{x}{i}".encode()).hexdigest(), 16) % (2**32 - 1)
            for i in range(self.num_hash_functions)
        ]

    def _minhash_signature(self, text: str) -> List[int]:
        words = set(text.lower().split())
        signature = [min(h(word) for word in words) for h in self.hash_functions]
        return signature

    def create_blocks(self, entities: List[Entity]) -> Dict[str, List[Entity]]:
        blocks = {}
        for entity in entities:
            text = entity.attributes.get(self.attribute, "")
            signature = self._minhash_signature(text)

            for i in range(0, len(signature), self.band_size):
                band = tuple(signature[i : i + self.band_size])
                block_key = hash(band)
                if block_key not in blocks:
                    blocks[block_key] = []
                blocks[block_key].append(entity)

        return blocks

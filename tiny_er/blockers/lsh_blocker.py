from ..core.base import Blocker, Entity
from typing import Dict, List, Callable
import hashlib

class LSHBlocker(Blocker):
    def __init__(self, num_hash_functions: int, band_size: int, attribute: str):
        self.num_hash_functions = num_hash_functions
        self.band_size = band_size
        self.attribute = attribute
        self.hash_functions = self._generate_hash_functions()

    def _generate_hash_functions(self):
        return [lambda x, i=i: int(hashlib.md5(f"{x}{i}".encode()).hexdigest(), 16) % (2**32 - 1)
                for i in range(self.num_hash_functions)]

    def _minhash_signature(self, text: str) -> List[int]:
        words = set(text.lower().split())
        signature = [min(h(word) for word in words) for h in self.hash_functions]
        return signature

    def create_blocks(self, entities: List[Entity]) -> Dict[str, List[Entity]]:
        blocks = {}
        for entity in entities:
            text = entity.attributes.get(self.attribute, '')
            signature = self._minhash_signature(text)
            
            for i in range(0, len(signature), self.band_size):
                band = tuple(signature[i:i+self.band_size])
                block_key = hash(band)
                if block_key not in blocks:
                    blocks[block_key] = []
                blocks[block_key].append(entity)
        
        return blocks
from typing import List, Dict, Any
from ..core.data_structures import Entity, Block
import hashlib
from ..core.base_classes import Blocker

class LSHBlocker(Blocker):
    def __init__(self, config: Dict[str, Any]):
        self.num_hash_functions = config.get('num_hash_functions')
        self.band_size = config.get('band_size')
        self.minhash_fields = config.get('minhash_fields')

    def block(self, entities: List[Entity]) -> List[Block]:
        blocks = {}
        for entity in entities:
            signature = self._minhash_signature(entity)
            band_hashes = self._band_hashes(signature)
            
            for band_hash in band_hashes:
                if band_hash not in blocks:
                    blocks[band_hash] = Block(band_hash)
                blocks[band_hash].add(entity)
        
        return list(blocks.values())

    def _minhash_signature(self, entity: Entity) -> List[int]:
        signature = []
        for i in range(self.num_hash_functions):
            min_hash = float('inf')
            for field in self.minhash_fields:
                value = str(entity.attributes.get(field, ''))
                hash_value = int(hashlib.md5(f"{i}:{value}".encode()).hexdigest(), 16)
                min_hash = min(min_hash, hash_value)
            signature.append(min_hash)
        return signature

    def _band_hashes(self, signature: List[int]) -> List[int]:
        band_hashes = []
        for i in range(0, len(signature), self.band_size):
            band = signature[i:i+self.band_size]
            band_hash = hash(tuple(band))
            band_hashes.append(band_hash)
        return band_hashes

def create_lsh_blocker(config: Dict[str, Any]) -> LSHBlocker:
    return LSHBlocker(config)
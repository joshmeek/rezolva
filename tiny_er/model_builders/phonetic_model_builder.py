from ..core.base import ModelBuilder, Entity
from typing import List, Any, Dict

class PhoneticModelBuilder(ModelBuilder):
    def __init__(self, attributes: List[str]):
        self.attributes = attributes

    def train(self, entities: List[Entity]) -> Any:
        model = {'entities': {}, 'phonetic_index': {}}
        for entity in entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                value = str(entity.attributes.get(attr, ''))
                phonetic_code = self._soundex(value)
                if phonetic_code not in model['phonetic_index']:
                    model['phonetic_index'][phonetic_code] = set()
                model['phonetic_index'][phonetic_code].add(entity.id)
        return model

    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        for entity in new_entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                value = str(entity.attributes.get(attr, ''))
                phonetic_code = self._soundex(value)
                if phonetic_code not in model['phonetic_index']:
                    model['phonetic_index'][phonetic_code] = set()
                model['phonetic_index'][phonetic_code].add(entity.id)
        return model

    def _soundex(self, s: str) -> str:
        if not s:
            return "0000"
        s = s.upper()
        soundex = s[0]
        consonant_sounds = {
            'BFPV': '1', 'CGJKQSXZ': '2', 'DT': '3',
            'L': '4', 'MN': '5', 'R': '6'
        }
        for char in s[1:]:
            for key in consonant_sounds:
                if char in key:
                    code = consonant_sounds[key]
                    if code != soundex[-1]:
                        soundex += code
                    break
            if len(soundex) == 4:
                break
        soundex += '0' * (4 - len(soundex))
        return soundex
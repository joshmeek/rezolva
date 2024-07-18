import re
from typing import Dict, Any, List
from ..core.data_structures import Entity
from ..core.base_classes import Preprocessor

class Normalizer(Preprocessor):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def preprocess(self, entities: List[Entity]) -> List[Entity]:
        return [self.normalize(entity) for entity in entities]

    def normalize(self, entity: Entity) -> Entity:
        normalized_attributes = {}
        for key, value in entity.attributes.items():
            if isinstance(value, str):
                normalized_value = self._normalize_string(value)
            else:
                normalized_value = value
            normalized_attributes[key] = normalized_value
        
        return Entity(id=entity.id, attributes=normalized_attributes)

    def _normalize_string(self, text: str) -> str:
        if self.config.get('lowercase', True):
            text = text.lower()
        
        if self.config.get('remove_punctuation', True):
            text = re.sub(r'[^\w\s]', '', text)
        
        if self.config.get('remove_whitespace', True):
            text = ' '.join(text.split())
        
        return text

def create_normalizer(config: Dict[str, Any]) -> Normalizer:
    return Normalizer(config)
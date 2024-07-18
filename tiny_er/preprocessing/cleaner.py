import re
from typing import Dict, Any, List
from ..core.data_structures import Entity
from ..core.base_classes import Preprocessor

class Cleaner(Preprocessor):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def preprocess(self, entities: List[Entity]) -> List[Entity]:
        return [self.clean(entity) for entity in entities]

    def clean(self, entity: Entity) -> Entity:
        cleaned_attributes = {}
        for key, value in entity.attributes.items():
            if isinstance(value, str):
                cleaned_value = self._clean_string(key, value)
            else:
                cleaned_value = value
            cleaned_attributes[key] = cleaned_value
        
        return Entity(id=entity.id, attributes=cleaned_attributes)

    def _clean_string(self, key: str, value: str) -> str:
        value = value.strip()
        
        if self.config.get('remove_special_characters', False):
            value = re.sub(r'[^a-zA-Z0-9\s]', '', value)
        
        if self.config.get('remove_digits', False):
            value = re.sub(r'\d', '', value)
        
        if key in self.config.get('max_length', {}):
            max_length = self.config['max_length'][key]
            value = value[:max_length]
        
        return value

def create_cleaner(config: Dict[str, Any]) -> Cleaner:
    return Cleaner(config)
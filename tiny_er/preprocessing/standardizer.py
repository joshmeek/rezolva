from typing import Dict, Any, List
from ..core.data_structures import Entity
from ..core.base_classes import Preprocessor

class Standardizer(Preprocessor):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def preprocess(self, entities: List[Entity]) -> List[Entity]:
        return [self.standardize(entity) for entity in entities]

    def standardize(self, entity: Entity) -> Entity:
        standardized_attributes = {}
        for key, value in entity.attributes.items():
            if isinstance(value, str):
                standardized_value = self._standardize_string(key, value)
            else:
                standardized_value = value
            standardized_attributes[key] = standardized_value
        
        return Entity(id=entity.id, attributes=standardized_attributes)

    def _standardize_string(self, key: str, value: str) -> str:
        if key in self.config:
            mapping = self.config[key]
            return mapping.get(value.lower(), value)
        return value

def create_standardizer(config: Dict[str, Any]) -> Standardizer:
    return Standardizer(config)
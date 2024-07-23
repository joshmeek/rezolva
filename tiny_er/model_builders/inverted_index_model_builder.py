import re
from typing import Any, Dict, List

from ..core.base import Entity, ModelBuilder


class InvertedIndexModelBuilder(ModelBuilder):
    def __init__(self, attributes: List[str]):
        self.attributes = attributes

    def train(self, entities: List[Entity]) -> Any:
        model = {'entities': {}, 'index': {}}
        for entity in entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                tokens = self._tokenize(entity.attributes.get(attr, ''))
                for token in tokens:
                    if token not in model['index']:
                        model['index'][token] = set()
                    model['index'][token].add(entity.id)
        return model

    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        for entity in new_entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                tokens = self._tokenize(entity.attributes.get(attr, ''))
                for token in tokens:
                    if token not in model['index']:
                        model['index'][token] = set()
                    model['index'][token].add(entity.id)
        return model

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())
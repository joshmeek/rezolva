from typing import Any, Dict, List

from ..core.base import Entity, ModelBuilder


class SimpleModelBuilder(ModelBuilder):
    def __init__(self, attributes: List[str]):
        self.attributes = attributes

    def train(self, entities: List[Entity]) -> Any:
        model = {'entities': {}, 'index': {}}
        for entity in entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                value = entity.attributes.get(attr, '').lower()
                if value:
                    if attr not in model['index']:
                        model['index'][attr] = {}
                    if value not in model['index'][attr]:
                        model['index'][attr][value] = set()
                    model['index'][attr][value].add(entity.id)
        return model

    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        for entity in new_entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                value = entity.attributes.get(attr, '').lower()
                if value:
                    if attr not in model['index']:
                        model['index'][attr] = {}
                    if value not in model['index'][attr]:
                        model['index'][attr][value] = set()
                    model['index'][attr][value].add(entity.id)
        return model
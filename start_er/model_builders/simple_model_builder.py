from typing import Any, Dict, List

from ..core.base import Entity, ModelBuilder


class SimpleModelBuilder(ModelBuilder):
    """
    A basic model builder that creates a simple index-based model for entity matching.

    This model builder creates two main data structures:
    1. An entity dictionary that maps entity IDs to Entity objects
    2. An attribute index that maps attribute values to sets of entity IDs

    This simple model is efficient for exact matching on attribute values but may not
    perform well for fuzzy matching or complex similarity computations.

    How it works:
    1. For each entity, store it in the entity dictionary
    2. For each attribute of the entity, add the entity ID to the corresponding
       attribute value's set in the attribute index

    Usage:
    builder = SimpleModelBuilder(['name', 'address'])
    model = builder.train(entities)

    :param attributes: A list of attribute names to be indexed
    :inherits: ModelBuilder
    """

    def __init__(self, attributes: List[str]):
        self.attributes = attributes

    def train(self, entities: List[Entity]) -> Any:
        model = {"entities": {}, "index": {}}
        for entity in entities:
            model["entities"][entity.id] = entity
            for attr in self.attributes:
                value = entity.attributes.get(attr, "").lower()
                if value:
                    if attr not in model["index"]:
                        model["index"][attr] = {}
                    if value not in model["index"][attr]:
                        model["index"][attr][value] = set()
                    model["index"][attr][value].add(entity.id)
        return model

    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        for entity in new_entities:
            model["entities"][entity.id] = entity
            for attr in self.attributes:
                value = entity.attributes.get(attr, "").lower()
                if value:
                    if attr not in model["index"]:
                        model["index"][attr] = {}
                    if value not in model["index"][attr]:
                        model["index"][attr][value] = set()
                    model["index"][attr][value].add(entity.id)
        return model

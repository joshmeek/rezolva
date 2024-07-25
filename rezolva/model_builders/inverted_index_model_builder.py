import re
from typing import Any, Dict, List

from ..core.base import Entity, ModelBuilder


class InvertedIndexModelBuilder(ModelBuilder):
    """
    A model builder that creates an inverted index for efficient entity matching.

    This model builder creates an inverted index where each token (word or n-gram)
    is mapped to a list of entity IDs that contain that token in their attributes.

    The inverted index model is particularly useful for text-heavy attributes and
    supports efficient partial matching and keyword search.

    How it works:
    1. Tokenize the specified attributes of each entity
    2. For each token, create an entry in the inverted index pointing to the entity

    Usage:
    builder = InvertedIndexModelBuilder(['name', 'description'])
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
                tokens = self._tokenize(entity.attributes.get(attr, ""))
                for token in tokens:
                    if token not in model["index"]:
                        model["index"][token] = set()
                    model["index"][token].add(entity.id)
        return model

    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        for entity in new_entities:
            model["entities"][entity.id] = entity
            for attr in self.attributes:
                tokens = self._tokenize(entity.attributes.get(attr, ""))
                for token in tokens:
                    if token not in model["index"]:
                        model["index"][token] = set()
                    model["index"][token].add(entity.id)
        return model

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

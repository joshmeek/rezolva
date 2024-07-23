from typing import Any, Callable, List

from ..core.base import Entity, Preprocessor


class SimplePreprocessor(Preprocessor):
    def __init__(self, preprocessing_functions: List[Callable[[Any], Any]] = None):
        self.preprocessing_functions = preprocessing_functions or []

    def preprocess(self, entity: Entity) -> Entity:
        processed_attributes = {}
        for key, value in entity.attributes.items():
            for func in self.preprocessing_functions:
                value = func(value)
            processed_attributes[key] = value
        return Entity(entity.id, processed_attributes)

    def add_preprocessing_function(self, func: Callable[[Any], Any]):
        self.preprocessing_functions.append(func)

    def remove_preprocessing_function(self, func: Callable[[Any], Any]):
        self.preprocessing_functions.remove(func)
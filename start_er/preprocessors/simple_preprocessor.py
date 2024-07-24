from typing import Any, Callable, List

from ..core.base import Entity, Preprocessor


class SimplePreprocessor(Preprocessor):
    """
    A flexible preprocessor that applies a series of preprocessing functions to entity attributes.

    This preprocessor allows for the configuration of multiple preprocessing steps that are
    applied in sequence to each attribute of an entity. This modular approach enables easy
    customization of the preprocessing pipeline for different entity resolution scenarios.

    Common preprocessing steps might include:
    - Lowercasing
    - Removing punctuation
    - Stripping whitespace
    - Normalizing dates or phone numbers
    - Removing stop words

    Usage:
    preprocessor = SimplePreprocessor([lowercase, remove_punctuation, strip_whitespace])
    processed_entity = preprocessor.preprocess(entity)

    :param preprocessing_functions: A list of functions to be applied to each attribute
    :inherits: Preprocessor
    """

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

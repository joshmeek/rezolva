from typing import Any, List, Tuple

from ..core.base import (Blocker, DataLoader, DataSaver, Entity, Matcher,
                         ModelBuilder, Preprocessor)


class EntityResolver:
    """
    The main class orchestrating the entity resolution process.

    EntityResolver combines all components of the entity resolution pipeline (preprocessor,
    model builder, matcher, and blocker) to perform the complete entity resolution task.
    It provides methods to train the resolution model and resolve new entities.

    How EntityResolver works:
    1. Preprocess input entities using the specified preprocessor
    2. Build or update the resolution model using the model builder
    3. Create blocks of potentially matching entities using the blocker
    4. Compare entities within each block using the matcher
    5. Return the matched entities above a specified threshold

    :param preprocessor: An instance of a Preprocessor subclass
    :param model_builder: An instance of a ModelBuilder subclass
    :param matcher: An instance of a Matcher subclass
    :param blocker: An instance of a Blocker subclass
    """

    def __init__(self, preprocessor: Preprocessor, model_builder: ModelBuilder, matcher: Matcher, blocker: Blocker):
        self.preprocessor = preprocessor
        self.model_builder = model_builder
        self.matcher = matcher
        self.blocker = blocker
        self.model = None

    def train(self, entities: List[Entity]):
        preprocessed_entities = [self.preprocessor.preprocess(e) for e in entities]
        self.model = self.model_builder.train(preprocessed_entities)

        # Call the matcher's train method if it exists
        if hasattr(self.matcher, "train") and callable(getattr(self.matcher, "train")):
            self.matcher.train(preprocessed_entities)

    def resolve(self, entities: List[Entity], top_k: int = 1) -> List[Tuple[Entity, List[Tuple[Entity, float]]]]:
        if not self.model:
            raise ValueError("Model not trained. Call train() first.")

        preprocessed_entities = [self.preprocessor.preprocess(e) for e in entities]
        blocks = self.blocker.create_blocks(preprocessed_entities)

        results = []
        for block in blocks.values():
            for entity in block:
                matches = self.matcher.match(entity, self.model)
                if matches:
                    results.append((entity, matches[:top_k]))

        return results

    def update_model(self, new_entities: List[Entity]):
        preprocessed_entities = [self.preprocessor.preprocess(e) for e in new_entities]
        self.model = self.model_builder.update(self.model, preprocessed_entities)

        # Update the matcher if it has an update method
        if hasattr(self.matcher, "update") and callable(getattr(self.matcher, "update")):
            self.matcher.update(preprocessed_entities)

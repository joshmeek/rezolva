from typing import Any, List, Tuple

from ..core.base import (Blocker, DataLoader, DataSaver, Entity, Matcher,
                         ModelBuilder, Preprocessor)


class EntityResolver:
    def __init__(self, preprocessor, model_builder, matcher, blocker):
        self.preprocessor = preprocessor
        self.model_builder = model_builder
        self.matcher = matcher
        self.blocker = blocker
        self.model = None

    def train(self, entities: List[Entity]):
        preprocessed_entities = [self.preprocessor.preprocess(e) for e in entities]
        self.model = self.model_builder.train(preprocessed_entities)

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
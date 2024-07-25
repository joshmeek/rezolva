import itertools
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from ..core.base import (Blocker, DataLoader, DataSaver, Entity, Matcher,
                         ModelBuilder, Preprocessor)


class EntityResolver:
    """
    The main class orchestrating the entity resolution process.

    EntityResolver combines all components of the entity resolution pipeline (preprocessor,
    model builder, matcher, and blocker) to perform the complete entity resolution task.
    It provides methods to train the resolution model, resolve new entities, update the model,
    and perform bulk resolutions.

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
        self.preprocessed_entities = {}
        self.blocks = {}

    def train(self, entities: List[Entity]):
        self.preprocessed_entities = {e.id: self.preprocessor.preprocess(e) for e in entities}
        self.model = self.model_builder.train(list(self.preprocessed_entities.values()))
        self.blocks = self.blocker.create_blocks(list(self.preprocessed_entities.values()))

        for block, entities in self.blocks.items():
            self.blocks[block] = {e.id for e in entities}  # Store entity IDs instead of Entity objects

        # Train the matcher if it has a train method
        if hasattr(self.matcher, "train") and callable(getattr(self.matcher, "train")):
            self.matcher.train(list(self.preprocessed_entities.values()))

    def resolve(self, entities: List[Entity], top_k: int = 1) -> List[Tuple[Entity, List[Tuple[Entity, float]]]]:
        if not self.model:
            raise ValueError("Model not trained. Call train() first.")

        new_preprocessed = {e.id: self.preprocessor.preprocess(e) for e in entities}
        new_blocks = self.blocker.create_blocks(list(new_preprocessed.values()))

        results = []
        for entity in entities:
            preprocessed_entity = new_preprocessed[entity.id]
            entity_block = next(
                (block for block, block_entities in new_blocks.items() if preprocessed_entity in block_entities), None
            )

            if entity_block is None:
                continue

            candidates = self.blocks.get(entity_block, set())
            matches = self._find_matches(preprocessed_entity, candidates, top_k)
            if matches:
                results.append((entity, matches))

        return results

    def _find_matches(self, entity: Entity, candidates: set, top_k: int) -> List[Tuple[Entity, float]]:
        candidate_entities = {
            id: self.preprocessed_entities[id] for id in candidates if id in self.preprocessed_entities
        }
        matches = self.matcher.match(entity, {"entities": candidate_entities})
        return sorted(matches, key=lambda x: x[1], reverse=True)[:top_k]

    def update_model(self, new_entities: List[Entity]):
        new_preprocessed = {e.id: self.preprocessor.preprocess(e) for e in new_entities}
        self.preprocessed_entities.update(new_preprocessed)
        self.model = self.model_builder.update(self.model, list(new_preprocessed.values()))

        new_blocks = self.blocker.create_blocks(list(new_preprocessed.values()))
        for key, entities in new_blocks.items():
            if key not in self.blocks:
                self.blocks[key] = set()
            self.blocks[key].update(e.id for e in entities)

    def bulk_resolve(
        self, entities: List[Entity], batch_size: int = 100, top_k: int = 1
    ) -> List[Tuple[Entity, List[Tuple[Entity, float]]]]:
        results = []
        for i in range(0, len(entities), batch_size):
            batch = entities[i : i + batch_size]
            results.extend(self.resolve(batch, top_k))
        return results

    def save_model(self, path: str):
        import pickle

        with open(path, "wb") as f:
            pickle.dump(
                {"model": self.model, "preprocessed_entities": self.preprocessed_entities, "blocks": self.blocks}, f
            )

    def load_model(self, path: str):
        import pickle

        with open(path, "rb") as f:
            data = pickle.load(f)
            self.model = data["model"]
            self.preprocessed_entities = data["preprocessed_entities"]
            self.blocks = data["blocks"]

    def get_stats(self) -> Dict[str, Any]:
        return {
            "num_entities": len(self.preprocessed_entities),
            "num_blocks": len(self.blocks),
            "avg_block_size": (
                sum(len(block) for block in self.blocks.values()) / len(self.blocks) if self.blocks else 0
            ),
            "model_size": (
                self.model_builder.get_model_size(self.model) if hasattr(self.model_builder, "get_model_size") else None
            ),
        }

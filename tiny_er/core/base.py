from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class Entity:
    def __init__(self, id: str, attributes: Dict[str, Any]):
        self.id = id
        self.attributes = attributes

class Preprocessor(ABC):
    @abstractmethod
    def preprocess(self, entity: Entity) -> Entity:
        pass

class ModelBuilder(ABC):
    @abstractmethod
    def train(self, entities: List[Entity]) -> Any:
        pass

    @abstractmethod
    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        pass

class Matcher(ABC):
    @abstractmethod
    def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
        pass

class Blocker(ABC):
    @abstractmethod
    def create_blocks(self, entities: List[Entity]) -> Dict[Any, List[Entity]]:
        pass

class DataLoader(ABC):
    @abstractmethod
    def load(self, source: Any) -> List[Entity]:
        pass

class DataSaver(ABC):
    @abstractmethod
    def save(self, entities: List[Entity], destination: Any):
        pass
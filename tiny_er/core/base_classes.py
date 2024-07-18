from abc import ABC, abstractmethod
from typing import List
from .data_structures import Entity, Comparison, MatchResult, Block

class Preprocessor(ABC):
    @abstractmethod
    def preprocess(self, entities: List[Entity]) -> List[Entity]:
        pass

class Blocker(ABC):
    @abstractmethod
    def block(self, entities: List[Entity]) -> List[Block]:
        pass

class SimilarityMeasure(ABC):
    @abstractmethod
    def compute(self, entity1: Entity, entity2: Entity) -> float:
        pass

class Matcher(ABC):
    @abstractmethod
    def match(self, comparisons: List[Comparison]) -> List[MatchResult]:
        pass
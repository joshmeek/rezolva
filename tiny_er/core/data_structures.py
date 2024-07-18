from typing import Dict, List, Any, Set
from dataclasses import dataclass, field

@dataclass
class Entity:
    """
    Represents a single entity with a unique identifier and attributes.
    """
    id: str
    attributes: Dict[str, Any]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

@dataclass
class Cluster:
    """
    Represents a cluster of entities that are considered to be the same real-world entity.
    """
    entities: Set[Entity] = field(default_factory=set)

    def add(self, entity: Entity):
        """Add an entity to the cluster."""
        self.entities.add(entity)

    def remove(self, entity: Entity):
        """Remove an entity from the cluster."""
        self.entities.remove(entity)

    def merge(self, other: 'Cluster'):
        """Merge another cluster into this one."""
        self.entities.update(other.entities)

    def __len__(self):
        return len(self.entities)

    def __iter__(self):
        return iter(self.entities)

@dataclass
class Comparison:
    """
    Represents a comparison between two entities, including their similarity score.
    """
    entity1: Entity
    entity2: Entity
    similarity: float

@dataclass
class MatchResult:
    """
    Represents the result of a matching process, including the matched entities and the confidence score.
    """
    entity1: Entity
    entity2: Entity
    confidence: float
    is_match: bool

class Block:
    """
    Represents a block of potentially matching entities.
    """
    def __init__(self, key: Any, entities: List[Entity] = None):
        self.key = key
        self.entities: List[Entity] = entities or []

    def add(self, entity: Entity):
        self.entities.append(entity)

    def __len__(self):
        return len(self.entities)

    def __iter__(self):
        return iter(self.entities)

    def __getitem__(self, index):
        return self.entities[index]
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class Entity:
    """
    Represents an entity in the entity resolution process.

    An entity is a fundamental unit in entity resolution, typically representing a real-world object
    or concept. It contains an identifier and a set of attributes that describe its characteristics.

    :param id: A unique identifier for the entity
    :param attributes: A dictionary of attribute names and their corresponding values
    """

    def __init__(self, id: str, attributes: Dict[str, Any]):
        self.id = id
        self.attributes = attributes


class Preprocessor(ABC):
    """
    Abstract base class for preprocessors in the entity resolution pipeline.

    Preprocessors are responsible for cleaning, standardizing, and transforming raw entity data
    before it's used in the matching process. This can include operations like lowercasing,
    removing punctuation, standardizing formats, etc.

    Subclasses should implement the `preprocess` method to define specific preprocessing logic.
    """

    @abstractmethod
    def preprocess(self, entity: Entity) -> Entity:
        pass


class ModelBuilder(ABC):
    """
    Abstract base class for model builders in the entity resolution pipeline.

    Model builders are responsible for creating and updating the data structures or models
    used for efficient entity matching. This could involve creating inverted indices,
    vector representations, or other data structures optimized for the chosen matching algorithm.

    Subclasses should implement the `train` and `update` methods to define specific model building logic.
    """

    @abstractmethod
    def train(self, entities: List[Entity]) -> Any:
        pass

    @abstractmethod
    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        pass


class Matcher(ABC):
    """
    Abstract base class for matchers in the entity resolution pipeline.

    Matchers are responsible for comparing entities and determining their similarity or
    the likelihood that they refer to the same real-world entity. Different matching
    algorithms can be implemented by subclassing this class.

    Subclasses should implement the `match` method to define specific matching logic.
    """

    @abstractmethod
    def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
        pass


class Blocker(ABC):
    """
    Abstract base class for blockers in the entity resolution pipeline.

    Blockers are used to reduce the number of comparisons needed in the matching phase
    by grouping potentially similar entities into blocks. Only entities within the same
    block are compared, significantly reducing the computational cost of entity resolution.

    Subclasses should implement the `create_blocks` method to define specific blocking logic.
    """

    @abstractmethod
    def create_blocks(self, entities: List[Entity]) -> Dict[Any, List[Entity]]:
        pass


class DataLoader(ABC):
    """
    Abstract base class for data loaders in the entity resolution pipeline.

    Data loaders are responsible for reading entity data from various sources (e.g., databases,
    CSV files, JSON files) and converting them into Entity objects that can be used in the
    entity resolution process.

    Subclasses should implement the `load` method to define specific data loading logic.
    """

    @abstractmethod
    def load(self, source: Any) -> List[Entity]:
        pass


class DataSaver(ABC):
    """
    Abstract base class for data savers in the entity resolution pipeline.

    Data savers are responsible for writing resolved entity data back to storage. This could
    involve updating a database, writing to a file, or interfacing with other data storage systems.

    Subclasses should implement the `save` method to define specific data saving logic.
    """

    @abstractmethod
    def save(self, entities: List[Entity], destination: Any):
        pass

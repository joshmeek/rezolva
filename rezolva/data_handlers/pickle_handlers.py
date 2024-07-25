import pickle
from typing import List

from ..core.base import DataLoader, DataSaver, Entity


class PickleDataLoader(DataLoader):
    """
    A data loader for Pickle files.

    This class is responsible for loading entity data from Pickle files. It reads the Pickle file
    and deserializes it into a list of Entity instances.

    Pickle Format:
    The Pickle file should contain a serialized list of Entity objects.

    Usage:
    loader = PickleDataLoader()
    entities = loader.load("path/to/data.pkl")

    Note: Be cautious when using Pickle files from untrusted sources, as they can pose a security risk.

    :inherits: DataLoader
    """

    def load(self, source: str) -> List[Entity]:
        with open(source, "rb") as f:
            return pickle.load(f)


class PickleDataSaver(DataSaver):
    """
    A data saver for Pickle files.

    This class is responsible for saving entity data to Pickle files. It serializes a list of
    Entity instances and writes them to a file.

    Usage:
    saver = PickleDataSaver()
    saver.save(entities, "path/to/output.pkl")

    Note: Pickle files are not human-readable and may not be compatible across different
    Python versions or platforms. Use with caution.

    :inherits: DataSaver
    """

    def save(self, entities: List[Entity], destination: str):
        with open(destination, "wb") as f:
            pickle.dump(entities, f)

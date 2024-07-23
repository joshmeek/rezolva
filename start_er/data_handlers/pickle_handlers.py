import pickle
from typing import List

from ..core.base import DataLoader, DataSaver, Entity


class PickleDataLoader(DataLoader):
    def load(self, source: str) -> List[Entity]:
        with open(source, 'rb') as f:
            return pickle.load(f)

class PickleDataSaver(DataSaver):
    def save(self, entities: List[Entity], destination: str):
        with open(destination, 'wb') as f:
            pickle.dump(entities, f)
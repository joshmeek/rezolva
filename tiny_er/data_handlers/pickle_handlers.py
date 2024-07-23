import pickle
from ..core.base import DataLoader, DataSaver, Entity
from typing import List

class PickleDataLoader(DataLoader):
    def load(self, source: str) -> List[Entity]:
        with open(source, 'rb') as f:
            return pickle.load(f)

class PickleDataSaver(DataSaver):
    def save(self, entities: List[Entity], destination: str):
        with open(destination, 'wb') as f:
            pickle.dump(entities, f)
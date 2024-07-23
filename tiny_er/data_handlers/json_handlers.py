import json
from typing import List

from ..core.base import DataLoader, DataSaver, Entity


class JSONDataLoader(DataLoader):
    def load(self, source: str) -> List[Entity]:
        with open(source, 'r') as f:
            data = json.load(f)
        return [Entity(item['id'], item['attributes']) for item in data]

class JSONDataSaver(DataSaver):
    def save(self, entities: List[Entity], destination: str):
        data = [{'id': entity.id, 'attributes': entity.attributes} for entity in entities]
        with open(destination, 'w') as f:
            json.dump(data, f, indent=2)
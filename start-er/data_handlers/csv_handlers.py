import csv
from typing import List

from ..core.base import DataLoader, DataSaver, Entity


class CSVDataLoader(DataLoader):
    def load(self, source: str) -> List[Entity]:
        entities = []
        with open(source, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entity_id = row.pop('id', str(len(entities)))
                entities.append(Entity(entity_id, row))
        return entities

class CSVDataSaver(DataSaver):
    def save(self, entities: List[Entity], destination: str):
        if not entities:
            return

        fieldnames = ['id'] + list(entities[0].attributes.keys())
        
        with open(destination, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entity in entities:
                row = {'id': entity.id, **entity.attributes}
                writer.writerow(row)
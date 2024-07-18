import csv
from typing import List, Dict, Any
from ..core.data_structures import Entity

def load_csv(file_path: str, id_column: str) -> List[Entity]:
    entities = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entity_id = row.pop(id_column)
            entity = Entity(id=entity_id, attributes=row)
            entities.append(entity)
    return entities

def load_json(file_path: str, id_key: str) -> List[Entity]:
    import json
    entities = []
    with open(file_path, 'r') as jsonfile:
        data = json.load(jsonfile)
        for item in data:
            entity_id = item.pop(id_key)
            entity = Entity(id=entity_id, attributes=item)
            entities.append(entity)
    return entities

def save_results(file_path: str, results: List[Dict[str, Any]]):
    with open(file_path, 'w') as csvfile:
        if not results:
            return
        fieldnames = results[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
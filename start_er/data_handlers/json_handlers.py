import json
from typing import List

from ..core.base import DataLoader, DataSaver, Entity


class JSONDataLoader(DataLoader):
    """
    A data loader for JSON files.

    This class is responsible for loading entity data from JSON files. It reads the JSON file
    and converts each JSON object into an Entity instance.

    JSON Format:
    The expected JSON format is an array of objects, where each object represents an entity.
    Each entity object should have an 'id' field and an 'attributes' field containing key-value pairs.

    Example JSON structure:
    [
        {
            "id": "1",
            "attributes": {
                "name": "John Doe",
                "age": 30,
                "city": "New York"
            }
        },
        ...
    ]

    Usage:
    loader = JSONDataLoader()
    entities = loader.load("path/to/data.json")

    :inherits: DataLoader
    """

    def load(self, source: str) -> List[Entity]:
        with open(source, "r") as f:
            data = json.load(f)
        return [Entity(item["id"], item["attributes"]) for item in data]


class JSONDataSaver(DataSaver):
    """
    A data saver for JSON files.

    This class is responsible for saving entity data to JSON files. It converts Entity instances
    into JSON objects and writes them to a file.

    The output JSON will have the same structure as expected by JSONDataLoader.

    Usage:
    saver = JSONDataSaver()
    saver.save(entities, "path/to/output.json")

    :inherits: DataSaver
    """

    def save(self, entities: List[Entity], destination: str):
        data = [{"id": entity.id, "attributes": entity.attributes} for entity in entities]
        with open(destination, "w") as f:
            json.dump(data, f, indent=2)

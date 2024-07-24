import csv
from typing import List

from ..core.base import DataLoader, DataSaver, Entity


class CSVDataLoader(DataLoader):
    """
    A data loader for CSV files.

    This class is responsible for loading entity data from CSV files. It reads the CSV file
    and converts each row into an Entity instance.

    CSV Format:
    The CSV file should have a header row. One column should be designated as the 'id' column.
    All other columns will be treated as attributes of the entity.

    Example CSV structure:
    id,name,age,city
    1,John Doe,30,New York
    2,Jane Smith,25,Los Angeles
    ...

    If no 'id' column is present, the loader will generate numeric IDs starting from 0.

    Usage:
    loader = CSVDataLoader()
    entities = loader.load("path/to/data.csv")

    :inherits: DataLoader
    """

    def load(self, source: str) -> List[Entity]:
        entities = []
        with open(source, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entity_id = row.pop("id", str(len(entities)))
                entities.append(Entity(entity_id, row))
        return entities


class CSVDataSaver(DataSaver):
    """
    A data saver for CSV files.

    This class is responsible for saving entity data to CSV files. It converts Entity instances
    into CSV rows and writes them to a file.

    The output CSV will have the same structure as expected by CSVDataLoader.

    Usage:
    saver = CSVDataSaver()
    saver.save(entities, "path/to/output.csv")

    :inherits: DataSaver
    """

    def save(self, entities: List[Entity], destination: str):
        if not entities:
            return

        fieldnames = ["id"] + list(entities[0].attributes.keys())

        with open(destination, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entity in entities:
                row = {"id": entity.id, **entity.attributes}
                writer.writerow(row)

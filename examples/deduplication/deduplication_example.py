import csv
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

from start_er import Entity, EntityResolver
from start_er.blockers import SortedNeighborhoodBlocker
from start_er.matchers import CosineSimilarityMatcher
from start_er.model_builders import SimpleModelBuilder


class CustomAdvancedPreprocessor:
    def __init__(self):
        self.ner_tags = {
            "PERSON": ["mr", "mrs", "ms", "dr", "prof"],
            "ORGANIZATION": ["inc", "corp", "llc", "ltd"],
            "LOCATION": ["st", "ave", "blvd", "rd", "highway", "hwy"],
        }

    def preprocess(self, entity: Entity) -> Entity:
        processed_attributes = {}
        for key, value in entity.attributes.items():
            if isinstance(value, str):
                value = self._preprocess_string(value, key)
            processed_attributes[key] = value
        return Entity(entity.id, processed_attributes)

    def _preprocess_string(self, value: str, attribute: str) -> str:
        value = value.strip().lower()
        if "name" in attribute:
            value = self._process_name(value)
        elif "address" in attribute:
            value = self._process_address(value)
        elif "phone" in attribute:
            value = self._process_phone(value)
        elif "email" in attribute:
            value = self._process_email(value)
        elif "date" in attribute:
            value = self._normalize_date(value)
        return value

    def _process_name(self, name: str) -> str:
        parts = name.split()
        processed_parts = []
        for part in parts:
            if part not in self.ner_tags["PERSON"]:
                processed_parts.append(part.capitalize())
        return " ".join(processed_parts)

    def _process_address(self, address: str) -> str:
        address = re.sub(r"\bstreet\b", "st", address)
        address = re.sub(r"\bavenue\b", "ave", address)
        address = re.sub(r"\bboulevard\b", "blvd", address)
        address = re.sub(r"\broad\b", "rd", address)
        return " ".join(word.capitalize() for word in address.split())

    def _process_phone(self, phone: str) -> str:
        return re.sub(r"\D", "", phone)  # Remove non-digit characters

    def _process_email(self, email: str) -> str:
        return email.lower()

    def _normalize_date(self, date_string: str) -> str:
        date_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%B %d, %Y",
            "%d %B %Y",
            "%Y/%m/%d",
            "%d.%m.%Y",
            "%m.%d.%Y",
        ]

        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_string, fmt)
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue

        return date_string  # Return original if no format matches


# Conflict resolution strategies
def most_common(values: List[Any]) -> Any:
    return Counter(values).most_common(1)[0][0]


def longest(values: List[Any]) -> Any:
    return max(values, key=lambda x: len(str(x)) if x is not None else 0)


def newest(values: List[Any]) -> Any:
    return max(values)


# Merge entities
def merge_entities(entities: List[Entity]) -> Entity:
    merged_attributes = {}
    all_keys = set()
    for entity in entities:
        all_keys.update(entity.attributes.keys())

    for key in all_keys:
        values = [entity.attributes.get(key) for entity in entities if key in entity.attributes]
        if len(set(values)) == 1:
            merged_attributes[key] = values[0]
        else:
            if key in ["name", "address"]:
                merged_attributes[key] = longest(values)
            elif key in ["email", "phone"]:
                merged_attributes[key] = most_common(values)
            else:
                merged_attributes[key] = newest(values)

    return Entity(f"merged_{entities[0].id}", merged_attributes)


# Load data from CSV
def load_data(file_path: str) -> List[Entity]:
    entities = []
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entities.append(Entity(row["id"], row))
    return entities


# Save deduplicated data to CSV
def save_data(file_path: str, entities: List[Entity]):
    with open(file_path, "w", newline="") as csvfile:
        fieldnames = entities[0].attributes.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity in entities:
            writer.writerow(entity.attributes)


# Main deduplication process
def deduplicate(input_file: str, output_file: str):
    # Load data
    entities = load_data(input_file)
    print(f"Loaded {len(entities)} entities")

    # Set up components
    preprocessor = CustomAdvancedPreprocessor()
    model_builder = SimpleModelBuilder(["name", "email", "phone", "address"])
    matcher = CosineSimilarityMatcher(
        threshold=0.8, attribute_weights={"name": 2.0, "email": 1.5, "phone": 1.0, "address": 1.0}
    )
    blocker = SortedNeighborhoodBlocker(key_func=lambda e: e.attributes["name"].split()[0].lower(), window_size=3)

    # Create resolver
    resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

    # Train the resolver
    resolver.train(entities)

    # Resolve entities
    results = resolver.resolve(entities)

    # Deduplicate and merge
    deduplicated_entities = []
    processed_ids = set()

    for entity, matches in results:
        if entity.id in processed_ids:
            continue

        if matches:
            entities_to_merge = [entity] + [match[0] for match in matches]
            merged_entity = merge_entities(entities_to_merge)
            deduplicated_entities.append(merged_entity)
            processed_ids.update(e.id for e in entities_to_merge)
        else:
            deduplicated_entities.append(entity)
            processed_ids.add(entity.id)

    print(f"Deduplicated to {len(deduplicated_entities)} entities")

    # Save deduplicated data
    save_data(output_file, deduplicated_entities)
    print(f"Saved deduplicated data to {output_file}")


if __name__ == "__main__":
    input_file = "input_data.csv"
    output_file = "deduplicated_data.csv"
    deduplicate(input_file, output_file)

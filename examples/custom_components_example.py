from typing import Any, Dict, List, Tuple

from rezolva import (Entity, EntityResolver, SimpleModelBuilder,
                      SimplePreprocessor)
from rezolva.core.base import Blocker, Matcher


class CustomBlocker(Blocker):
    def create_blocks(self, entities: List[Entity]) -> Dict[str, List[Entity]]:
        blocks = {}
        for entity in entities:
            key = f"{entity.attributes['brand']}_{entity.attributes['category']}"
            if key not in blocks:
                blocks[key] = []
            blocks[key].append(entity)
        return blocks


class CustomMatcher(Matcher):
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def match(self, entity: Entity, model: dict) -> List[Tuple[Entity, float]]:
        matches = []
        for candidate_id, candidate in model["entities"].items():
            if candidate_id != entity.id:
                score = self._calculate_similarity(entity, candidate)
                if score >= self.threshold:
                    matches.append((candidate, score))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_similarity(self, entity1: Entity, entity2: Entity) -> float:
        title_sim = self._jaccard_similarity(entity1.attributes["title"], entity2.attributes["title"])
        desc_sim = self._jaccard_similarity(entity1.attributes["description"], entity2.attributes["description"])
        return (title_sim * 0.6) + (desc_sim * 0.4)

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0


# Set up components
preprocessor = SimplePreprocessor([str.lower, str.strip])
model_builder = SimpleModelBuilder(["title", "description", "brand", "category"])
matcher = CustomMatcher(threshold=0.3)
blocker = CustomBlocker()

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity(
        "1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple", "category": "Phones"}
    ),
    Entity(
        "2", {"title": "MacBook Pro", "description": "Powerful Apple laptop", "brand": "Apple", "category": "Laptops"}
    ),
    Entity(
        "3",
        {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung", "category": "Phones"},
    ),
    Entity(
        "4",
        {
            "title": "Galaxy Book",
            "description": "Samsung's lightweight laptop",
            "brand": "Samsung",
            "category": "Laptops",
        },
    ),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity(
        "5",
        {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple", "category": "Phones"},
    ),
    Entity(
        "6",
        {
            "title": "Galaxy Book Pro",
            "description": "Samsung's premium laptop",
            "brand": "Samsung",
            "category": "Laptops",
        },
    ),
]

# Resolve entities
results = resolver.resolve(new_entities)

# Print results
for entity, matches in results:
    print(f"Top matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches[:2]:  # Limiting to top 2 matches
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
    print()

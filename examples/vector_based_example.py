from rezolva import Entity, EntityResolver, SimpleBlocker, SimplePreprocessor
from rezolva.matchers import CosineSimilarityMatcher
from rezolva.model_builders import SimpleVectorModelBuilder
from rezolva.preprocessors.preprocessing_functions import (lowercase,
                                                            remove_punctuation,
                                                            strip_whitespace)

# Set up components
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleVectorModelBuilder(["title", "description", "brand"])
matcher = CosineSimilarityMatcher(threshold=0.5, attribute_weights={"title": 2.0, "description": 1.5, "brand": 1.0})
blocker = SimpleBlocker(lambda e: e.attributes["brand"].lower())

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity(
        "1", {"title": "iPhone 12", "description": "Latest Apple smartphone with A14 Bionic chip", "brand": "Apple"}
    ),
    Entity(
        "2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone with LiDAR scanner", "brand": "Apple"}
    ),
    Entity(
        "3", {"title": "Galaxy S21", "description": "Samsung's flagship phone with Exynos 2100", "brand": "Samsung"}
    ),
    Entity("4", {"title": "Pixel 5", "description": "Google's latest smartphone with 5G support", "brand": "Google"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity(
        "5",
        {
            "title": "iPhone 12 Pro Max",
            "description": "Apple's largest premium smartphone with A14 chip",
            "brand": "Apple",
        },
    ),
    Entity(
        "6",
        {
            "title": "Galaxy S21 Ultra",
            "description": "Samsung's premium flagship with Exynos 2100 and S Pen support",
            "brand": "Samsung",
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

# Inspect the vector representation of entities
print("\nVector representations:")
for entity_id, entity_vector in resolver.model["vectors"].items():
    print(f"Entity {entity_id}:")
    top_5_terms = sorted(entity_vector.items(), key=lambda x: x[1], reverse=True)[:5]
    for term, value in top_5_terms:
        print(f"  {term}: {value:.4f}")
    print()

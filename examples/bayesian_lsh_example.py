from rezolva import Entity, EntityResolver, SimplePreprocessor
from rezolva.blockers import LSHBlocker
from rezolva.matchers import BayesianMatcher
from rezolva.model_builders import SimpleModelBuilder
from rezolva.preprocessors.preprocessing_functions import (lowercase,
                                                           remove_punctuation,
                                                           strip_whitespace)

# Set up components
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleModelBuilder(["title", "description", "brand"])
matcher = BayesianMatcher(threshold=0.3, attribute_weights={"title": 2.0, "description": 1.5, "brand": 1.0})
blocker = LSHBlocker(num_hash_functions=3, band_size=1, attribute="description")

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
    Entity("5", {"title": "iPhone SE", "description": "Compact Apple smartphone with A13 Bionic", "brand": "Apple"}),
    Entity(
        "6",
        {"title": "Galaxy Note 20", "description": "Samsung's productivity powerhouse with S Pen", "brand": "Samsung"},
    ),
    Entity(
        "7",
        {
            "title": "Pixel 4a",
            "description": "Google's budget-friendly smartphone with great camera",
            "brand": "Google",
        },
    ),
    Entity(
        "8",
        {
            "title": "iPhone 11",
            "description": "Previous generation Apple smartphone with dual camera",
            "brand": "Apple",
        },
    ),
    Entity(
        "9",
        {"title": "Galaxy A52", "description": "Samsung's mid-range phone with 5G capabilities", "brand": "Samsung"},
    ),
    Entity(
        "10",
        {
            "title": "Pixel 4 XL",
            "description": "Google's previous flagship with advanced camera features",
            "brand": "Google",
        },
    ),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity(
        "11",
        {
            "title": "iPhone 12 Pro Max",
            "description": "Apple's largest premium smartphone with A14 chip",
            "brand": "Apple",
        },
    ),
    Entity(
        "12",
        {
            "title": "Galaxy S21 Ultra",
            "description": "Samsung's premium flagship with Exynos 2100 and S Pen support",
            "brand": "Samsung",
        },
    ),
    Entity(
        "13", {"title": "Pixel 5a", "description": "Google's latest mid-range smartphone with 5G", "brand": "Google"}
    ),
]

# Resolve entities
results = resolver.resolve(new_entities)

print("\nAll match scores:")
for new_entity in new_entities:
    print(f"\nMatches for {new_entity.id} - {new_entity.attributes['title']}:")
    all_matches = matcher.match(new_entity, resolver.model)
    for match, score in all_matches:
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.4f})")

from start_er import (Entity, EntityResolver, SimpleBlocker,
                      SimpleModelBuilder, SimplePreprocessor)
from start_er.matchers import CosineSimilarityMatcher
from start_er.preprocessors.preprocessing_functions import (extract_initials,
                                                            lowercase,
                                                            normalize_phone,
                                                            remove_accents,
                                                            remove_punctuation,
                                                            strip_whitespace)


def custom_brand_normalizer(value):
    brand_mapping = {
        "apple": "Apple Inc.",
        "samsung": "Samsung Electronics",
        "google": "Google LLC"
    }
    return brand_mapping.get(value.lower(), value)

# Set up components with advanced preprocessing
preprocessor = SimplePreprocessor([
    lowercase,
    strip_whitespace,
    remove_punctuation,
    remove_accents,
    lambda x: normalize_phone(x) if isinstance(x, str) and x.replace('-', '').isdigit() else x,
    lambda x: custom_brand_normalizer(x) if isinstance(x, str) else x,
    lambda x: extract_initials(x) if isinstance(x, str) and len(x.split()) > 1 else x
])

model_builder = SimpleModelBuilder(['title', 'description', 'brand', 'contact'])
matcher = CosineSimilarityMatcher(threshold=0.6, attribute_weights={'title': 2.0, 'description': 1.5, 'brand': 1.0, 'contact': 0.5})
blocker = SimpleBlocker(lambda e: e.attributes['brand'].lower())

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple", "contact": "1-800-275-2273"}),
    Entity("2", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung", "contact": "1-800-726-7864"}),
    Entity("3", {"title": "Pixel 5", "description": "Google's latest smartphone", "brand": "Google", "contact": "1-855-836-3987"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity("4", {"title": "iPhone 12 Pro Max", "description": "Apple's largest premium smartphone", "brand": "apple", "contact": "18002752273"}),
    Entity("5", {"title": "Galaxy S21 Ultra", "description": "Samsung's premium flagship phone", "brand": "SAMSUNG", "contact": "1 (800) 726-7864"}),
]

# Resolve entities
results = resolver.resolve(new_entities)

# Print results
for entity, matches in results:
    print(f"Top matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches[:2]:  # Limiting to top 2 matches
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
    print()

# Print preprocessed entities to show the effects of preprocessing
print("Preprocessed Entities:")
for entity in new_entities:
    preprocessed = preprocessor.preprocess(entity)
    print(f"Entity {preprocessed.id}:")
    for key, value in preprocessed.attributes.items():
        print(f"  {key}: {value}")
    print()
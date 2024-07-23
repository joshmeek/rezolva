from tiny_er import EntityResolver, Entity, SimplePreprocessor, SimpleModelBuilder, SimpleBlocker
from tiny_er.matchers import CosineSimilarityMatcher
from tiny_er.preprocessors.preprocessing_functions import lowercase, strip_whitespace, remove_punctuation

# Set up components
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleModelBuilder(['title', 'description', 'brand'])
matcher = CosineSimilarityMatcher(threshold=0.5, attribute_weights={'title': 2.0, 'description': 1.5, 'brand': 1.0})
blocker = SimpleBlocker(lambda e: e.attributes['brand'].lower())

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
    Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}),
    Entity("3", {"title": "iPhone 11", "description": "Previous generation Apple smartphone", "brand": "Apple"}),
    Entity("4", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}),
    Entity("5", {"title": "Galaxy S21 Ultra", "description": "Samsung's premium flagship phone", "brand": "Samsung"}),
    Entity("6", {"title": "Pixel 5", "description": "Google's latest smartphone", "brand": "Google"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity("7", {"title": "iPhone 12 Pro Max", "description": "Apple's largest premium smartphone", "brand": "Apple"}),
    Entity("8", {"title": "Galaxy S21+", "description": "Samsung's large screen flagship", "brand": "Samsung"}),
]

# Resolve entities
results = resolver.resolve(new_entities)

# Print results
for entity, matches in results:
    print(f"Top matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches[:2]:  # Limiting to top 2 matches
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
    print()
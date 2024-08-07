from rezolva import (Entity, EntityResolver, SimpleBlocker, SimpleModelBuilder,
                     SimplePreprocessor)
from rezolva.clusters.hierarchical_cluster import HierarchicalCluster
from rezolva.matchers import CosineSimilarityMatcher
from rezolva.preprocessors.preprocessing_functions import (lowercase,
                                                           remove_punctuation,
                                                           strip_whitespace)

# Set up components
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleModelBuilder(["title", "description", "brand"])
clustering_algorithm = HierarchicalCluster(threshold=0.2)  # Adjust threshold as needed
matcher = CosineSimilarityMatcher(
    threshold=0.5,
    attribute_weights={"title": 2.0, "description": 1.5, "brand": 1.0},
    clustering_algorithm=clustering_algorithm,
)
blocker = SimpleBlocker(lambda e: e.attributes["brand"].lower())

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
    Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}),
    Entity("3", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}),
    Entity("4", {"title": "Pixel 5", "description": "Google's latest smartphone", "brand": "Google"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity("5", {"title": "iPhone 12 Pro Max", "description": "Apple's largest premium smartphone", "brand": "Apple"}),
    Entity("6", {"title": "Galaxy S21+", "description": "Samsung's large screen flagship", "brand": "Samsung"}),
]

# Resolve entities
results = resolver.resolve(new_entities, top_k=2)

# Print results
for entity, matches in results:
    print(f"Matches for {entity.id} - {entity.attributes['title']}:")
    for i in range(0, len(matches), 2):  # Step by 2 to get Entity-score pairs
        match_entity = matches[i]
        score = matches[i + 1]
        print(f"  Match: {match_entity.id} - {match_entity.attributes['title']} (Score: {score:.2f})")
    print()

# Additional example to show clustering effect
print("Demonstrating clustering effect:")
test_entity = Entity("7", {"title": "iPhone 13", "description": "Next generation Apple smartphone", "brand": "Apple"})
test_results = resolver.resolve([test_entity], top_k=4)  # Increase top_k to see more matches

for entity, matches in test_results:
    print(f"Matches for {entity.id} - {entity.attributes['title']}:")
    for i in range(0, len(matches), 2):  # Step by 2 to get Entity-score pairs
        match_entity = matches[i]
        score = matches[i + 1]
        print(f"  Match: {match_entity.id} - {match_entity.attributes['title']} (Score: {score:.2f})")
    print()

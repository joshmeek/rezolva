from tiny_er import EntityResolver, Entity
from tiny_er.preprocessors.simple_preprocessor import SimplePreprocessor
from tiny_er.preprocessors.preprocessing_functions import lowercase, strip_whitespace, remove_punctuation
from tiny_er.model_builders.simple_vector_model_builder import SimpleVectorModelBuilder
from tiny_er.matchers.cosine_similarity_matcher import CosineSimilarityMatcher
from tiny_er.blockers.simple_blocker import SimpleBlocker
from typing import List, Tuple, Dict
import math

# Set up components
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleVectorModelBuilder(['title', 'description', 'category'])
matcher = CosineSimilarityMatcher(threshold=0.5)
blocker = SimpleBlocker(lambda e: e.attributes['category'])

# Create the resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Sample training data
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "category": "Electronics"}),
    Entity("2", {"title": "Samsung Galaxy S21", "description": "Powerful Android phone", "category": "Electronics"}),
    Entity("3", {"title": "MacBook Pro", "description": "High-performance laptop", "category": "Electronics"}),
    Entity("4", {"title": "Desk Lamp", "description": "Adjustable LED lamp", "category": "Home & Office"}),
    Entity("5", {"title": "Office Chair", "description": "Ergonomic chair for work", "category": "Home & Office"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity("6", {"title": "iPhone 13", "description": "Next-gen Apple smartphone", "category": "Electronics"}),
    Entity("7", {"title": "Standing Desk", "description": "Adjustable height desk for office", "category": "Home & Office"}),
]

# Resolve entities
results = resolver.resolve(new_entities)

# Print results
for entity, matches in results:
    print(f"Matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches:
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
    print()

# Function to inspect the vector representation of an entity
def inspect_vector(entity_id: str, model: Dict):
    if entity_id in model['vectors']:
        print(f"Vector representation for entity {entity_id}:")
        for term, value in sorted(model['vectors'][entity_id].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {term}: {value:.4f}")
    else:
        print(f"No vector found for entity {entity_id}")

# Inspect vectors of trained entities
print("Inspecting vectors of trained entities:")
for entity_id in ["1", "4"]:
    inspect_vector(entity_id, resolver.model)
    print()

# Inspect vectors of new entities
print("Inspecting vectors of new entities:")
for new_entity in new_entities:
    new_vector = matcher._vectorize_entity(new_entity, resolver.model)
    print(f"Vector representation for new entity {new_entity.id}:")
    for term, value in sorted(new_vector.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {term}: {value:.4f}")
    print()

# Demonstrate matching a new entity against the model
print("Demonstrating direct matching of a new entity:")
new_entity = Entity("8", {"title": "Smart TV", "description": "4K Ultra HD Smart LED TV", "category": "Electronics"})
matches = matcher.match(new_entity, resolver.model)
print(f"Matches for new entity {new_entity.id} - {new_entity.attributes['title']}:")
for match, score in matches:
    print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
from rezolva import (Entity, EntityResolver, SimpleBlocker,
                      SimpleModelBuilder, SimplePreprocessor)
from rezolva.matchers import CosineSimilarityMatcher
from rezolva.preprocessors.preprocessing_functions import (lowercase,
                                                            remove_punctuation,
                                                            strip_whitespace)
from rezolva.utils.visualization import visualize_resolution_process

# Set up a sample resolver
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleModelBuilder(["title", "description", "brand"])
matcher = CosineSimilarityMatcher(threshold=0.5, attribute_weights={"title": 2.0, "description": 1.5, "brand": 1.0})
blocker = SimpleBlocker(lambda e: e.attributes["brand"].lower())
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Sample entities
entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
    Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}),
    Entity("3", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}),
]

# Train the resolver
resolver.train(entities)

# Visualize resolution process for a new entity
new_entity = Entity("4", {"title": "iPhone 12 Max", "description": "Apple's largest smartphone", "brand": "Apple"})
visualization = visualize_resolution_process(resolver, new_entity)
print(visualization)

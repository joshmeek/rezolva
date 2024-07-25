import pickle

from rezolva import (Entity, EntityResolver, SimpleBlocker, SimpleModelBuilder,
                     SimplePreprocessor)
from rezolva.matchers import CosineSimilarityMatcher
from rezolva.preprocessors.preprocessing_functions import (lowercase,
                                                           remove_punctuation,
                                                           strip_whitespace)


def create_resolver():
    preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
    model_builder = SimpleModelBuilder(["title", "description", "brand"])
    matcher = CosineSimilarityMatcher(threshold=0.5, attribute_weights={"title": 2.0, "description": 1.5, "brand": 1.0})
    blocker = SimpleBlocker(lambda e: e.attributes["brand"].lower())
    return EntityResolver(preprocessor, model_builder, matcher, blocker)


def save_model(resolver, filename):
    with open(filename, "wb") as f:
        pickle.dump(resolver.model, f)


def load_model(resolver, filename):
    with open(filename, "rb") as f:
        resolver.model = pickle.load(f)


# Create and train the resolver
resolver = create_resolver()
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
    Entity("2", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}),
    Entity("3", {"title": "Pixel 5", "description": "Google's latest smartphone", "brand": "Google"}),
]
resolver.train(training_entities)

# Save the model
save_model(resolver, "er_model.pkl")

# Create a new resolver and load the saved model
new_resolver = create_resolver()
load_model(new_resolver, "er_model.pkl")

# Test the loaded model
new_entity = Entity("4", {"title": "iPhone 12 Pro", "description": "Apple's premium smartphone", "brand": "Apple"})
results = new_resolver.resolve([new_entity])

# Print results
for entity, matches in results:
    print(f"Top matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches[:2]:
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")

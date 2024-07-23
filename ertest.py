from tiny_er.core.resolver import EntityResolver
from tiny_er.core.base import Entity
from tiny_er.preprocessors.simple_preprocessor import SimplePreprocessor
from tiny_er.model_builders.simple_model_builder import SimpleModelBuilder
from tiny_er.matchers.jaccard_matcher import JaccardMatcher
from tiny_er.blockers.simple_blocker import SimpleBlocker

# # Set up components
# preprocessor = SimplePreprocessor()
# model_builder = SimpleModelBuilder(['name', 'email', 'phone'])
# matcher = JaccardMatcher(threshold=0.3)
# blocker = SimpleBlocker(lambda e: e.attributes['name'][0].lower())

# # Create resolver
# resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# # Training data
training_entities = [
    Entity("1", {"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"}),
    Entity("2", {"name": "Jane Smith", "email": "jane@example.com", "phone": "987-654-3210"}),
    Entity("3", {"name": "Robert Johnson", "email": "robert@example.com", "phone": "456-789-0123"}),
    Entity("4", {"name": "Sarah Williams", "email": "sarah@example.com", "phone": "789-012-3456"}),
]

# # Train the resolver
# resolver.train(training_entities)

# # New entities to resolve
new_entities = [
    Entity("5", {"name": "Jon Doe", "email": "john@gmail.com", "phone": "123-456-7890"}),
    Entity("6", {"name": "Jane Smith", "email": "jsmith@example.com", "phone": "987-654-3210"}),
    Entity("7", {"name": "Bob Johnson", "email": "robert@example.com", "phone": "456-789-0123"}),
    Entity("8", {"name": "Sarah W.", "email": "swilliams@example.com", "phone": "789-012-3456"}),
    Entity("9", {"name": "Alice Brown", "email": "alice@example.com", "phone": "234-567-8901"}),
]

# # Resolve entities
# results = resolver.resolve(new_entities)

# for entity, matches in results:
#     print(f"Matches for {entity.id} - {entity.attributes['name']}:")
#     for match, score in matches:
#         print(f"  Match: {match.id} - {match.attributes['name']} (Score: {score:.2f})")
#     print()

import re
from typing import List, Dict, Any, Tuple
from tiny_er.core.base import Preprocessor, ModelBuilder, Matcher, Entity

class EnhancedPreprocessor(Preprocessor):
    def preprocess(self, entity: Entity) -> Entity:
        processed_attributes = {}
        for key, value in entity.attributes.items():
            if isinstance(value, str):
                # Convert to lowercase, remove punctuation, and normalize whitespace
                value = re.sub(r'[^\w\s]', '', value.lower())
                value = ' '.join(value.split())
                # Handle common nicknames
                if key == 'name':
                    value = self._normalize_name(value)
            processed_attributes[key] = value
        return Entity(entity.id, processed_attributes)

    def _normalize_name(self, name):
        nickname_map = {
            'bob': 'robert', 'rob': 'robert', 'bobby': 'robert',
            'jim': 'james', 'jimmy': 'james', 'jamie': 'james',
            'john': 'jonathan', 'jon': 'jonathan',
            'bill': 'william', 'will': 'william',
            'tom': 'thomas', 'tommy': 'thomas',
        }
        parts = name.split()
        if parts[0] in nickname_map:
            parts[0] = nickname_map[parts[0]]
        return ' '.join(parts)

class EnhancedModelBuilder(ModelBuilder):
    def __init__(self, attributes: List[str], weights: Dict[str, float] = None):
        self.attributes = attributes
        self.weights = weights or {attr: 1.0 for attr in attributes}

    def train(self, entities: List[Entity]) -> Any:
        model = {'entities': {}, 'index': {}}
        for entity in entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                value = entity.attributes.get(attr, '').lower()
                if value:
                    if attr not in model['index']:
                        model['index'][attr] = {}
                    for token in value.split():
                        if token not in model['index'][attr]:
                            model['index'][attr][token] = set()
                        model['index'][attr][token].add(entity.id)
        return model

    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        for entity in new_entities:
            model['entities'][entity.id] = entity
            for attr in self.attributes:
                value = entity.attributes.get(attr, '').lower()
                if value:
                    if attr not in model['index']:
                        model['index'][attr] = {}
                    for token in value.split():
                        if token not in model['index'][attr]:
                            model['index'][attr][token] = set()
                        model['index'][attr][token].add(entity.id)
        return model

class EnhancedJaccardMatcher(Matcher):
    def __init__(self, threshold: float = 0.3, weights: Dict[str, float] = None):
        self.threshold = threshold
        self.weights = weights or {}

    def match(self, entity: Entity, model: Dict) -> List[Tuple[Entity, float]]:
        candidate_ids = set()
        for attr in model['index']:
            value = entity.attributes.get(attr, '').lower()
            for token in value.split():
                if token in model['index'][attr]:
                    candidate_ids.update(model['index'][attr][token])
        
        matches = []
        for candidate_id in candidate_ids:
            if candidate_id != entity.id:
                candidate = model['entities'][candidate_id]
                similarity = self._calculate_weighted_similarity(entity, candidate)
                if similarity >= self.threshold:
                    matches.append((candidate, similarity))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_weighted_similarity(self, entity1: Entity, entity2: Entity) -> float:
        total_weight = 0
        weighted_similarity = 0
        for attr in set(entity1.attributes.keys()) | set(entity2.attributes.keys()):
            weight = self.weights.get(attr, 1.0)
            total_weight += weight
            value1 = str(entity1.attributes.get(attr, '')).lower()
            value2 = str(entity2.attributes.get(attr, '')).lower()
            similarity = self._token_based_jaccard(value1, value2)
            weighted_similarity += weight * similarity
        return weighted_similarity / total_weight if total_weight > 0 else 0

    def _token_based_jaccard(self, s1: str, s2: str) -> float:
        set1 = set(s1.split())
        set2 = set(s2.split())
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0

# Update the EntityResolver to use these enhanced components
class EnhancedEntityResolver:
    def __init__(self, preprocessor, model_builder, matcher, blocker):
        self.preprocessor = preprocessor
        self.model_builder = model_builder
        self.matcher = matcher
        self.blocker = blocker
        self.model = None

    def train(self, entities: List[Entity]):
        preprocessed_entities = [self.preprocessor.preprocess(e) for e in entities]
        self.model = self.model_builder.train(preprocessed_entities)

    def resolve(self, entities: List[Entity]) -> List[Tuple[Entity, List[Tuple[Entity, float]]]]:
        if not self.model:
            raise ValueError("Model not trained. Call train() first.")
        
        preprocessed_entities = [self.preprocessor.preprocess(e) for e in entities]
        results = []
        for entity in preprocessed_entities:
            matches = self.matcher.match(entity, self.model)
            if matches:
                results.append((entity, matches))
        
        return results

    def update_model(self, new_entities: List[Entity]):
        preprocessed_entities = [self.preprocessor.preprocess(e) for e in new_entities]
        self.model = self.model_builder.update(self.model, preprocessed_entities)

# Example usage
weights = {'name': 2.0, 'email': 1.5, 'phone': 1.0}
preprocessor = EnhancedPreprocessor()
model_builder = EnhancedModelBuilder(['name', 'email', 'phone'], weights)
matcher = EnhancedJaccardMatcher(threshold=0.4, weights=weights)
blocker = SimpleBlocker(lambda e: e.attributes['name'][0].lower())

resolver = EnhancedEntityResolver(preprocessor, model_builder, matcher, blocker)

# Use the same training_entities and new_entities as before
resolver.train(training_entities)
results = resolver.resolve(new_entities)

print("Enhanced Resolution Results:")
for entity, matches in results:
    print(f"Matches for {entity.id} - {entity.attributes['name']}:")
    if matches:
        for match, score in matches:
            print(f"  Match: {match.id} - {match.attributes['name']} (Score: {score:.2f})")
    else:
        print("  No matches found")
    print()
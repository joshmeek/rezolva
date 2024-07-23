# Tiny ER

**Minimalist entity resolution. No dependencies. Pure Python.**

Tiny ER is a lightweight, flexible, and extensible entity resolution library implemented in pure Python. It's designed for simplicity, educational purposes, and easy integration into larger projects.

## Features

- Zero dependencies: Built with Python standard library only
- Modular architecture: Easy to customize and extend
- Educational: Clear implementation of ER concepts
- Flexible: Adaptable to various ER scenarios

## Installation

```bash
pip install tiny-er
```

## Quick Start

Here's a simple example of how to use Tiny ER:

```python
from tiny_er import EntityResolver, Entity, SimplePreprocessor, SimpleModelBuilder, JaccardMatcher, SimpleBlocker

# Set up components
preprocessor = SimplePreprocessor()
model_builder = SimpleModelBuilder(['name', 'email', 'phone'])
matcher = JaccardMatcher(threshold=0.5)
blocker = SimpleBlocker(lambda e: e.attributes['name'][0].lower())

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity("1", {"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"}),
    Entity("2", {"name": "Jane Smith", "email": "jane@example.com", "phone": "987-654-3210"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity("3", {"name": "Jon Doe", "email": "john@gmail.com", "phone": "123-456-7890"}),
    Entity("4", {"name": "Jane Smith", "email": "jsmith@example.com", "phone": "987-654-3210"}),
]

# Resolve entities
results = resolver.resolve(new_entities)

# Print results
for entity, matches in results:
    print(f"Matches for {entity.id} - {entity.attributes['name']}:")
    for match, score in matches:
        print(f"  Match: {match.id} - {match.attributes['name']} (Score: {score:.2f})")
    print()
```

## Advanced Usage: Enhanced Modular Design

Tiny ER's modular design allows for easy customization and extension. Here's an example of how to create and use enhanced components:

```python
from tiny_er import Entity, Preprocessor, ModelBuilder, Matcher, SimpleBlocker
from tiny_er.core.resolver import EntityResolver
import re

class EnhancedPreprocessor(Preprocessor):
    def preprocess(self, entity: Entity) -> Entity:
        processed_attributes = {}
        for key, value in entity.attributes.items():
            if isinstance(value, str):
                value = re.sub(r'[^\w\s]', '', value.lower())
                value = ' '.join(value.split())
                if key == 'name':
                    value = self._normalize_name(value)
            processed_attributes[key] = value
        return Entity(entity.id, processed_attributes)

    def _normalize_name(self, name):
        nickname_map = {'bob': 'robert', 'rob': 'robert', 'jim': 'james', 'john': 'jonathan', 'jon': 'jonathan'}
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
        # Similar to train, but updates existing model
        ...

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
        # Implement weighted Jaccard similarity
        ...

# Usage of enhanced components
weights = {'name': 2.0, 'email': 1.5, 'phone': 1.0}
preprocessor = EnhancedPreprocessor()
model_builder = EnhancedModelBuilder(['name', 'email', 'phone'], weights)
matcher = EnhancedJaccardMatcher(threshold=0.4, weights=weights)
blocker = SimpleBlocker(lambda e: e.attributes['name'][0].lower())

resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Use resolver as in the basic example
...
```

## Key Components

1. **Preprocessor**: Cleans and standardizes entity attributes.
2. **ModelBuilder**: Creates and updates the matching model.
3. **Matcher**: Computes similarity between entities and finds matches.
4. **Blocker**: Groups similar entities to reduce comparison space.

Each component has a base abstract class that can be extended to create custom implementations.

## Customization

You can easily extend Tiny ER by creating custom implementations of its components:

1. Subclass the base component classes (`Preprocessor`, `ModelBuilder`, `Matcher`, `Blocker`).
2. Implement the required methods with your custom logic.
3. Use your custom components when creating the `EntityResolver`.

## Contributing

Contributions to Tiny ER are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

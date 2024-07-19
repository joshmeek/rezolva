# tiny_er

Minimalist entity resolution. No dependencies. Pure Python.

## Ethos

- **Tiny**: Entire library in <1000 lines of code
- **Zero Dependencies**: Built with Python standard library only
- **Simplicity**: Clean API. Easy to understand, use, and modify
- **Educational**: Clear implementation of ER concepts
- **Flexible**: Adaptable to various ER scenarios

## Features

- Preprocessing & normalization
- Blocking strategies
- Similarity measures
- Rule-based & probabilistic matching
- Evaluation metrics
- Customizable

## Quick Start

```python
from tiny_er.core.entity_resolver import EntityResolver
from tiny_er.core.config import get_config
from tiny_er.core.data_structures import Entity
from tiny_er.preprocessing.normalizer import create_normalizer
from tiny_er.blocking.standard_blocking import create_blocker
from tiny_er.similarity.string_similarity import create_similarity_measure
from tiny_er.matching.rule_based import create_matcher

# Sample data
entities = [
    Entity("1", {"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"}),
    Entity("2", {"name": "Jane Doe", "email": "jane@example.com", "phone": "987-654-3210"}),
    Entity("3", {"name": "J. Doe", "email": "john@example.com", "phone": "123-456-7890"}),
    Entity("4", {"name": "Jane Smith", "email": "jane@example.com", "phone": "555-555-5555"}),
    Entity("5", {"name": "John Smith", "email": "johnsmith@example.com", "phone": "111-222-3333"})
]

# Configuration
config = get_config()
config['preprocessing'] = {'lowercase': True, 'remove_punctuation': True, 'remove_whitespace': True}
config['blocking'] = {'method': 'standard', 'block_key': 'name'}
config['similarity'] = {'method': 'jaccard', 'threshold': 0.3}
config['matching'] = {'method': 'threshold', 'threshold': 0.3}

# Create EntityResolver
resolver = EntityResolver(
    create_normalizer(config['preprocessing']),
    create_blocker(config['blocking']),
    create_similarity_measure(config['similarity']),
    create_matcher(config['matching'])
)

# Resolve entities
resolved_entities = resolver.resolve(entities)

# Print results
print("Resolved Entities:")
for entity in resolved_entities:
    print(f"Resolved ID: {entity.id}")
    print(f"Original IDs: {entity.original_ids}")
    print(f"Attributes: {entity.attributes}")
    print("---")
```

## Evaluation

```python
from tiny_er.evaluation.metrics import evaluate
from tiny_er.evaluation.cross_validation import k_fold_cross_validation
from tiny_er.core.data_structures import MatchResult, Entity

# Using entities and resolver from the previous example

# Create true matches (ground truth)
true_matches = [
    ('1', '3'),  # John Doe and J. Doe are the same person
    ('2', '4')   # Jane Doe and Jane Smith are the same person
]

# Perform entity resolution
resolved_entities = resolver.resolve(entities)

# Create predicted matches from resolved entities
def create_match_results(resolved_entities):
    predicted_matches = []
    for resolved_entity in resolved_entities:
        original_ids = resolved_entity.original_ids
        for i in range(len(original_ids)):
            for j in range(i + 1, len(original_ids)):
                predicted_matches.append(
                    MatchResult(
                        entity1=Entity(id=original_ids[i], attributes={}),
                        entity2=Entity(id=original_ids[j], attributes={}),
                        confidence=1.0,
                        is_match=True
                    )
                )
    return predicted_matches

predicted_matches = create_match_results(resolved_entities)

# Basic evaluation
metrics = evaluate(true_matches, predicted_matches, config={'metrics': ['precision', 'recall', 'f1_score']})

print("Evaluation Metrics:")
for metric, value in metrics.items():
    print(f"{metric}: {value:.2f}")

# Cross-validation
def resolver_function(entities):
    resolved_entities = resolver.resolve(entities)
    return create_match_results(resolved_entities)

cv_results = k_fold_cross_validation(entities, resolver_function, true_matches, k=5)

print("\nCross-validation Results:")
for metric, value in cv_results.items():
    print(f"{metric}: {value:.2f}")
```

## Customize

Extend base classes to create custom components:

```python
from tiny_er.core.entity_resolver import EntityResolver
from tiny_er.core.config import get_config
from tiny_er.core.data_structures import Entity, Block
from tiny_er.core.base_classes import Blocker
from tiny_er.preprocessing.normalizer import create_normalizer
from tiny_er.similarity.string_similarity import create_similarity_measure
from tiny_er.matching.rule_based import create_matcher

class MultiFieldBlocker(Blocker):
    def __init__(self, blocking_fields):
        self.blocking_fields = blocking_fields

    def block(self, entities):
        blocks = {}
        for entity in entities:
            block_key = self._create_block_key(entity)
            if block_key not in blocks:
                blocks[block_key] = Block(block_key)
            blocks[block_key].add(entity)
        return list(blocks.values())

    def _create_block_key(self, entity):
        key_parts = []
        for field in self.blocking_fields:
            value = entity.attributes.get(field, '')
            key_parts.append(value[:1].lower() if value else '_')
        return ''.join(key_parts)

# Sample data
entities = [
    Entity("1", {"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890", "city": "New York"}),
    Entity("2", {"name": "Jane Doe", "email": "jane@example.com", "phone": "987-654-3210", "city": "Los Angeles"}),
    Entity("3", {"name": "J. Doe", "email": "john@example.com", "phone": "123-456-7890", "city": "New York"}),
    Entity("4", {"name": "Jane Smith", "email": "janes@example.com", "phone": "555-555-5555", "city": "Chicago"}),
    Entity("5", {"name": "John Smith", "email": "johns@example.com", "phone": "111-222-3333", "city": "New York"})
]

# Configuration
config = get_config()
config['preprocessing'] = {'lowercase': True, 'remove_punctuation': True, 'remove_whitespace': True}
config['similarity'] = {'method': 'jaccard', 'threshold': 0.7}
config['matching'] = {'method': 'threshold', 'threshold': 0.7}

# Create custom blocker
custom_blocker = MultiFieldBlocker(blocking_fields=['name', 'city'])

# Create EntityResolver with custom blocker
resolver = EntityResolver(
    create_normalizer(config['preprocessing']),
    custom_blocker,
    create_similarity_measure(config['similarity']),
    create_matcher(config['matching'])
)

# Resolve entities
resolved_entities = resolver.resolve(entities)

# Print results
print("Resolved Entities:")
for entity in resolved_entities:
    print(f"Resolved ID: {entity.id}")
    print(f"Original IDs: {entity.original_ids}")
    print(f"Attributes: {entity.attributes}")
    print("---")

# Evaluate results
from tiny_er.evaluation.metrics import evaluate
from tiny_er.core.data_structures import MatchResult

true_matches = [
    ('1', '3'),  # John Doe and J. Doe are the same person
    ('2', '4')   # Jane Doe and Jane Smith are the same person (this won't be caught due to different cities)
]

predicted_matches = [
    MatchResult(Entity(id1, {}), Entity(id2, {}), 1.0, True)
    for resolved_entity in resolved_entities
    for id1 in resolved_entity.original_ids
    for id2 in resolved_entity.original_ids
    if id1 < id2
]

metrics = evaluate(true_matches, predicted_matches, config={'metrics': ['precision', 'recall', 'f1_score']})

print("\nEvaluation Metrics:")
for metric, value in metrics.items():
    print(f"{metric}: {value:.2f}")
```

## Why tiny_er?

- **Learning**: Understand ER without the complexity of large libraries
- **Prototyping**: Quickly implement and test ER ideas
- **Embedding**: Easily integrate into larger projects
- **Customization**: Modify the core logic to fit specific needs

## License

MIT

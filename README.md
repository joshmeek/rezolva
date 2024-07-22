# tiny_er

Minimalist entity resolution. No dependencies. Pure Python.

## Ethos

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
resolver = EntityResolver(config=config)

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
from tiny_er.core.data_structures import Entity, Block, MatchResult, Comparison
from tiny_er.core.base_classes import Blocker, Matcher
from tiny_er.preprocessing.normalizer import create_normalizer
from tiny_er.similarity.vector_similarity import create_vector_similarity_measure

class ImprovedProfessionBlocker(Blocker):
    def __init__(self, profession_field):
        self.profession_field = profession_field

    def block(self, entities):
        blocks = {
            'tech': Block('tech'),
            'data': Block('data'),
            'other': Block('other')
        }
        for entity in entities:
            profession = entity.attributes.get(self.profession_field, '').lower()
            if 'engineer' in profession or 'developer' in profession:
                blocks['tech'].add(entity)
            elif 'scientist' in profession or 'analyst' in profession:
                blocks['data'].add(entity)
            else:
                blocks['other'].add(entity)
        return list(blocks.values())

class ThresholdMatcher(Matcher):
    def __init__(self, threshold):
        self.threshold = threshold

    def match(self, comparisons):
        return [MatchResult(comparison.entity1, comparison.entity2, comparison.similarity, comparison.similarity >= self.threshold)
                for comparison in comparisons]

# Sample data
entities = [
    Entity("1", {"name": "John Doe", "email": "john@example.com", "profession": "Software Engineer", "bio": "Experienced software developer with 5 years in the field"}),
    Entity("2", {"name": "Jane Doe", "email": "jane@example.com", "profession": "Data Scientist", "bio": "Data scientist specializing in machine learning and AI"}),
    Entity("3", {"name": "J. Doe", "email": "jdoe@example.com", "profession": "Software Developer", "bio": "Full-stack developer with expertise in web technologies"}),
    Entity("4", {"name": "Jane Smith", "email": "janes@example.com", "profession": "Data Analyst", "bio": "Data analyst with strong statistical background"}),
    Entity("5", {"name": "John Smith", "email": "johns@example.com", "profession": "Project Manager", "bio": "IT project manager with 10 years of experience"})
]

# Configuration
config = get_config()
config['preprocessing'] = {'lowercase': True, 'remove_punctuation': True, 'remove_whitespace': True}
config['similarity'] = {
    'method': 'cosine',
    'fields': ['name', 'profession', 'bio'],
    'threshold': 0.3
}
config['matching'] = {'threshold': 0.3}
config['evaluation'] = {'metrics': ['precision', 'recall', 'f1_score']}

# Create components
preprocessor = create_normalizer(config['preprocessing'])
blocker = ImprovedProfessionBlocker(profession_field='profession')
similarity_measure = create_vector_similarity_measure(config['similarity'])
matcher = ThresholdMatcher(config['matching']['threshold'])

# Create EntityResolver
resolver = EntityResolver(
    preprocessor=preprocessor,
    blocker=blocker,
    similarity_measure=similarity_measure,
    matcher=matcher
)

# Resolve entities
resolved_entities = resolver.resolve(entities)

print("Resolved Entities:")
for entity in resolved_entities:
    print(f"Resolved ID: {entity.id}")
    print(f"Original IDs: {entity.original_ids}")
    print(f"Attributes: {entity.attributes}")
    print("---")

# Evaluate results
from tiny_er.evaluation.metrics import evaluate

true_matches = [
    ('1', '3'),  # John Doe and J. Doe are both software developers
    ('2', '4')   # Jane Doe and Jane Smith are both in data-related professions
]

predicted_matches = create_match_results(resolved_entities)
metrics = evaluate(true_matches, predicted_matches, config['evaluation'])

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

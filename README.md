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
from tiny_er.preprocessing.normalizer import create_normalizer
from tiny_er.blocking.standard_blocking import create_blocker
from tiny_er.similarity.string_similarity import create_similarity_measure
from tiny_er.matching.rule_based import create_matcher
from tiny_er.utils.data_loader import load_csv, save_results

# Setup
config = get_config()
resolver = EntityResolver(
    create_normalizer(config['preprocessing']),
    create_blocker(config['blocking']),
    create_similarity_measure(config['similarity']),
    create_matcher(config['matching'])
)

# Resolve
entities = load_csv('data.csv', id_column='id')
results = resolver.resolve(entities)

# Save
output = [{
    'cluster_id': id(cluster),
    'entity_id': entity.id,
    'attributes': entity.attributes
} for cluster in results for entity in cluster]
save_results('output.csv', output)
```

## Evaluation

```python
from tiny_er.evaluation.metrics import evaluate
from tiny_er.evaluation.cross_validation import k_fold_cross_validation

# Basic evaluation
metrics = evaluate(true_matches, predicted_matches, config={'metrics': ['precision', 'recall', 'f1_score']})

# Cross-validation
cv_results = k_fold_cross_validation(entities, resolver.resolve, true_matches, k=5)
```

## Customize

Extend base classes to create custom components:

```python
from tiny_er.core.base_classes import Blocker

class MyBlocker(Blocker):
    def block(self, entities):
        # Custom blocking logic
        pass

resolver = EntityResolver(normalizer, MyBlocker(), similarity_measure, matcher)
```

## Why tiny_er?

- **Learning**: Understand ER without the complexity of large libraries
- **Prototyping**: Quickly implement and test ER ideas
- **Embedding**: Easily integrate into larger projects
- **Customization**: Modify the core logic to fit specific needs

## License

MIT

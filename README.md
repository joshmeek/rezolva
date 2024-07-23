# start-er

**Entity resolution for everyone. Minimal. No Dependencies.**

_**start-er**_ is a lightweight, flexible, and extensible entity resolution library implemented in pure Python. It's designed for simplicity, educational purposes, and easy integration into larger projects.

## Features

- Zero dependencies: Built with Python standard library only
- Modular architecture: Easy to customize and extend
- Defaults: Out-of-the-box implementations of ER algorithms
- Flexible: Adaptable to various ER scenarios

## Installation

```bash
pip install start-er
```

## Quick Start

Here's a simple example of how to use Tiny ER:

```python
from start_er import Entity, EntityResolver, SimpleBlocker, SimpleModelBuilder, SimplePreprocessor
from start_er.matchers import CosineSimilarityMatcher
from start_er.preprocessors.preprocessing_functions import lowercase, strip_whitespace, remove_punctuation

# Set up components
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleModelBuilder(['title', 'description', 'brand'])
matcher = CosineSimilarityMatcher(threshold=0.5, attribute_weights={'title': 2.0, 'description': 1.5, 'brand': 1.0})
blocker = SimpleBlocker(lambda e: e.attributes['brand'].lower())

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Train the resolver
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
    Entity("2", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}),
    Entity("3", {"title": "Pixel 5", "description": "Google's latest smartphone", "brand": "Google"}),
]
resolver.train(training_entities)

# Resolve new entities
new_entities = [
    Entity("4", {"title": "iPhone 12 Pro", "description": "Apple's premium smartphone", "brand": "Apple"}),
    Entity("5", {"title": "Galaxy S21+", "description": "Samsung's large screen flagship", "brand": "Samsung"}),
]
results = resolver.resolve(new_entities, top_k=1)

# Print results
for entity, matches in results:
    print(f"Top matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches[:2]:
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
```

## Advanced Usage

For more advanced examples, including custom preprocessing, different matching algorithms, and model saving/loading, please check the [`examples`](https://github.com/joshmeek/start-er/tree/main/examples) directory in the repository.

## Customization

You can extend Tiny ER by creating custom implementations of its components:

1. Subclass the base component classes (`Preprocessor`, `ModelBuilder`, `Matcher`, `Blocker`)
2. Implement the required methods with your custom logic
3. Use your custom components when creating the `EntityResolver`

## Contributing

Contributions to Tiny ER are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

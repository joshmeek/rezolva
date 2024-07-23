# Tiny ER

**Minimalist entity resolution. No dependencies. Pure Python.**

Tiny ER is a lightweight, flexible, and extensible entity resolution library implemented in pure Python. It's designed for simplicity, educational purposes, and easy integration into larger projects.

## Features

- Zero dependencies: Built with Python standard library only
- Modular architecture: Easy to customize and extend
- Educational: Clear implementation of ER concepts
- Flexible: Adaptable to various ER scenarios
- Customizable preprocessing pipeline
- Multiple matching algorithms
- Configurable attribute weighting
- Top-K results

## Installation

```bash
pip install tiny-er
```

## Quick Start

Here's a simple example of how to use Tiny ER:

```python
from tiny_er import EntityResolver, Entity, SimplePreprocessor, SimpleModelBuilder, SimpleBlocker
from tiny_er.matchers import CosineSimilarityMatcher
from tiny_er.preprocessors.preprocessing_functions import lowercase, strip_whitespace, remove_punctuation

# Set up components
preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
model_builder = SimpleModelBuilder(['title', 'description', 'brand'])
matcher = CosineSimilarityMatcher(threshold=0.5, attribute_weights={'title': 2.0, 'description': 1.5, 'brand': 1.0})
blocker = SimpleBlocker(lambda e: e.attributes['brand'].lower())

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
    Entity("2", {"title": "iPhone 12 Pro", "description": "Premium Apple smartphone", "brand": "Apple"}),
    Entity("3", {"title": "iPhone 11", "description": "Previous generation Apple smartphone", "brand": "Apple"}),
    Entity("4", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}),
    Entity("5", {"title": "Galaxy S21 Ultra", "description": "Samsung's premium flagship phone", "brand": "Samsung"}),
    Entity("6", {"title": "Pixel 5", "description": "Google's latest smartphone", "brand": "Google"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity("7", {"title": "iPhone 12 Pro Max", "description": "Apple's largest premium smartphone", "brand": "Apple"}),
    Entity("8", {"title": "Galaxy S21+", "description": "Samsung's large screen flagship", "brand": "Samsung"}),
]

# Resolve entities
results = resolver.resolve(new_entities, top_k=2)

# Print results
for entity, matches in results:
    print(f"Top 3 matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches:
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
    print()
```

## Advanced Usage

Tiny ER's modular design allows for easy customization and extension. Here's a more advanced example that demonstrates custom preprocessing, blocking, and matching for product data:

```python
from tiny_er import EntityResolver, Entity, SimplePreprocessor, SimpleModelBuilder, SimpleBlocker
from tiny_er.matchers import TfIdfMatcher
from tiny_er.preprocessors.preprocessing_functions import lowercase, strip_whitespace, remove_punctuation

# Custom preprocessing function
def extract_product_type(entity: Entity) -> Entity:
    title = str(entity.attributes.get('title', '')).lower()
    if 'phone' in title or 'smartphone' in title:
        product_type = 'phone'
    elif 'laptop' in title or 'notebook' in title:
        product_type = 'laptop'
    else:
        product_type = 'other'
    return Entity(entity.id, {**entity.attributes, 'product_type': product_type})

# Set up components
preprocessor = SimplePreprocessor([
    lowercase,
    strip_whitespace,
    remove_punctuation,
    extract_product_type
])

attribute_weights = {'title': 2.0, 'description': 1.5, 'brand': 1.0, 'product_type': 0.5}
model_builder = SimpleModelBuilder(list(attribute_weights.keys()))
matcher = TfIdfMatcher(threshold=0.6, attribute_weights=attribute_weights)
blocker = SimpleBlocker(lambda e: str(e.attributes.get('product_type', '')))

# Create resolver
resolver = EntityResolver(preprocessor, model_builder, matcher, blocker)

# Training data
training_entities = [
    Entity("1", {"title": "iPhone 12", "description": "Latest Apple smartphone", "brand": "Apple"}),
    Entity("2", {"title": "Galaxy S21", "description": "Samsung's flagship phone", "brand": "Samsung"}),
    Entity("3", {"title": "MacBook Pro", "description": "Powerful Apple laptop", "brand": "Apple"}),
    Entity("4", {"title": "Dell XPS 13", "description": "Compact high-performance notebook", "brand": "Dell"}),
]

# Train the resolver
resolver.train(training_entities)

# New entities to resolve
new_entities = [
    Entity("5", {"title": "iPhone 12 Pro", "description": "Apple's premium smartphone", "brand": "Apple"}),
    Entity("6", {"title": "Surface Laptop 4", "description": "Microsoft's sleek notebook", "brand": "Microsoft"}),
]

# Resolve entities
results = resolver.resolve(new_entities, top_k=2)

# Print results
for entity, matches in results:
    print(f"Top 2 matches for {entity.id} - {entity.attributes['title']}:")
    for match, score in matches:
        print(f"  Match: {match.id} - {match.attributes['title']} (Score: {score:.2f})")
    print()
```

This example demonstrates:

1. A custom preprocessing function to extract product type
2. Using TF-IDF matching with weighted attributes
3. Blocking based on the extracted product type
4. Resolving entities across different product categories

## Customization

You can easily extend Tiny ER by creating custom implementations of its components:

1. Subclass the base component classes (`Preprocessor`, `ModelBuilder`, `Matcher`, `Blocker`).
2. Implement the required methods with your custom logic.
3. Use your custom components when creating the `EntityResolver`.

## Contributing

Contributions to Tiny ER are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

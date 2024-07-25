import random
from typing import List, Tuple

from rezolva import (Entity, EntityResolver, SimpleBlocker,
                      SimpleModelBuilder, SimplePreprocessor)
from rezolva.core.base import Blocker, Matcher
from rezolva.matchers import CosineSimilarityMatcher
from rezolva.preprocessors.preprocessing_functions import (lowercase,
                                                            remove_punctuation,
                                                            strip_whitespace)
# Import the evaluation utilities
from rezolva.utils.evaluation import (cross_validate, evaluate_resolver,
                                       generate_performance_report,
                                       print_cross_validation_report)


# Custom components
class CustomBlocker(Blocker):
    def create_blocks(self, entities: List[Entity]) -> dict:
        blocks = {}
        for entity in entities:
            key = f"{entity.attributes['brand']}_{entity.attributes['category']}"
            if key not in blocks:
                blocks[key] = []
            blocks[key].append(entity)
        return blocks


class CustomMatcher(Matcher):
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def match(self, entity: Entity, model: dict) -> List[Tuple[Entity, float]]:
        matches = []
        for candidate_id, candidate in model["entities"].items():
            if candidate_id != entity.id:
                score = self._calculate_similarity(entity, candidate)
                if score >= self.threshold:
                    matches.append((candidate, score))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _calculate_similarity(self, entity1: Entity, entity2: Entity) -> float:
        title_sim = self._jaccard_similarity(entity1.attributes["title"], entity2.attributes["title"])
        desc_sim = self._jaccard_similarity(entity1.attributes["description"], entity2.attributes["description"])
        return (title_sim * 0.6) + (desc_sim * 0.4)

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0


# Generate sample data
def generate_sample_data(n: int = 100) -> Tuple[List[Entity], dict]:
    brands = ["Apple", "Samsung", "Google", "Sony", "LG"]
    categories = ["Smartphone", "Laptop", "Tablet", "TV", "Headphones"]
    entities = []
    ground_truth = {}

    for i in range(n):
        brand = random.choice(brands)
        category = random.choice(categories)
        title = f"{brand} {category} {random.randint(1, 10)}"
        description = f"A {category.lower()} made by {brand}"
        entity = Entity(str(i), {"title": title, "description": description, "brand": brand, "category": category})
        entities.append(entity)

        # Generate some similar entities for ground truth
        if random.random() < 0.3:  # 30% chance of having a match
            similar_entity = Entity(
                str(n + i),
                {
                    "title": f"{title} Pro",
                    "description": f"Premium {description.lower()}",
                    "brand": brand,
                    "category": category,
                },
            )
            entities.append(similar_entity)
            ground_truth[str(i)] = [str(n + i)]
            ground_truth[str(n + i)] = [str(i)]

    return entities, ground_truth


# Set up resolvers
def setup_simple_resolver():
    preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
    model_builder = SimpleModelBuilder(["title", "description", "brand", "category"])
    matcher = CosineSimilarityMatcher(
        threshold=0.5, attribute_weights={"title": 2.0, "description": 1.5, "brand": 1.0, "category": 0.5}
    )
    blocker = SimpleBlocker(lambda e: e.attributes["brand"].lower())
    return EntityResolver(preprocessor, model_builder, matcher, blocker)


def setup_custom_resolver():
    preprocessor = SimplePreprocessor([lowercase, strip_whitespace, remove_punctuation])
    model_builder = SimpleModelBuilder(["title", "description", "brand", "category"])
    matcher = CustomMatcher(threshold=0.3)
    blocker = CustomBlocker()
    return EntityResolver(preprocessor, model_builder, matcher, blocker)


# Main execution
if __name__ == "__main__":
    # Generate sample data
    entities, ground_truth = generate_sample_data(200)

    # Set up resolvers
    simple_resolver = setup_simple_resolver()
    custom_resolver = setup_custom_resolver()

    simple_resolver.train(entities)
    custom_resolver.train(entities)

    # Evaluate simple resolver
    print("Evaluating Simple Resolver")
    print("==========================")
    simple_metrics = evaluate_resolver(simple_resolver, entities, ground_truth)
    print(generate_performance_report(simple_metrics))

    print("\nCross-validation for Simple Resolver")
    simple_cv_results = cross_validate(simple_resolver, entities, ground_truth, k=5)
    print_cross_validation_report(simple_cv_results)

    print("\n\nEvaluating Custom Resolver")
    print("===========================")
    custom_metrics = evaluate_resolver(custom_resolver, entities, ground_truth)
    print(generate_performance_report(custom_metrics))

    print("\nCross-validation for Custom Resolver")
    custom_cv_results = cross_validate(custom_resolver, entities, ground_truth, k=5)
    print_cross_validation_report(custom_cv_results)

    # Compare results
    print("\nComparison of Simple vs Custom Resolver")
    print("=======================================")
    metrics = ["precision", "recall", "f1", "accuracy"]
    for metric in metrics:
        simple_value = simple_metrics[metric]
        custom_value = custom_metrics[metric]
        difference = custom_value - simple_value
        print(f"{metric.capitalize()}:")
        print(f"  Simple: {simple_value:.3f}")
        print(f"  Custom: {custom_value:.3f}")
        print(
            f"  Difference: {difference:.3f} ({'better' if difference > 0 else 'same' if difference == 0 else 'worse'} for Custom)"
        )
        print()

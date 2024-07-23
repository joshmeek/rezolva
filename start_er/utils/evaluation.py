import math
from typing import Dict, List, Tuple

from start_er import Entity, EntityResolver


def calculate_precision_recall_f1(true_positives: int, false_positives: int, false_negatives: int) -> Tuple[float, float, float]:
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

def calculate_accuracy(true_positives: int, true_negatives: int, total_comparisons: int) -> float:
    return (true_positives + true_negatives) / total_comparisons if total_comparisons > 0 else 0

def evaluate_resolver(resolver: EntityResolver, test_entities: List[Entity], ground_truth: Dict[str, List[str]], threshold: float = 0.5) -> Dict[str, float]:
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0
    total_comparisons = 0

    results = resolver.resolve(test_entities)

    for entity, matches in results:
        true_matches = set(ground_truth.get(entity.id, []))
        predicted_matches = set([match.id for match, score in matches if score >= threshold])

        true_positives += len(true_matches.intersection(predicted_matches))
        false_positives += len(predicted_matches - true_matches)
        false_negatives += len(true_matches - predicted_matches)
        true_negatives += len(set(e.id for e in test_entities) - true_matches - predicted_matches)
        total_comparisons += len(test_entities) - 1  # Exclude self-comparison

    precision, recall, f1 = calculate_precision_recall_f1(true_positives, false_positives, false_negatives)
    accuracy = calculate_accuracy(true_positives, true_negatives, total_comparisons)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy
    }

def generate_performance_report(metrics: Dict[str, float]) -> str:
    report = "Entity Resolution Performance Report\n"
    report += "===================================\n\n"
    report += f"Precision: {metrics['precision']:.3f}\n"
    report += f"Recall: {metrics['recall']:.3f}\n"
    report += f"F1 Score: {metrics['f1']:.3f}\n"
    report += f"Accuracy: {metrics['accuracy']:.3f}\n"
    return report

def cross_validate(resolver: EntityResolver, entities: List[Entity], ground_truth: Dict[str, List[str]], k: int = 5) -> Dict[str, List[float]]:
    fold_size = len(entities) // k
    results = {
        "precision": [],
        "recall": [],
        "f1": [],
        "accuracy": []
    }

    for i in range(k):
        start = i * fold_size
        end = start + fold_size if i < k - 1 else len(entities)

        test_entities = entities[start:end]
        fold_metrics = evaluate_resolver(resolver, test_entities, ground_truth)

        for metric, value in fold_metrics.items():
            results[metric].append(value)

    return results

def print_cross_validation_report(cv_results: Dict[str, List[float]]) -> None:
    print("Cross-Validation Results")
    print("========================\n")
    for metric, values in cv_results.items():
        mean = sum(values) / len(values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
        print(f"{metric.capitalize()}:")
        print(f"  Mean: {mean:.3}")
        print(f"  Standard Deviation: {std_dev:.3}")
        print()
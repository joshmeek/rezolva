import math
from typing import Dict, List, Tuple

from rezolva import Entity, EntityResolver


def calculate_precision_recall_f1(
    true_positives: int, false_positives: int, false_negatives: int
) -> Tuple[float, float, float]:
    """
    Calculate precision, recall, and F1 score for entity resolution results.

    Precision: The fraction of predicted matches that are correct.
    Recall: The fraction of actual matches that were predicted.
    F1 Score: The harmonic mean of precision and recall.

    :param true_positives: Number of correctly predicted matches
    :param false_positives: Number of incorrectly predicted matches
    :param false_negatives: Number of actual matches that were not predicted
    :return: A tuple containing (precision, recall, F1 score)
    """
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1


def calculate_accuracy(true_positives: int, true_negatives: int, total_comparisons: int) -> float:
    """
    Calculate accuracy for entity resolution results.

    Accuracy: The fraction of correct predictions (both true positives and true negatives) among the total number of cases examined.

    :param true_positives: Number of correctly predicted matches
    :param true_negatives: Number of correctly predicted non-matches
    :param total_comparisons: Total number of comparisons made
    :return: Accuracy score
    """
    return (true_positives + true_negatives) / total_comparisons if total_comparisons > 0 else 0


def evaluate_resolver(
    resolver: EntityResolver, test_entities: List[Entity], ground_truth: Dict[str, List[str]], threshold: float = 0.5
) -> Dict[str, float]:
    """
    Evaluate the performance of an EntityResolver using a set of test entities and ground truth data.

    This function runs the resolver on the test entities and compares the results to the ground truth,
    calculating precision, recall, F1 score, and accuracy.

    :param resolver: An instance of EntityResolver to evaluate
    :param test_entities: A list of Entity objects to use for testing
    :param ground_truth: A dictionary mapping entity IDs to lists of matching entity IDs
    :param threshold: The similarity threshold to use for determining matches
    :return: A dictionary containing the evaluation metrics (precision, recall, F1, accuracy)
    """
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

    return {"precision": precision, "recall": recall, "f1": f1, "accuracy": accuracy}


def generate_performance_report(metrics: Dict[str, float]) -> str:
    """
    Generate a formatted performance report from evaluation metrics.

    This function takes a dictionary of evaluation metrics and creates a
    human-readable string report.

    :param metrics: A dictionary containing evaluation metrics (precision, recall, F1, accuracy)
    :return: A formatted string containing the performance report
    """
    report = "Entity Resolution Performance Report\n"
    report += "===================================\n\n"
    report += f"Precision: {metrics['precision']:.3f}\n"
    report += f"Recall: {metrics['recall']:.3f}\n"
    report += f"F1 Score: {metrics['f1']:.3f}\n"
    report += f"Accuracy: {metrics['accuracy']:.3f}\n"
    return report


def cross_validate(
    resolver: EntityResolver, entities: List[Entity], ground_truth: Dict[str, List[str]], k: int = 5
) -> Dict[str, List[float]]:
    """
    Perform k-fold cross-validation on an EntityResolver.

    This function splits the data into k folds, trains the resolver on k-1 folds and tests on the remaining fold,
    repeating this process k times. It returns the evaluation metrics for each fold.

    :param resolver: An instance of EntityResolver to evaluate
    :param entities: A list of all Entity objects
    :param ground_truth: A dictionary mapping entity IDs to lists of matching entity IDs
    :param k: The number of folds for cross-validation
    :return: A dictionary containing lists of evaluation metrics for each fold
    """
    fold_size = len(entities) // k
    results = {"precision": [], "recall": [], "f1": [], "accuracy": []}

    for i in range(k):
        start = i * fold_size
        end = start + fold_size if i < k - 1 else len(entities)

        test_entities = entities[start:end]
        fold_metrics = evaluate_resolver(resolver, test_entities, ground_truth)

        for metric, value in fold_metrics.items():
            results[metric].append(value)

    return results


def print_cross_validation_report(cv_results: Dict[str, List[float]]) -> None:
    """
    Print a report of cross-validation results.

    This function takes the results of cross-validation and prints a summary
    including the mean and standard deviation of each metric across all folds.

    :param cv_results: A dictionary containing lists of evaluation metrics for each fold
    """
    print("Cross-Validation Results")
    print("========================\n")
    for metric, values in cv_results.items():
        mean = sum(values) / len(values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
        print(f"{metric.capitalize()}:")
        print(f"  Mean: {mean:.3}")
        print(f"  Standard Deviation: {std_dev:.3}")
        print()

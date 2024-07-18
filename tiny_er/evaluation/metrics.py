from typing import List, Dict, Any
from ..core.data_structures import MatchResult
from ..core.config import get_config

def calculate_metrics(true_matches: List[tuple], predicted_matches: List[MatchResult]) -> Dict[str, float]:
    true_positive = 0
    false_positive = 0
    false_negative = 0

    predicted_set = {(match.entity1.id, match.entity2.id) for match in predicted_matches if match.is_match}
    true_set = set(true_matches)

    for match in predicted_set:
        if match in true_set or (match[1], match[0]) in true_set:
            true_positive += 1
        else:
            false_positive += 1

    false_negative = len(true_set) - true_positive

    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score
    }

def evaluate(true_matches: List[tuple], predicted_matches: List[MatchResult], config: Dict[str, Any]) -> Dict[str, float]:
    if not config:
        config = get_config()["evaluation"]

    metrics = calculate_metrics(true_matches, predicted_matches)
    return {metric: value for metric, value in metrics.items() if metric in config.get('metrics', [])}
from typing import List, Dict, Any
from ..core.data_structures import Comparison, MatchResult
from ..core.base_classes import Matcher
import math
import random

class SimpleLogisticRegressionMatcher(Matcher):
    def __init__(self, config: Dict[str, Any]):
        self.learning_rate = config.get('learning_rate', 0.01)
        self.num_iterations = config.get('num_iterations', 1000)
        self.weights = {}
        self.threshold = config.get('threshold', 0.5)

    def train(self, labeled_comparisons: List[tuple]):
        # Initialize weights
        num_features = len(labeled_comparisons[0][0].entity1.attributes)
        self.weights = {f'w{i}': random.uniform(-1, 1) for i in range(num_features)}
        self.weights['bias'] = random.uniform(-1, 1)

        for _ in range(self.num_iterations):
            for comparison, label in labeled_comparisons:
                features = self._extract_features(comparison)
                prediction = self._sigmoid(sum(self.weights[f'w{i}'] * feat for i, feat in enumerate(features)) + self.weights['bias'])
                error = label - prediction

                # Update weights
                for i, feat in enumerate(features):
                    self.weights[f'w{i}'] += self.learning_rate * error * feat
                self.weights['bias'] += self.learning_rate * error

    def match(self, comparisons: List[Comparison]) -> List[MatchResult]:
        results = []
        for comparison in comparisons:
            features = self._extract_features(comparison)
            score = self._sigmoid(sum(self.weights[f'w{i}'] * feat for i, feat in enumerate(features)) + self.weights['bias'])
            is_match = score >= self.threshold
            result = MatchResult(
                entity1=comparison.entity1,
                entity2=comparison.entity2,
                confidence=score,
                is_match=is_match
            )
            results.append(result)
        return results

    def _extract_features(self, comparison: Comparison) -> List[float]:
        features = []
        for field in comparison.entity1.attributes:
            if field in comparison.entity2.attributes:
                features.append(float(comparison.entity1.attributes[field] == comparison.entity2.attributes[field]))
            else:
                features.append(0.0)
        return features

    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))

def create_ml_matcher(config: Dict[str, Any]) -> SimpleLogisticRegressionMatcher:
    return SimpleLogisticRegressionMatcher(config)
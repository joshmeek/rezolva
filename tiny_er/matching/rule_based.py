from typing import List, Dict, Any
from ..core.data_structures import Comparison, MatchResult
from ..core.base_classes import Matcher

class ThresholdMatcher(Matcher):
    def __init__(self, config: Dict[str, Any]):
        self.threshold = config.get('threshold', 0.5)  # Lower the default threshold

    def match(self, comparisons: List[Comparison]) -> List[MatchResult]:
        results = []
        for comparison in comparisons:
            is_match = comparison.similarity >= self.threshold
            result = MatchResult(
                entity1=comparison.entity1,
                entity2=comparison.entity2,
                confidence=comparison.similarity,
                is_match=is_match
            )
            results.append(result)
        return results

def create_matcher(config: Dict[str, Any]):
    return ThresholdMatcher(config)
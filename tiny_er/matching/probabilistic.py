import math
from typing import List, Dict, Any
from ..core.data_structures import Comparison, MatchResult
from ..core.base_classes import Matcher

class FellegiSunterMatcher(Matcher):
    def __init__(self, config: Dict[str, Any]):
        self.m_probabilities = config.get('m_probabilities', {})
        self.u_probabilities = config.get('u_probabilities', {})
        self.threshold = config.get('threshold', 0)
        self.fields = list(self.m_probabilities.keys())

    def match(self, comparisons: List[Comparison]) -> List[MatchResult]:
        return [self._match_pair(comparison) for comparison in comparisons]

    def _match_pair(self, comparison: Comparison) -> MatchResult:
        weight = self._calculate_weight(comparison)
        is_match = weight >= self.threshold
        return MatchResult(
            entity1=comparison.entity1,
            entity2=comparison.entity2,
            confidence=weight,
            is_match=is_match
        )

    def _calculate_weight(self, comparison: Comparison) -> float:
        total_weight = 0
        for field in self.fields:
            value1 = comparison.entity1.attributes.get(field)
            value2 = comparison.entity2.attributes.get(field)
            
            if value1 is None or value2 is None:
                # Skip this field if either entity is missing it
                continue
            
            if value1 == value2:
                m = self.m_probabilities[field]
                u = self.u_probabilities[field]
                weight = math.log2(m / u) if u > 0 else 0
            else:
                # For non-matches, we'll use a smaller penalty
                weight = -0.5  # This value can be adjusted

            total_weight += weight
        
        return total_weight

def create_probabilistic_matcher(config: Dict[str, Any]) -> FellegiSunterMatcher:
    return FellegiSunterMatcher(config)
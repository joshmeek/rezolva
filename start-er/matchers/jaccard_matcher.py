
from .base_matcher import BaseAttributeMatcher


class JaccardMatcher(BaseAttributeMatcher):
    def _calculate_attribute_similarity(self, val1: str, val2: str) -> float:
        set1 = set(val1.lower().split())
        set2 = set(val2.lower().split())
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union
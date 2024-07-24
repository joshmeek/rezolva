from .base_matcher import BaseAttributeMatcher


class JaccardMatcher(BaseAttributeMatcher):
    """
    A matcher that uses Jaccard similarity to compare entities.

    Jaccard similarity is defined as the size of the intersection divided by the size of the union of two sets.
    For text attributes, the sets are typically the sets of words or n-grams in the text.

    How Jaccard Similarity works:
    1. Convert attribute values into sets (e.g., sets of words for text attributes)
    2. Compute the intersection and union of these sets
    3. Divide the size of the intersection by the size of the union

    Advantages:
    - Simple to understand and implement
    - Works well for comparing sets of items (e.g., tags, categories)
    - Normalizes for the size of the attributes

    Disadvantages:
    - Doesn't consider the frequency of items, only their presence or absence
    - May not work well for very short text where small differences have a large impact

    :param threshold: The similarity threshold above which entities are considered a match
    :param attribute_weights: A dictionary mapping attribute names to their importance in matching
    """

    def _calculate_attribute_similarity(self, val1: str, val2: str) -> float:
        set1 = set(val1.lower().split())
        set2 = set(val2.lower().split())

        if not set1 and not set2:
            return 1.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union

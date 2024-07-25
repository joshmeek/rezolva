from .base_matcher import BaseAttributeMatcher


class LevenshteinMatcher(BaseAttributeMatcher):
    """
    A matcher that uses Levenshtein distance to compare entities.

    Levenshtein distance, also known as edit distance, is the minimum number of single-character edits
    (insertions, deletions, or substitutions) required to change one word into another.

    How Levenshtein Distance works:
    1. Initialize a matrix with the lengths of the two strings plus one
    2. Fill the matrix using dynamic programming, where each cell represents the minimum edits needed
    3. The bottom-right cell gives the Levenshtein distance
    4. Convert the distance to a similarity score

    Advantages:
    - Handles spelling errors and typos well
    - Works for comparing strings of different lengths
    - Intuitive measure of string similarity

    Disadvantages:
    - Can be computationally expensive for long strings
    - Doesn't consider semantic similarity, only syntactic

    :param threshold: The similarity threshold above which entities are considered a match
    :param attribute_weights: A dictionary mapping attribute names to their importance in matching
    """

    def _calculate_attribute_similarity(self, val1: str, val2: str) -> float:
        distance = self._levenshtein_distance(val1, val2)
        max_length = max(len(val1), len(val2))
        return 1 - (distance / max_length) if max_length > 0 else 1

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

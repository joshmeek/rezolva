from .base_matcher import BaseAttributeMatcher


class JaroWinklerMatcher(BaseAttributeMatcher):
    """
    A matcher that uses Jaro-Winkler distance to compare entities.

    Jaro-Winkler distance is a string metric measuring edit distance between two sequences. It's a variant of the
    Jaro distance metric and mainly used for comparing short strings such as person names.

    How Jaro-Winkler works:
    1. Calculate the Jaro distance
    2. Determine the length of the common prefix up to 4 characters
    3. Adjust the Jaro distance based on the common prefix

    Advantages:
    - Works well for short strings like names or words
    - Gives more favorable ratings to strings that match from the beginning
    - Handles transpositions well

    Disadvantages:
    - May not be suitable for long strings or sentences
    - Can be computationally expensive for large datasets

    :param threshold: The similarity threshold above which entities are considered a match
    :param attribute_weights: A dictionary mapping attribute names to their importance in matching
    """

    def _calculate_attribute_similarity(self, val1: str, val2: str) -> float:
        return self._jaro_winkler_similarity(val1, val2)

    def _jaro_winkler_similarity(self, s1: str, s2: str) -> float:
        jaro_distance = self._jaro_distance(s1, s2)
        prefix_length = 0
        for char1, char2 in zip(s1, s2):
            if char1 == char2:
                prefix_length += 1
            else:
                break
        prefix_length = min(prefix_length, 4)
        return jaro_distance + (prefix_length * 0.1 * (1 - jaro_distance))

    def _jaro_distance(self, s1: str, s2: str) -> float:
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        match_distance = (max(len(s1), len(s2)) // 2) - 1
        s1_matches = [0] * len(s1)
        s2_matches = [0] * len(s2)
        matches = 0
        transpositions = 0
        for i in range(len(s1)):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len(s2))
            for j in range(start, end):
                if s2_matches[j]:
                    continue
                if s1[i] != s2[j]:
                    continue
                s1_matches[i] = 1
                s2_matches[j] = 1
                matches += 1
                break
        if matches == 0:
            return 0.0
        k = 0
        for i in range(len(s1)):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1
        return ((matches / len(s1)) + (matches / len(s2)) + ((matches - transpositions / 2) / matches)) / 3.0

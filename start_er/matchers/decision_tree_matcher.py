import random
from typing import List, Tuple, Dict
from ..core.base import Matcher, Entity

class DecisionTreeNode:
    def __init__(self, attribute=None, threshold=None, left=None, right=None, value=None):
        self.attribute = attribute
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class DecisionTreeMatcher(Matcher):
    def __init__(self, attributes: List[str], max_depth: int = 3):
        self.attributes = attributes
        self.max_depth = max_depth
        self.tree = None

    def train(self, pairs: List[Tuple[Entity, Entity]], labels: List[bool]):
        self.tree = self._build_tree(pairs, labels, 0)

    def match(self, entity: Entity, candidates: List[Entity]) -> List[Tuple[Entity, float]]:
        matches = []
        for candidate in candidates:
            if candidate.id != entity.id:
                similarity = self._predict(entity, candidate)
                if similarity > 0.5:
                    matches.append((candidate, similarity))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def _build_tree(self, pairs: List[Tuple[Entity, Entity]], labels: List[bool], depth: int) -> DecisionTreeNode:
        if depth == self.max_depth or len(set(labels)) == 1:
            return DecisionTreeNode(value=sum(labels) / len(labels))

        best_attribute = None
        best_threshold = None
        best_gain = 0

        for attribute in self.attributes:
            values = [self._compare_attribute(pair[0], pair[1], attribute) for pair in pairs]
            threshold = sum(values) / len(values)
            left_labels = [label for value, label in zip(values, labels) if value <= threshold]
            right_labels = [label for value, label in zip(values, labels) if value > threshold]

            gain = self._calculate_gini(labels) - (
                len(left_labels) / len(labels) * self._calculate_gini(left_labels) +
                len(right_labels) / len(labels) * self._calculate_gini(right_labels)
            )

            if gain > best_gain:
                best_gain = gain
                best_attribute = attribute
                best_threshold = threshold

        if best_attribute is None:
            return DecisionTreeNode(value=sum(labels) / len(labels))

        left_pairs = [pair for pair in pairs if self._compare_attribute(pair[0], pair[1], best_attribute) <= best_threshold]
        right_pairs = [pair for pair in pairs if self._compare_attribute(pair[0], pair[1], best_attribute) > best_threshold]
        left_labels = [label for value, label in zip(values, labels) if value <= best_threshold]
        right_labels = [label for value, label in zip(values, labels) if value > best_threshold]

        left_subtree = self._build_tree(left_pairs, left_labels, depth + 1)
        right_subtree = self._build_tree(right_pairs, right_labels, depth + 1)

        return DecisionTreeNode(best_attribute, best_threshold, left_subtree, right_subtree)

    def _predict(self, entity1: Entity, entity2: Entity) -> float:
        node = self.tree
        while node.value is None:
            if self._compare_attribute(entity1, entity2, node.attribute) <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

    def _compare_attribute(self, entity1: Entity, entity2: Entity, attribute: str) -> float:
        value1 = entity1.attributes.get(attribute, '')
        value2 = entity2.attributes.get(attribute, '')
        return self._jaccard_similarity(str(value1), str(value2))

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0

    def _calculate_gini(self, labels: List[bool]) -> float:
        if len(labels) == 0:
            return 0.0
        p = sum(labels) / len(labels)
        return 2 * p * (1 - p)

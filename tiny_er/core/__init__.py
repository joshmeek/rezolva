from .entity_resolver import EntityResolver
from .config import get_config
from .data_structures import Entity, Cluster, Comparison, MatchResult, Block
from .base_classes import Preprocessor, Blocker, SimilarityMeasure, Matcher

__all__ = [
    'EntityResolver', 'get_config', 'Entity', 'Cluster', 'Comparison', 'MatchResult', 'Block',
    'Preprocessor', 'Blocker', 'SimilarityMeasure', 'Matcher'
]
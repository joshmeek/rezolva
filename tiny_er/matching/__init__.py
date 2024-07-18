from .rule_based import create_matcher
from .probabilistic import create_probabilistic_matcher
from .machine_learning import create_ml_matcher

__all__ = ['create_matcher', 'create_probabilistic_matcher', 'create_ml_matcher']
from .core.entity_resolver import EntityResolver
from .core.config import get_config
from .preprocessing.normalizer import create_normalizer
from .blocking.standard_blocking import create_blocker
from .similarity.string_similarity import create_similarity_measure
from .matching.rule_based import create_matcher
from .evaluation.metrics import evaluate
from .utils.data_loader import load_csv, load_json, save_results

__all__ = [
    'EntityResolver',
    'get_config',
    'create_normalizer',
    'create_blocker',
    'create_similarity_measure',
    'create_matcher',
    'evaluate',
    'load_csv',
    'load_json',
    'save_results'
]

__version__ = '0.1.0'
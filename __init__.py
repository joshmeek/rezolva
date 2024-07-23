# Import main components
from .core.resolver import EntityResolver
from .core.base import Entity, Preprocessor, ModelBuilder, Matcher, Blocker

# Import default implementations
from .preprocessors.simple_preprocessor import SimplePreprocessor
from .model_builders.simple_model_builder import SimpleModelBuilder
from .matchers.jaccard_matcher import JaccardMatcher
from .blockers.simple_blocker import SimpleBlocker

# Define what should be available when someone does `from tiny_er import *`
__all__ = [
    'EntityResolver',
    'Entity',
    'Preprocessor',
    'ModelBuilder',
    'Matcher',
    'Blocker',
    'SimplePreprocessor',
    'SimpleModelBuilder',
    'JaccardMatcher',
    'SimpleBlocker',
]

# Optionally, you can include package metadata
__version__ = '0.1.0'
__author__ = 'Josh Meek'
__email__ = 'mail@josh.dev'
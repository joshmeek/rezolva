# File: start_er/__init__.py

from .blockers.simple_blocker import SimpleBlocker
from .core.base import Entity
from .core.resolver import EntityResolver
from .model_builders.simple_model_builder import SimpleModelBuilder
from .preprocessors.simple_preprocessor import SimplePreprocessor

# Version of the start_er package
__version__ = "0.1.0"

# List of public objects in this package
__all__ = ["EntityResolver", "Entity", "SimplePreprocessor", "SimpleModelBuilder", "SimpleBlocker"]

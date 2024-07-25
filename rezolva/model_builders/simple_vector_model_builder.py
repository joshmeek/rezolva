import math
from collections import Counter
from typing import Any, Dict, List

from ..core.base import Entity, ModelBuilder


class SimpleVectorModelBuilder(ModelBuilder):
    """
    A model builder that creates vector representations of entities for similarity-based matching.

    This model builder converts entity attributes into numerical vectors, typically using
    techniques like TF-IDF (Term Frequency-Inverse Document Frequency). These vector
    representations can then be used for efficient similarity computations.

    How it works:
    1. Build a vocabulary from all entity attributes
    2. Compute IDF (Inverse Document Frequency) for each term in the vocabulary
    3. For each entity, compute a TF-IDF vector based on its attributes

    The resulting model includes:
    - A dictionary of entity vectors
    - The global vocabulary
    - IDF values for each term in the vocabulary

    This model is particularly useful for cosine similarity-based matching and can handle
    partial matches and fuzzy matching more effectively than simple index-based models.

    Usage:
    builder = SimpleVectorModelBuilder(['name', 'description'])
    model = builder.train(entities)

    :param attributes: A list of attribute names to be vectorized
    :inherits: ModelBuilder
    """

    def __init__(self, attributes: List[str]):
        self.attributes = attributes
        self.vocabulary = set()

    def train(self, entities: List[Entity]) -> Any:
        model = {"entities": {}, "vectors": {}, "idf": {}}

        # Build vocabulary and document frequency
        doc_freq = Counter()
        for entity in entities:
            model["entities"][entity.id] = entity
            entity_terms = set()
            for attr in self.attributes:
                terms = str(entity.attributes.get(attr, "")).lower().split()
                self.vocabulary.update(terms)
                entity_terms.update(terms)
            doc_freq.update(entity_terms)

        # Calculate IDF
        num_docs = len(entities)
        model["idf"] = {term: math.log(num_docs / (freq + 1)) for term, freq in doc_freq.items()}

        # Calculate TF-IDF vectors
        for entity in entities:
            vector = {}
            term_freq = Counter()
            for attr in self.attributes:
                term_freq.update(str(entity.attributes.get(attr, "")).lower().split())

            for term, freq in term_freq.items():
                tf = freq / sum(term_freq.values())
                vector[term] = tf * model["idf"][term]

            model["vectors"][entity.id] = vector

        return model

    def update(self, model: Any, new_entities: List[Entity]) -> Any:
        # For simplicity, we're retraining the entire model here.
        # In a real-world scenario, you might want to implement incremental updates.
        all_entities = list(model["entities"].values()) + new_entities
        return self.train(all_entities)

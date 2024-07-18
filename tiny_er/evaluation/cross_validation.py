from typing import List, Dict, Any, Callable, Tuple
from ..core.data_structures import Entity, MatchResult
from .metrics import evaluate
import random
from collections import defaultdict

def k_fold_cross_validation(entities: List[Entity], 
                            resolver_function: Callable[[List[Entity]], List[MatchResult]],
                            true_matches: List[tuple],
                            k: int = 5,
                            config: Dict[str, Any] = None) -> Dict[str, float]:
    random.shuffle(entities)
    fold_size = len(entities) // k
    total_metrics = defaultdict(float)

    for i in range(k):
        start = i * fold_size
        end = start + fold_size if i < k - 1 else len(entities)
        
        test_entities = entities[start:end]
        train_entities = entities[:start] + entities[end:]

        predicted_matches = resolver_function(train_entities)
        fold_metrics = evaluate(true_matches, predicted_matches, config)

        for metric, value in fold_metrics.items():
            total_metrics[metric] += value

    avg_metrics = {metric: value / k for metric, value in total_metrics.items()}
    return avg_metrics

def train_test_split(entities: List[Entity], 
                     true_matches: List[tuple],
                     test_size: float = 0.2,
                     random_state: int = None) -> Tuple[List[Entity], List[Entity], List[tuple], List[tuple]]:
    if random_state is not None:
        random.seed(random_state)
    
    # Ensure we have at least one match
    if not true_matches:
        raise ValueError("No true matches provided")

    # Choose a random match to preserve
    preserved_match = random.choice(true_matches)
    preserved_entities = [next(e for e in entities if e.id == id) for id in preserved_match]

    # Remove preserved entities from the list to shuffle
    remaining_entities = [e for e in entities if e not in preserved_entities]
    
    # Shuffle remaining entities
    shuffled_entities = random.sample(remaining_entities, len(remaining_entities))
    
    # Calculate split sizes
    total_size = len(entities)
    test_size_count = max(int(total_size * test_size), 2)  # Ensure at least 2 entities in test set
    train_size_count = total_size - test_size_count

    # Decide whether to put preserved match in train or test set
    if random.random() < test_size:
        test_entities = preserved_entities + shuffled_entities[:test_size_count-2]
        train_entities = shuffled_entities[test_size_count-2:]
    else:
        train_entities = preserved_entities + shuffled_entities[:train_size_count-2]
        test_entities = shuffled_entities[train_size_count-2:]

    # Create sets of entity IDs for quick lookup
    test_entity_ids = {entity.id for entity in test_entities}
    train_entity_ids = {entity.id for entity in train_entities}

    # Split matches
    test_matches = [match for match in true_matches if match[0] in test_entity_ids and match[1] in test_entity_ids]
    train_matches = [match for match in true_matches if match[0] in train_entity_ids and match[1] in train_entity_ids]

    return train_entities, test_entities, train_matches, test_matches
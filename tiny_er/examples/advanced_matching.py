from tiny_er.core.entity_resolver import EntityResolver
from tiny_er.core.config import get_config
from tiny_er.preprocessing.normalizer import create_normalizer
from tiny_er.blocking.standard_blocking import create_blocker
from tiny_er.similarity.string_similarity import create_similarity_measure
from tiny_er.matching.probabilistic import create_probabilistic_matcher
from tiny_er.utils.data_loader import load_csv, save_results
from tiny_er.evaluation.metrics import evaluate

def main():
    # Load configuration
    config = get_config()

    # Create components
    normalizer = create_normalizer(config['preprocessing'])
    blocker = create_blocker(config['blocking'])
    similarity_measure = create_similarity_measure(config['similarity'])
    
    # Use probabilistic matcher
    matcher = create_probabilistic_matcher({
        'm_probabilities': {'name': 0.9, 'address': 0.8, 'phone': 0.9},
        'u_probabilities': {'name': 0.1, 'address': 0.3, 'phone': 0.1},
        'threshold': 0.7
    })

    # Create EntityResolver
    resolver = EntityResolver(normalizer, blocker, similarity_measure, matcher)

    # Load data
    entities = load_csv('path/to/your/data.csv', id_column='id')

    # Load true matches (if available)
    true_matches = load_csv('path/to/true_matches.csv', id_column='pair_id')

    # Resolve entities
    results = resolver.resolve(entities)

    # Process results
    output = []
    for cluster in results:
        for entity in cluster:
            output.append({
                'cluster_id': id(cluster),
                'entity_id': entity.id,
                'attributes': entity.attributes
            })

    save_results('path/to/output_advanced_matching.csv', output)

    # Evaluate results
    if true_matches:
        evaluation_results = evaluate(true_matches, results, config['evaluation'])
        print("Evaluation results:")
        for metric, value in evaluation_results.items():
            print(f"{metric}: {value:.4f}")

    print(f"Advanced entity resolution completed. Resolved {len(results)} clusters.")

if __name__ == "__main__":
    main()
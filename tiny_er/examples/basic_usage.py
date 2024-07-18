from tiny_er.core.entity_resolver import EntityResolver
from tiny_er.core.config import get_config
from tiny_er.preprocessing.normalizer import create_normalizer
from tiny_er.blocking.standard_blocking import create_blocker
from tiny_er.similarity.string_similarity import create_similarity_measure
from tiny_er.matching.rule_based import create_matcher
from tiny_er.utils.data_loader import load_csv, save_results

def main():
    # Load configuration
    config = get_config()

    # Create components
    normalizer = create_normalizer(config['preprocessing'])
    blocker = create_blocker(config['blocking'])
    similarity_measure = create_similarity_measure(config['similarity'])
    matcher = create_matcher(config['matching'])

    # Create EntityResolver
    resolver = EntityResolver(normalizer, blocker, similarity_measure, matcher)

    # Load data
    entities = load_csv('path/to/your/data.csv', id_column='id')

    # Resolve entities
    results = resolver.resolve(entities)

    # Process and save results
    output = []
    for cluster in results:
        for entity in cluster:
            output.append({
                'cluster_id': id(cluster),
                'entity_id': entity.id,
                'attributes': entity.attributes
            })

    save_results('path/to/output.csv', output)

    print(f"Entity resolution completed. Resolved {len(results)} clusters.")

if __name__ == "__main__":
    main()
from tiny_er.core.entity_resolver import EntityResolver
from tiny_er.core.config import get_config
from tiny_er.preprocessing.normalizer import create_normalizer
from tiny_er.blocking.standard_blocking import create_blocker
from tiny_er.similarity.string_similarity import create_similarity_measure
from tiny_er.similarity.vector_similarity import create_vector_similarity_measure
from tiny_er.similarity.phonetic_similarity import create_phonetic_similarity_measure
from tiny_er.matching.rule_based import create_matcher
from tiny_er.utils.data_loader import load_csv, save_results

class CombinedSimilarityMeasure:
    def __init__(self, measures, weights):
        self.measures = measures
        self.weights = weights

    def compute(self, entity1, entity2):
        total_similarity = 0
        total_weight = sum(self.weights)
        for measure, weight in zip(self.measures, self.weights):
            similarity = measure.compute(entity1, entity2)
            total_similarity += similarity * weight
        return total_similarity / total_weight

def main():
    # Load configuration
    config = get_config()

    # Create components
    normalizer = create_normalizer(config['preprocessing'])
    blocker = create_blocker(config['blocking'])
    
    # Create multiple similarity measures
    string_sim = create_similarity_measure({'method': 'levenshtein'})
    vector_sim = create_vector_similarity_measure({'method': 'cosine', 'fields': ['age', 'income']})
    phonetic_sim = create_phonetic_similarity_measure({'method': 'soundex', 'field': 'name'})

    # Combine similarity measures
    combined_sim = CombinedSimilarityMeasure(
        measures=[string_sim, vector_sim, phonetic_sim],
        weights=[0.5, 0.3, 0.2]
    )

    matcher = create_matcher(config['matching'])

    # Create EntityResolver with combined similarity measure
    resolver = EntityResolver(normalizer, blocker, combined_sim, matcher)

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

    save_results('path/to/output_multiple_similarity.csv', output)

    print(f"Entity resolution with multiple similarity measures completed. Resolved {len(results)} clusters.")

if __name__ == "__main__":
    main()
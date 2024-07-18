from typing import List, Dict, Any
from ..core.data_structures import Cluster

def print_cluster_summary(clusters: List[Cluster]):
    print("Cluster Summary:")
    print("-" * 20)
    for i, cluster in enumerate(clusters, 1):
        print(f"Cluster {i}: {len(cluster)} entities")

def print_detailed_clusters(clusters: List[Cluster], max_entities: int = 5):
    print("Detailed Clusters:")
    print("-" * 20)
    for i, cluster in enumerate(clusters, 1):
        print(f"Cluster {i}:")
        for j, entity in enumerate(cluster.entities):
            if j >= max_entities:
                print(f"  ... and {len(cluster) - max_entities} more entities")
                break
            print(f"  Entity {entity.id}: {entity.attributes}")
        print()

def print_matching_matrix(entities: List[Dict[str, Any]], matches: List[tuple]):
    entity_ids = [e['id'] for e in entities]
    n = len(entity_ids)
    matrix = [[' ' for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        matrix[i][i] = 'X'
    
    for match in matches:
        i = entity_ids.index(match[0])
        j = entity_ids.index(match[1])
        matrix[i][j] = matrix[j][i] = 'M'
    
    print("Matching Matrix:")
    print("-" * (n * 2 + 3))
    print("  " + " ".join(str(i) for i in range(n)))
    for i, row in enumerate(matrix):
        print(f"{i} {' '.join(row)}")

def text_histogram(data: Dict[str, int], width: int = 50):
    if not data:
        return

    max_value = max(data.values())
    max_label_length = max(len(label) for label in data.keys())

    print("Histogram:")
    print("-" * (max_label_length + width + 10))
    for label, value in data.items():
        bar_length = int((value / max_value) * width)
        print(f"{label.rjust(max_label_length)} | {'#' * bar_length} {value}")

def visualize_results(clusters: List[Cluster], matches: List[tuple], entities: List[Dict[str, Any]]):
    print_cluster_summary(clusters)
    print()
    print_detailed_clusters(clusters)
    print()
    print_matching_matrix(entities, matches)
    print()
    
    # Create a histogram of cluster sizes
    cluster_sizes = {}
    for cluster in clusters:
        size = len(cluster)
        cluster_sizes[size] = cluster_sizes.get(size, 0) + 1
    text_histogram(cluster_sizes)
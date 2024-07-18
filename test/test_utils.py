import unittest
import os
import tempfile
from tiny_er.utils.data_loader import load_csv, load_json, save_results
from tiny_er.utils.logging import setup_logger, EntityResolutionLogger
from tiny_er.utils.visualization import print_cluster_summary, print_detailed_clusters, print_matching_matrix, text_histogram

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_load_csv(self):
        csv_content = "id,name,age\n1,John Doe,30\n2,Jane Doe,28"
        csv_file = os.path.join(self.temp_dir, "test.csv")
        with open(csv_file, 'w') as f:
            f.write(csv_content)
        
        entities = load_csv(csv_file, "id")
        self.assertEqual(len(entities), 2)
        self.assertEqual(entities[0].id, "1")
        self.assertEqual(entities[0].attributes["name"], "John Doe")
        self.assertEqual(entities[1].attributes["age"], "28")

    def test_load_json(self):
        json_content = '[{"id": "1", "name": "John Doe", "age": 30}, {"id": "2", "name": "Jane Doe", "age": 28}]'
        json_file = os.path.join(self.temp_dir, "test.json")
        with open(json_file, 'w') as f:
            f.write(json_content)
        
        entities = load_json(json_file, "id")
        self.assertEqual(len(entities), 2)
        self.assertEqual(entities[0].id, "1")
        self.assertEqual(entities[0].attributes["name"], "John Doe")
        self.assertEqual(entities[1].attributes["age"], 28)

    def test_save_results(self):
        results = [
            {"id": "1", "name": "John Doe", "match": "2"},
            {"id": "2", "name": "Jane Doe", "match": "1"}
        ]
        output_file = os.path.join(self.temp_dir, "output.csv")
        save_results(output_file, results)
        
        with open(output_file, 'r') as f:
            content = f.read()
        self.assertIn("id,name,match", content)
        self.assertIn("1,John Doe,2", content)
        self.assertIn("2,Jane Doe,1", content)

    def test_setup_logger(self):
        logger = setup_logger({"log_level": "INFO"})
        self.assertEqual(logger.level, 20)  # 20 is the numeric value for INFO level

    def test_entity_resolution_logger(self):
        logger = setup_logger({"log_level": "INFO"})
        er_logger = EntityResolutionLogger(logger)
        
        # These calls should not raise any exceptions
        er_logger.log_start(100)
        er_logger.log_blocking(10)
        er_logger.log_comparison(1000)
        er_logger.log_matching(50)
        er_logger.log_error("Test error")
        er_logger.log_warning("Test warning")
        er_logger.log_custom("Custom message", "DEBUG")

    def test_print_cluster_summary(self):
        from tiny_er.core.data_structures import Cluster, Entity
        clusters = [
            Cluster({Entity("1", {"name": "John"}), Entity("2", {"name": "Johnny"})}),
            Cluster({Entity("3", {"name": "Jane"})})
        ]
        # This should not raise any exception
        print_cluster_summary(clusters)

    def test_print_detailed_clusters(self):
        from tiny_er.core.data_structures import Cluster, Entity
        clusters = [
            Cluster({Entity("1", {"name": "John"}), Entity("2", {"name": "Johnny"})}),
            Cluster({Entity("3", {"name": "Jane"})})
        ]
        # This should not raise any exception
        print_detailed_clusters(clusters)

    def test_print_matching_matrix(self):
        entities = [
            {"id": "1", "name": "John"},
            {"id": "2", "name": "Jane"},
            {"id": "3", "name": "Bob"}
        ]
        matches = [("1", "2")]
        # This should not raise any exception
        print_matching_matrix(entities, matches)

    def test_text_histogram(self):
        data = {"A": 5, "B": 10, "C": 3}
        # This should not raise any exception
        text_histogram(data)

if __name__ == '__main__':
    unittest.main()
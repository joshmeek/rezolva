import unittest
from tiny_er.core.data_structures import Entity, Cluster, Comparison, MatchResult, Block
from tiny_er.core.entity_resolver import EntityResolver
from tiny_er.core.config import get_config, DEFAULT_CONFIG

class TestCore(unittest.TestCase):
    def test_entity(self):
        entity = Entity(id="1", attributes={"name": "John", "age": 30})
        self.assertEqual(entity.id, "1")
        self.assertEqual(entity.attributes["name"], "John")
        self.assertEqual(entity.attributes["age"], 30)

    def test_cluster(self):
        entity1 = Entity(id="1", attributes={"name": "John"})
        entity2 = Entity(id="2", attributes={"name": "Johnny"})
        cluster = Cluster()
        cluster.add(entity1)
        cluster.add(entity2)
        self.assertEqual(len(cluster), 2)
        self.assertIn(entity1, cluster)
        self.assertIn(entity2, cluster)

    def test_comparison(self):
        entity1 = Entity(id="1", attributes={"name": "John"})
        entity2 = Entity(id="2", attributes={"name": "Johnny"})
        comparison = Comparison(entity1, entity2, 0.8)
        self.assertEqual(comparison.entity1, entity1)
        self.assertEqual(comparison.entity2, entity2)
        self.assertEqual(comparison.similarity, 0.8)

    def test_match_result(self):
        entity1 = Entity(id="1", attributes={"name": "John"})
        entity2 = Entity(id="2", attributes={"name": "Johnny"})
        match_result = MatchResult(entity1, entity2, 0.8, True)
        self.assertEqual(match_result.entity1, entity1)
        self.assertEqual(match_result.entity2, entity2)
        self.assertEqual(match_result.confidence, 0.8)
        self.assertTrue(match_result.is_match)

    def test_block(self):
        entity1 = Entity(id="1", attributes={"name": "John"})
        entity2 = Entity(id="2", attributes={"name": "Johnny"})
        block = Block("J")
        block.add(entity1)
        block.add(entity2)
        self.assertEqual(len(block), 2)
        self.assertEqual(block[0], entity1)
        self.assertEqual(block[1], entity2)

    def test_get_config(self):
        config = get_config()
        self.assertEqual(config, DEFAULT_CONFIG)
        
        user_config = {"preprocessing": {"lowercase": False}}
        merged_config = get_config(user_config)
        self.assertFalse(merged_config["preprocessing"]["lowercase"])
        self.assertTrue(merged_config["preprocessing"]["remove_punctuation"])

    def test_entity_resolver(self):
        class MockPreprocessor:
            def preprocess(self, entities):
                return entities

        class MockBlocker:
            def block(self, entities):
                return [Block("all", entities)]

        class MockSimilarityMeasure:
            def compute(self, entity1, entity2):
                return 1.0 if entity1.attributes["name"] == entity2.attributes["name"] else 0.0

        class MockMatcher:
            def match(self, comparisons):
                return [MatchResult(c.entity1, c.entity2, c.similarity, c.similarity > 0.5) for c in comparisons]

        resolver = EntityResolver(MockPreprocessor(), MockBlocker(), MockSimilarityMeasure(), MockMatcher())
        entities = [
            Entity("1", {"name": "John"}),
            Entity("2", {"name": "Jane"}),
            Entity("3", {"name": "John"}),
            Entity("4", {"name": "Jack"})
        ]
        clusters = resolver.resolve(entities)
        
        self.assertEqual(len(clusters), 3)
        self.assertTrue(any(len(cluster) == 2 for cluster in clusters))
        self.assertTrue(all(len(cluster) >= 1 for cluster in clusters))

        # Additional assertions to verify cluster contents
        john_cluster = next(cluster for cluster in clusters if len(cluster) == 2)
        self.assertTrue(all(entity.attributes["name"] == "John" for entity in john_cluster))

        singleton_clusters = [cluster for cluster in clusters if len(cluster) == 1]
        self.assertEqual(len(singleton_clusters), 2)
        singleton_names = set(next(iter(cluster)).attributes["name"] for cluster in singleton_clusters)
        self.assertEqual(singleton_names, {"Jane", "Jack"})    

if __name__ == '__main__':
    unittest.main()
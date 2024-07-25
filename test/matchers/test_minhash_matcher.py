import unittest

from rezolva.core.base import Entity
from rezolva.matchers.minhash_matcher import MinHashMatcher


class TestMinHashMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = MinHashMatcher(
            threshold=0.5, num_hash_functions=100, attribute_weights={"title": 1.0, "description": 0.5}
        )

    def test_match(self):
        entity = Entity("1", {"title": "iPhone 12", "description": "Latest smartphone from Apple"})
        candidates = [
            Entity("2", {"title": "iPhone 12 Pro", "description": "Advanced smartphone from Apple"}),
            Entity("3", {"title": "Galaxy S21", "description": "Latest smartphone from Samsung"}),
        ]

        matches = self.matcher.match(entity, candidates)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0].id, "2")
        self.assertGreater(matches[0][1], 0.5)

    def test_minhash_signature(self):
        text = "This is a test sentence for MinHash"
        signature = self.matcher._minhash_signature(text)

        self.assertEqual(len(signature), self.matcher.num_hash_functions)
        self.assertTrue(all(isinstance(x, int) for x in signature))

    def test_calculate_weighted_similarity(self):
        entity_signatures = {
            "title": self.matcher._minhash_signature("iPhone 12"),
            "description": self.matcher._minhash_signature("Latest smartphone from Apple"),
        }
        candidate = Entity("2", {"title": "iPhone 12 Pro", "description": "Advanced smartphone from Apple"})

        similarity = self.matcher._calculate_weighted_similarity(entity_signatures, candidate)
        self.assertGreater(similarity, 0)
        self.assertLessEqual(similarity, 1)

    def test_generate_hash_functions(self):
        hash_functions = self.matcher._generate_hash_functions()
        self.assertEqual(len(hash_functions), self.matcher.num_hash_functions)

        # Test that hash functions produce different results for the same input
        test_input = "test"
        hash_results = [h(test_input) for h in hash_functions]
        self.assertEqual(len(set(hash_results)), len(hash_results))  # All results should be unique


if __name__ == "__main__":
    unittest.main()

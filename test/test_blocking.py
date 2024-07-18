import unittest
from tiny_er.core.data_structures import Entity
from tiny_er.blocking.standard_blocking import StandardBlocker
from tiny_er.blocking.lsh_blocking import LSHBlocker
from tiny_er.blocking.sorted_neighborhood import SortedNeighborhoodBlocker

class TestBlocking(unittest.TestCase):
    def setUp(self):
        self.entities = [
            Entity("1", {"name": "John Doe", "age": "30"}),
            Entity("2", {"name": "Jane Doe", "age": "28"}),
            Entity("3", {"name": "Bob Smith", "age": "45"}),
            Entity("4", {"name": "Alice Johnson", "age": "35"})
        ]

    def test_standard_blocker(self):
        blocker = StandardBlocker({"block_key": "name"})
        blocks = blocker.block(self.entities)
        self.assertEqual(len(blocks), 3)  # One block for each first letter: J, B, A
        self.assertTrue(any(len(block) == 2 for block in blocks))  # "J" block should have 2 entities

    def test_lsh_blocker(self):
        config = {
            "num_hash_functions": 2,
            "band_size": 1,
            "minhash_fields": ["name", "age"]
        }
        blocker = LSHBlocker(config)
        blocks = blocker.block(self.entities)
        self.assertGreater(len(blocks), 0)
        self.assertTrue(all(len(block) > 0 for block in blocks))

    def test_sorted_neighborhood_blocker(self):
        blocker = SortedNeighborhoodBlocker({"window_size": 2})
        blocks = blocker.block(self.entities)
        self.assertEqual(len(blocks), 3)  # With 4 entities and window size 2, we should have 3 blocks
        self.assertTrue(all(len(block) == 2 for block in blocks))

if __name__ == '__main__':
    unittest.main()
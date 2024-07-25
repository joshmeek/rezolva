import unittest

from rezolva.blockers.lsh_blocker import LSHBlocker
from rezolva.core.base import Entity


class TestLSHBlocker(unittest.TestCase):
    def setUp(self):
        self.blocker = LSHBlocker(num_hash_functions=100, band_size=5, attribute="description")

    def test_create_blocks(self):
        entities = [
            Entity("1", {"name": "iPhone 12", "description": "Latest smartphone from Apple"}),
            Entity("2", {"name": "iPhone 12 Pro", "description": "Advanced smartphone from Apple"}),
            Entity("3", {"name": "Galaxy S21", "description": "Latest smartphone from Samsung"}),
            Entity("4", {"name": "MacBook Pro", "description": "Powerful laptop from Apple"}),
            Entity("5", {"name": "Dell XPS", "description": "High-performance laptop"}),
        ]

        blocks = self.blocker.create_blocks(entities)

        self.assertGreater(len(blocks), 0)
        self.assertTrue(all(isinstance(key, int) for key in blocks.keys()))
        self.assertTrue(all(isinstance(block, list) for block in blocks.values()))

        # Check that similar entities are more likely to be in the same block
        apple_blocks = set()
        samsung_blocks = set()
        laptop_blocks = set()

        for block_key, block_entities in blocks.items():
            for entity in block_entities:
                if "Apple" in entity.attributes["description"]:
                    apple_blocks.add(block_key)
                if "Samsung" in entity.attributes["description"]:
                    samsung_blocks.add(block_key)
                if "laptop" in entity.attributes["description"]:
                    laptop_blocks.add(block_key)

        self.assertGreater(len(apple_blocks.intersection(samsung_blocks)), 0)
        self.assertGreater(len(laptop_blocks - apple_blocks), 0)

    def test_minhash_signature(self):
        text = "This is a test sentence for MinHash"
        signature = self.blocker._minhash_signature(text)

        self.assertEqual(len(signature), self.blocker.num_hash_functions)
        self.assertTrue(all(isinstance(x, int) for x in signature))

    def test_empty_input(self):
        blocks = self.blocker.create_blocks([])
        self.assertEqual(len(blocks), 0)

    def test_single_entity(self):
        entity = Entity("1", {"name": "iPhone 12", "description": "Latest smartphone from Apple"})
        blocks = self.blocker.create_blocks([entity])
        self.assertGreater(len(blocks), 0)
        self.assertEqual(sum(len(block) for block in blocks.values()), 20)


if __name__ == "__main__":
    unittest.main()

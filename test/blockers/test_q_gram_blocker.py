import unittest

from rezolva.blockers.q_gram_blocker import QGramBlocker, default_key_func
from rezolva.core.base import Entity


class TestQGramBlocker(unittest.TestCase):
    def setUp(self):
        self.entities = [
            Entity("1", {"name": "John Doe", "city": "New York"}),
            Entity("2", {"name": "Jane Smith", "city": "Los Angeles"}),
            Entity("3", {"name": "Jon Doe", "city": "New York"}),  # Similar to John Doe
            Entity("4", {"name": "Alice Brown", "city": "Chicago"}),
            Entity("5", {"name": "Bob Johnson", "city": "Boston"}),
        ]
        self.blocker = QGramBlocker(q=2, key_func=default_key_func, threshold=2)

    def test_create_blocks(self):
        blocks = self.blocker.create_blocks(self.entities)

        # Check if we have blocks
        self.assertGreater(len(blocks), 0)

        # Check if all entities are in at least one block
        all_entities = set()
        for block in blocks.values():
            all_entities.update(block)
        self.assertEqual(len(all_entities), len(self.entities))

        # Check if similar entities are in the same block
        john_block = None
        for block in blocks.values():
            if self.entities[0] in block:
                john_block = block
                break
        self.assertIsNotNone(john_block)

    def test_q_gram_generation(self):
        q_grams = self.blocker._generate_q_grams("hello")
        expected_q_grams = [" h", "he", "el", "ll", "lo", "o "]
        self.assertEqual(q_grams, expected_q_grams)

    def test_custom_key_func(self):
        custom_key_func = lambda e: e.attributes["name"]
        custom_blocker = QGramBlocker(q=2, key_func=custom_key_func, threshold=2)
        blocks = custom_blocker.create_blocks(self.entities)

        # Check if entities with similar names are in the same block
        john_block = None
        for block in blocks.values():
            if self.entities[0] in block:
                john_block = block
                break
        self.assertIsNotNone(john_block)
        self.assertIn(self.entities[2], john_block)  # Jon Doe should be in the same block as John Doe


if __name__ == "__main__":
    unittest.main()

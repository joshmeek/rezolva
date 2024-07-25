import unittest

from rezolva.blockers.sorted_neighborhood_blocker import (
    SortedNeighborhoodBlocker, default_key_func)
from rezolva.core.base import Entity


class TestSortedNeighborhoodBlocker(unittest.TestCase):
    def setUp(self):
        self.entities = [
            Entity("1", {"name": "John Doe", "city": "New York"}),
            Entity("2", {"name": "Jane Smith", "city": "Los Angeles"}),
            Entity("3", {"name": "Bob Johnson", "city": "Chicago"}),
            Entity("4", {"name": "Alice Brown", "city": "New York"}),
            Entity("5", {"name": "Charlie Davis", "city": "Boston"}),
        ]
        self.blocker = SortedNeighborhoodBlocker(default_key_func, window_size=3)

    def test_create_blocks(self):
        blocks = self.blocker.create_blocks(self.entities)

        # Check if we have the expected number of blocks
        self.assertEqual(len(blocks), len(self.entities))

        # Check if all entities are in at least one block
        all_entities = set()
        for block in blocks.values():
            all_entities.update(block)
        self.assertEqual(len(all_entities), len(self.entities))

        # Check if entities are in the correct blocks
        for entity in self.entities:
            key = default_key_func(entity)
            self.assertIn(entity, blocks[key])

        # Check if the window size is respected
        for block in blocks.values():
            self.assertLessEqual(len(block), self.blocker.window_size)

    def test_custom_key_func(self):
        custom_key_func = lambda e: e.attributes["city"][0].lower()
        custom_blocker = SortedNeighborhoodBlocker(custom_key_func, window_size=3)
        blocks = custom_blocker.create_blocks(self.entities)

        # Check if entities with the same city initial are in the same block
        self.assertIn(self.entities[0], blocks["n"])  # New York
        self.assertIn(self.entities[3], blocks["n"])  # New York
        self.assertIn(self.entities[1], blocks["l"])  # Los Angeles


if __name__ == "__main__":
    unittest.main()

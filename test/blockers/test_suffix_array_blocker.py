import unittest

from rezolva.blockers.suffix_array_blocker import (SuffixArrayBlocker,
                                                   default_key_func)
from rezolva.core.base import Entity


class TestSuffixArrayBlocker(unittest.TestCase):
    def setUp(self):
        self.entities = [
            Entity("1", {"name": "John Doe", "city": "New York"}),
            Entity("2", {"name": "Jane Smith", "city": "Los Angeles"}),
            Entity("3", {"name": "John Smith", "city": "Chicago"}),
            Entity("4", {"name": "Alice Johnson", "city": "New York"}),
            Entity("5", {"name": "Bob Williams", "city": "Los Angeles"}),
        ]
        self.blocker = SuffixArrayBlocker(default_key_func, min_suffix_length=4)

    def test_create_blocks(self):
        blocks = self.blocker.create_blocks(self.entities)

        # Check if we have blocks
        self.assertGreater(len(blocks), 0)

        # Check if all entities are in at least one block
        all_entities = set()
        for block in blocks.values():
            all_entities.update(block)
        self.assertEqual(len(all_entities), len(self.entities))

        # Check if entities with common suffixes are in the same block
        new_york_block = blocks.get("new york")
        self.assertIsNotNone(new_york_block)
        self.assertIn(self.entities[0], new_york_block)
        self.assertIn(self.entities[3], new_york_block)

        los_angeles_block = blocks.get("los angeles")
        self.assertIsNotNone(los_angeles_block)
        self.assertIn(self.entities[1], los_angeles_block)
        self.assertIn(self.entities[4], los_angeles_block)

    def test_build_suffix_array(self):
        suffix_array = self.blocker._build_suffix_array(self.entities)

        # Check if all suffixes are present
        self.assertIn("john doe new york", suffix_array)
        self.assertIn("new york", suffix_array)
        self.assertIn("york", suffix_array)

        # Check if indices are correct
        self.assertEqual(suffix_array["john doe new york"], [0])
        self.assertEqual(set(suffix_array["new york"]), {0, 3})

    def test_custom_key_func(self):
        custom_key_func = lambda e: e.attributes["name"].lower()
        custom_blocker = SuffixArrayBlocker(custom_key_func, min_suffix_length=4)
        blocks = custom_blocker.create_blocks(self.entities)

        # Check if entities with common name suffixes are in the same block
        smith_block = blocks.get("smith")
        self.assertIsNotNone(smith_block)
        self.assertIn(self.entities[1], smith_block)  # Jane Smith
        self.assertIn(self.entities[2], smith_block)  # John Smith


if __name__ == "__main__":
    unittest.main()

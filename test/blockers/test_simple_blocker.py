import unittest

from rezolva.blockers.simple_blocker import SimpleBlocker
from rezolva.core.base import Entity


class TestSimpleBlocker(unittest.TestCase):
    def setUp(self):
        self.blocker = SimpleBlocker(lambda e: e.attributes["category"])

    def test_create_blocks(self):
        entities = [
            Entity("1", {"name": "iPhone 12", "category": "Smartphone"}),
            Entity("2", {"name": "Galaxy S21", "category": "Smartphone"}),
            Entity("3", {"name": "MacBook Pro", "category": "Laptop"}),
            Entity("4", {"name": "Dell XPS", "category": "Laptop"}),
            Entity("5", {"name": "AirPods", "category": "Audio"}),
        ]

        blocks = self.blocker.create_blocks(entities)

        self.assertEqual(len(blocks), 3)
        self.assertIn("Smartphone", blocks)
        self.assertIn("Laptop", blocks)
        self.assertIn("Audio", blocks)
        self.assertEqual(len(blocks["Smartphone"]), 2)
        self.assertEqual(len(blocks["Laptop"]), 2)
        self.assertEqual(len(blocks["Audio"]), 1)

    def test_empty_input(self):
        blocks = self.blocker.create_blocks([])
        self.assertEqual(len(blocks), 0)

    def test_single_entity(self):
        entity = Entity("1", {"name": "iPhone 12", "category": "Smartphone"})
        blocks = self.blocker.create_blocks([entity])
        self.assertEqual(len(blocks), 1)
        self.assertIn("Smartphone", blocks)
        self.assertEqual(len(blocks["Smartphone"]), 1)

    def test_custom_blocking_key(self):
        blocker = SimpleBlocker(lambda e: e.attributes["name"][0].upper())
        entities = [
            Entity("1", {"name": "iPhone 12", "category": "Smartphone"}),
            Entity("2", {"name": "Galaxy S21", "category": "Smartphone"}),
            Entity("3", {"name": "MacBook Pro", "category": "Laptop"}),
        ]

        blocks = blocker.create_blocks(entities)

        self.assertEqual(len(blocks), 3)
        self.assertIn("I", blocks)
        self.assertIn("G", blocks)
        self.assertIn("M", blocks)
        self.assertEqual(len(blocks["I"]), 1)
        self.assertEqual(len(blocks["G"]), 1)
        self.assertEqual(len(blocks["M"]), 1)


if __name__ == "__main__":
    unittest.main()

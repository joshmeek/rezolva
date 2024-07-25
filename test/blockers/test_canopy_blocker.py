import unittest

from rezolva.blockers.canopy_blocker import CanopyBlocker, euclidean_distance
from rezolva.core.base import Entity


class TestCanopyBlocker(unittest.TestCase):
    def setUp(self):
        self.entities = [
            Entity("1", {"x": 1, "y": 1}),
            Entity("2", {"x": 2, "y": 2}),
            Entity("3", {"x": 10, "y": 10}),
            Entity("4", {"x": 11, "y": 11}),
            Entity("5", {"x": 20, "y": 20}),
        ]
        self.blocker = CanopyBlocker(euclidean_distance, t1=5, t2=2)

    def test_create_blocks(self):
        blocks = self.blocker.create_blocks(self.entities)

        # Check if we have the expected number of blocks
        self.assertGreaterEqual(len(blocks), 2)
        self.assertLessEqual(len(blocks), 5)

        # Check if all entities are in at least one block
        all_entities = set()
        for block in blocks.values():
            all_entities.update(block)
        self.assertEqual(len(all_entities), len(self.entities))

        # Check if close entities are in the same block
        for block in blocks.values():
            if len(block) > 1:
                for i in range(len(block)):
                    for j in range(i + 1, len(block)):
                        distance = euclidean_distance(block[i], block[j])
                        self.assertLess(distance, self.blocker.t1)


if __name__ == "__main__":
    unittest.main()

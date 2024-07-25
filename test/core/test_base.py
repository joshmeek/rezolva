import unittest

from rezolva.core.base import (Blocker, DataLoader, DataSaver, Entity, Matcher,
                               ModelBuilder, Preprocessor)


class TestEntity(unittest.TestCase):
    def test_entity_creation(self):
        entity = Entity("1", {"name": "John", "age": 30})
        self.assertEqual(entity.id, "1")
        self.assertEqual(entity.attributes, {"name": "John", "age": 30})


class TestAbstractClasses(unittest.TestCase):
    def test_abstract_methods(self):
        abstract_classes = [Preprocessor, ModelBuilder, Matcher, Blocker, DataLoader, DataSaver]
        for cls in abstract_classes:
            with self.assertRaises(TypeError):
                cls()


if __name__ == "__main__":
    unittest.main()

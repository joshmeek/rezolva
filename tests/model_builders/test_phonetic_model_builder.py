import unittest

from tiny_er.core.base import Entity
from tiny_er.model_builders.phonetic_model_builder import PhoneticModelBuilder


class TestPhoneticModelBuilder(unittest.TestCase):
    def setUp(self):
        self.model_builder = PhoneticModelBuilder(['name'])

    def test_train(self):
        entities = [
            Entity("1", {"name": "John Smith"}),
            Entity("2", {"name": "Jon Smyth"})
        ]
        model = self.model_builder.train(entities)

        self.assertIn('entities', model)
        self.assertIn('phonetic_index', model)
        self.assertEqual(len(model['entities']), 2)
        self.assertIn('J500', model['phonetic_index'])
        self.assertIn('S530', model['phonetic_index'])

    def test_update(self):
        initial_entities = [Entity("1", {"name": "John Smith"})]
        model = self.model_builder.train(initial_entities)

        new_entities = [Entity("2", {"name": "Jane Doe"})]
        updated_model = self.model_builder.update(model, new_entities)

        self.assertEqual(len(updated_model['entities']), 2)
        self.assertIn('J500', updated_model['phonetic_index'])
        self.assertIn('D000', updated_model['phonetic_index'])

    def test_soundex(self):
        self.assertEqual(self.model_builder._soundex("Robert"), "R163")
        self.assertEqual(self.model_builder._soundex("Rupert"), "R163")
        self.assertEqual(self.model_builder._soundex("Ashcraft"), "A261")
        self.assertEqual(self.model_builder._soundex("Ashcroft"), "A261")
        self.assertEqual(self.model_builder._soundex(""), "0000")

if __name__ == '__main__':
    unittest.main()
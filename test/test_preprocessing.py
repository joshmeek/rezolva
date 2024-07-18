import unittest
from tiny_er.core.data_structures import Entity
from tiny_er.preprocessing.normalizer import Normalizer
from tiny_er.preprocessing.standardizer import Standardizer
from tiny_er.preprocessing.cleaner import Cleaner

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.entity = Entity("1", {
            "name": "John DOE",
            "age": "30",
            "address": "123 Main St., Apt. 4B",
            "phone": "123-456-7890"
        })

    def test_normalizer(self):
        config = {
            "lowercase": True,
            "remove_punctuation": True,
            "remove_whitespace": True
        }
        normalizer = Normalizer(config)
        normalized = normalizer.normalize(self.entity)
        self.assertEqual(normalized.attributes["name"], "john doe")
        self.assertEqual(normalized.attributes["address"], "123 main st apt 4b")
        self.assertEqual(normalized.attributes["phone"], "1234567890")

    def test_standardizer(self):
        config = {
            "name": {
                "john doe": "John Doe",
                "jane doe": "Jane Doe"
            },
            "age": {
                "30": "30-35",
                "25": "25-30"
            }
        }
        standardizer = Standardizer(config)
        standardized = standardizer.standardize(self.entity)
        self.assertEqual(standardized.attributes["name"], "John Doe")
        self.assertEqual(standardized.attributes["age"], "30-35")

    def test_cleaner(self):
        config = {
            "remove_special_characters": True,
            "remove_digits": False,
            "max_length": {
                "name": 10,
                "address": 20
            }
        }
        cleaner = Cleaner(config)
        cleaned = cleaner.clean(self.entity)
        self.assertEqual(cleaned.attributes["name"], "John DOE")
        self.assertEqual(cleaned.attributes["address"], "123 Main St Apt 4B")
        self.assertEqual(cleaned.attributes["phone"], "1234567890")

if __name__ == '__main__':
    unittest.main()
import unittest

from rezolva.core.base import Entity
from rezolva.preprocessors.simple_preprocessor import SimplePreprocessor


class TestSimplePreprocessor(unittest.TestCase):
    def test_preprocess(self):
        def uppercase(value):
            return value.upper() if isinstance(value, str) else value

        preprocessor = SimplePreprocessor([uppercase])
        entity = Entity("1", {"name": "John", "age": 30})
        processed_entity = preprocessor.preprocess(entity)

        self.assertEqual(processed_entity.id, "1")
        self.assertEqual(processed_entity.attributes["name"], "JOHN")
        self.assertEqual(processed_entity.attributes["age"], 30)

    def test_add_remove_preprocessing_function(self):
        preprocessor = SimplePreprocessor()

        def dummy_func(value):
            return value

        preprocessor.add_preprocessing_function(dummy_func)
        self.assertIn(dummy_func, preprocessor.preprocessing_functions)

        preprocessor.remove_preprocessing_function(dummy_func)
        self.assertNotIn(dummy_func, preprocessor.preprocessing_functions)


if __name__ == "__main__":
    unittest.main()

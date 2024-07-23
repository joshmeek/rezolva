import os
import pickle
import unittest

from start_er.core.base import Entity
from start_er.data_handlers.pickle_handlers import (PickleDataLoader,
                                                   PickleDataSaver)


class TestPickleHandlers(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_data.pickle'
        self.test_data = [
            Entity("1", {"name": "John Doe", "age": 30}),
            Entity("2", {"name": "Jane Smith", "age": 25})
        ]
        with open(self.test_file, 'wb') as f:
            pickle.dump(self.test_data, f)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_pickle_data_loader(self):
        loader = PickleDataLoader()
        entities = loader.load(self.test_file)

        self.assertEqual(len(entities), 2)
        self.assertIsInstance(entities[0], Entity)
        self.assertEqual(entities[0].id, "1")
        self.assertEqual(entities[0].attributes["name"], "John Doe")
        self.assertEqual(entities[1].id, "2")
        self.assertEqual(entities[1].attributes["age"], 25)

    def test_pickle_data_saver(self):
        entities = [
            Entity("3", {"name": "Alice Johnson", "age": 35}),
            Entity("4", {"name": "Bob Williams", "age": 40})
        ]
        saver = PickleDataSaver()
        output_file = 'output_test_data.pickle'
        saver.save(entities, output_file)

        # Check if the file was created
        self.assertTrue(os.path.exists(output_file))

        # Load the saved data and verify
        with open(output_file, 'rb') as f:
            saved_data = pickle.load(f)

        self.assertEqual(len(saved_data), 2)
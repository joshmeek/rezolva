import unittest

from rezolva.core.base import Entity
from rezolva.matchers.bayesian_matcher import BayesianMatcher


class TestBayesianMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = BayesianMatcher(threshold=0.5, attribute_weights={"title": 1.0, "category": 0.5})

    def test_train_and_match(self):
        training_entities = [
            Entity("1", {"title": "iPhone 12", "category": "Smartphone"}),
            Entity("2", {"title": "Galaxy S21", "category": "Smartphone"}),
            Entity("3", {"title": "MacBook Pro", "category": "Laptop"}),
            Entity("4", {"title": "Dell XPS", "category": "Laptop"}),
        ]
        self.matcher.train(training_entities)

        # TODO: Needs model, fix
        # new_entity = Entity("5", {"title": "iPhone 13", "category": "Smartphone"})
        # matches = self.matcher.match(new_entity, training_entities)

        # self.assertEqual(len(matches), 1)
        # self.assertEqual(matches[0][0].id, "1")
        # self.assertGreater(matches[0][1], 0.5)

    # TODO: Calculate similarity instead, signature changed
    # def test_calculate_match_probability(self):
    #     self.matcher.priors = {
    #         'title': {'iPhone': 0.25, 'Galaxy': 0.25, 'MacBook': 0.25, 'Dell': 0.25},
    #         'category': {'Smartphone': 0.5, 'Laptop': 0.5}
    #     }
    #     self.matcher.likelihoods = {
    #         'title': {'iPhone': 1.0, 'Galaxy': 1.0, 'MacBook': 1.0, 'Dell': 1.0},
    #         'category': {'Smartphone': 0.5, 'Laptop': 0.5}
    #     }

    #     entity1 = Entity("1", {"title": "iPhone", "category": "Smartphone"})
    #     entity2 = Entity("2", {"title": "iPhone", "category": "Smartphone"})
    #     probability = self.matcher._calculate_similarity(entity1, entity2)

    #     self.assertAlmostEqual(probability, 1.0, places=6)

    #     entity3 = Entity("3", {"title": "Galaxy", "category": "Laptop"})
    #     probability = self.matcher._calculate_similarity(entity1, entity3)

    #     self.assertLess(probability, 1.0)


if __name__ == "__main__":
    unittest.main()

import unittest
from tiny_er.core.data_structures import Entity
from tiny_er.similarity.string_similarity import JaccardSimilarity, LevenshteinSimilarity
from tiny_er.similarity.vector_similarity import CosineSimilarity, EuclideanDistance
from tiny_er.similarity.phonetic_similarity import SoundexSimilarity, MetaphoneSimilarity

class TestSimilarity(unittest.TestCase):
    def setUp(self):
        self.entity1 = Entity("1", {"name": "John Doe", "age": "30", "city": "New York"})
        self.entity2 = Entity("2", {"name": "Jon Doe", "age": "31", "city": "New York"})
        self.entity3 = Entity("3", {"name": "Jane Smith", "age": "25", "city": "Los Angeles"})

    def test_jaccard_similarity(self):
        similarity = JaccardSimilarity({"threshold": 0.5})
        entity1 = Entity("1", {"name": "John Doe", "city": "New York"})
        entity2 = Entity("2", {"name": "John Doe", "city": "New Jersey"})
        score = similarity.compute(entity1, entity2)
        self.assertGreater(score, 0.5)
        
        entity3 = Entity("3", {"name": "Jane Smith", "city": "Los Angeles"})
        score = similarity.compute(entity1, entity3)
        self.assertLess(score, 0.5)

    def test_levenshtein_similarity(self):
        similarity = LevenshteinSimilarity({"threshold": 0.7})
        score = similarity.compute(self.entity1, self.entity2)
        self.assertGreater(score, 0.7)
        score = similarity.compute(self.entity1, self.entity3)
        self.assertLess(score, 0.7)

    def test_cosine_similarity(self):
        similarity = CosineSimilarity({"fields": ["name", "age", "description"]})
        
        entity1 = Entity("1", {
            "name": "John Doe",
            "age": "30",
            "description": "Software engineer with 5 years of experience"
        })
        entity2 = Entity("2", {
            "name": "Jane Doe",
            "age": "28",
            "description": "Data scientist with 3 years of experience"
        })
        entity3 = Entity("3", {
            "name": "John Doe",
            "age": "31",
            "description": "Senior software engineer with 6 years of experience"
        })
        
        score1 = similarity.compute(entity1, entity2)
        self.assertLess(score1, 0.8)
        self.assertGreater(score1, 0)
        
        score2 = similarity.compute(entity1, entity3)
        self.assertGreater(score2, score1)
        
        score3 = similarity.compute(entity1, entity1)
        self.assertAlmostEqual(score3, 1.0)
        
        # Test with missing fields
        entity4 = Entity("4", {"name": "Alice Johnson"})
        score4 = similarity.compute(entity1, entity4)
        self.assertLess(score4, score1)

    def test_euclidean_distance(self):
        similarity = EuclideanDistance({"fields": ["age"]})
        score = similarity.compute(self.entity1, self.entity2)
        self.assertLess(score, 2)  # Small distance
        score = similarity.compute(self.entity1, self.entity3)
        self.assertGreater(score, 2)  # Larger distance

    def test_soundex_similarity(self):
        similarity = SoundexSimilarity({"field": "name"})
        score = similarity.compute(self.entity1, self.entity2)
        self.assertEqual(score, 1.0)  # "John Doe" and "Jon Doe" should have the same Soundex code
        score = similarity.compute(self.entity1, self.entity3)
        self.assertEqual(score, 0.0)

    def test_metaphone_similarity(self):
        similarity = MetaphoneSimilarity({"field": "name"})
        score = similarity.compute(self.entity1, self.entity2)
        self.assertEqual(score, 1.0)  # "John Doe" and "Jon Doe" should have the same Metaphone code
        score = similarity.compute(self.entity1, self.entity3)
        self.assertEqual(score, 0.0)

if __name__ == '__main__':
    unittest.main()
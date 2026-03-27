import numpy as np
from django.test import TestCase
from .services.cache import SemanticCache

class CacheTest(TestCase):
    def setUp(self):
        """Set up a real test case with 768-dim vectors."""
        self.question = "What is the termination notice period?"
        self.answer = "It is 30 days as per clause 4.2."
        # Standardize on 768-dim float32
        self.vector = np.random.rand(768).astype(np.float32)
        
        # Save to cache
        SemanticCache.set_hit(self.question, self.answer, self.vector)

    def test_cache_hit(self):
        """Verify that the same vector returns the correct answer."""
        cached_answer = SemanticCache.get_hit(self.vector)
        self.assertEqual(cached_answer, self.answer)

    def test_cache_miss(self):
        """Verify that a different vector returns None."""
        random_vector = np.random.rand(768).astype(np.float32)
        cached_answer = SemanticCache.get_hit(random_vector)
        self.assertIsNone(cached_answer)
import unittest
from io_tools.cache import CacheObject

class TestCache(unittest.TestCase):
    def test_cache(self):
        cache = CacheObject('cache.json')
        cache['key1'] = 'value1'
        self.assertEqual(cache['key1'], 'value1')
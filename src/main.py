"""
you can add some example code here
"""
from io_tools.cache import CacheObject

cache = CacheObject('cache.json')

def test():
    cache['rom'] = 'kcc'
    print(cache['rom'])

if __name__ == "__main__":
    test()
    
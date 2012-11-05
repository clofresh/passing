# Internal async implementation
import atexit
from multiprocessing.pool import ThreadPool

DEFAULT_POOL_SIZE = 10
_pool = None

def init_pool(pool_size=None):
    global _pool, DEFAULT_POOL_SIZE
    pool_size = pool_size or DEFAULT_POOL_SIZE
    if _pool:
        raise Exception("Pool is already initialized")
    _pool = ThreadPool(pool_size)
    atexit.register(close_pool)
    return _pool

def close_pool():
    global _pool
    _pool.close()
    _pool.join()

def get_pool():
    global _pool
    if _pool is None:
        _pool = init_pool()
    return _pool

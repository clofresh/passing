# Try to find the best wireformat available
try:
    import msgpack as wireformat
except ImportError:
    try:
        import simplejson as wireformat
    except ImportError:
        try:
            import json as wireformat
        except ImportError:
            import cPickle as wireformat

loads = wireformat.loads
dumps = wireformat.dumps

from passing.base import Passing
from passing import wireformat

class RedisPassing(Passing):
    def __init__(self, name, redis_conn):
        Passing.__init__(self, name)
        self.redis_conn = redis_conn
        self.pubsub = redis_conn.pubsub()
        self.pubsub.subscribe(name)

    def register(self, groups):
        self.groups = groups
        self.pubsub.subscribe(groups)

    def _send(self, recipient, message):
        self.redis_conn.publish(recipient, wireformat.dumps(message))

    def _receive(self):
        for msg in self.pubsub.listen():
            if msg['type'] == 'message':
                return wireformat.loads(msg['data'])

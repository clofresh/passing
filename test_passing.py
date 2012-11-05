import os
import signal
import sys
import time

from passing.base import Timeout
from passing.redis import RedisPassing
import redis

n = 4
print 'creating {0} children'.format(n)
children = []
main_p = RedisPassing('parent', redis.Redis())

for i in range(n):
    pid = os.fork()
    child_name = 'child-{0}'.format(i)
    if pid == 0:
        # Child
        p = RedisPassing(child_name, redis.Redis())
        print '{0}: started, waiting for ping'.format(p.name)
        msg_type, sender = p.receive()
        if msg_type == 'ping':
            print '{0}: received ping from {1}, sending pong'.format(p.name, sender)
            p.send(sender, ('pong', p.name))
        else:
            raise Exception("{0}: Unexpected mesage: {1}".format(msg_type))
        print '{0}: waiting for stop message'.format(p.name)
        while True:
            try:
                msg_type = p.receive(5)
            except Timeout:
                print '{0}: got bored of waiting, giving up'.format(p.name)
                sys.exit(1)
            if msg_type == 'stop':
                print '{0}: received stop, stopping'.format(p.name)
                sys.exit(0)
            else:
                raise Exception("{0}: Unexpected mesage: {1}".format(msg_type))
    else:
        # Parent
        children.append(child_name)

time.sleep(1)

for child_name in children:
    print '{0}: sending ping to {1}'.format(main_p.name, child_name)
    main_p.send(child_name, ('ping', main_p.name))

num_left = n
while num_left > 0:
    print '{0}: waiting for {1} children to pong'.format(main_p.name, num_left)
    message_type, name = main_p.receive()
    if message_type == 'pong':
        print '{0}: received pong from {1}, sending stop message'.format(main_p.name, name)
        main_p.send(name, 'stop')
        num_left -= 1

print '{0}: done'.format(main_p.name)

import multiprocessing
from abc import ABCMeta, abstractmethod
from passing.async import get_pool

__all__ = ['Timeout', 'Passing']

class Timeout(Exception): pass

class Passing(object):
    ''' Abstract base class for Passing objects. Implement `register`, `_send`,
        and `_receive` in the implementing subclass.
    '''

    __metaclass__ = ABCMeta
    def __init__(self, name, *args, **kwargs):
        self.name = name

    @abstractmethod
    def register(self, groups):
        ''' Register the Passing process to a group or list of groups
        '''

    def send(self, recipient, message):
        ''' Asynchronously send `message` to `recipient`
        '''
        get_pool().apply_async(self._send, (recipient, message))

    def receive(self, timeout=None):
        ''' Synchronously wait `timeout` seconds for a message. If a message
            arrives by then, return it, otherwise, raise a `Timeout`.
        '''
        promise = get_pool().apply_async(self._receive)
        try:
            data = promise.get(timeout)
        except multiprocessing.TimeoutError:
            raise Timeout()
        else:
            return data

    @abstractmethod
    def _send(recipient, message):
        raise NotImplementedError()

    @abstractmethod
    def _receive(timeout=None):
        raise NotImplementedError()


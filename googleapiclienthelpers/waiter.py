import time

__all__ = [
    'Waiter',
]


class Waiter(object):
    '''Wait for a resource to reach a desired state.

    This class implements a generic way to wait for an operation to
    reach a desired state.

    To use: create a new instance by providing a callable and the
    arguments that it requires.  Then, call wait() and the Waiter will
    poll the callable until the desired status is reached.

    The callable you pass must have a .execute() method, like the
    Resource objects returned by googleapiclient.

    For example, you might start an instance and wait until it reaches
    the RUNNING status:
    >>> instances = build_subresource('compute.instances', 'v1')
    >>> instances.insert(...)
    >>> waiter = Waiter(instances.get, project=..., zone=..., instance=...)
    >>> waiter.wait('status', 'RUNNING')

    '''
    def __init__(self, func, *args, **kargs):
        '''Construct a new Waiter

        Args:
          func: callable, the callable that returns the status.  Most
                of the time this will be a googleapiclient Resource method.
          *args: positional arguments to be passed to func.
          **kargs: keyword arguments to be passed to func.

        '''
        self.func = func
        self.args = args
        self.kargs = kargs

    def wait(self, field, value, retries=60, interval=2):
        '''Wait until an object reached the desired status

        When called, the Waiter will invoke the callable provided at
        construction and capture its return.  The Waiter extracts
        field, and checks if it's equal to value.  If it is, the full
        response from the callable is returned.

        wait() handles three kinds of field parameter:
          * dict-like return where field is a string that specified a key.
          * object-like return where field is a string naming an attribute.
          * any kind of return where field is a one-place callable that extracts
            the needed data to compare.

        Args:
          field: string or callable, the data to extract.
          value: varies, the value indicating the desired state.
          retries: int, maximum number of times to poll.
          interval: float, time to sleep between polls.

        '''
        count = 0

        while count < retries:
            response = self.func(*self.args, **self.kargs).execute()

            # field might be a dict key
            try:
                if response[field] == value:
                    return response
            except KeyError:
                pass

            # field might be an object attribute
            try:
                if getattr(response, field) == value:
                    return response
            except (AttributeError, TypeError):
                pass

            # field might be a callable that finds the right thing
            try:
                if field(response) == value:
                    return response
            except TypeError:
                pass

            # either the desired status hasn't been reached, or the
            # user passed something nonsensical as field/value
            time.sleep(interval)
            count += 1

        raise ValueError('Never received desired value %s' % value)

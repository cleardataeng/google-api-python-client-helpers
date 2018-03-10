from googleapiclienthelpers.waiter import Waiter
import pytest


class Counter(object):
    '''Count by one when the increment method is called

    The only purpose of this class is to test Waiter's functionality.
    '''
    def __init__(self): self.count = 0

    def __getitem__(self, item):
        if item != 'value':
            raise KeyError(item)

        return self.count

    def __contains__(self, key):
        return key == 'value'

    def increment(self):
        return self

    def execute(self):
        self.count += 1
        return self


def _do_wait(waiter, method, expect):
    if method == 'attr':
        return waiter.wait('count', expect, interval=0)
    elif method == 'key':
        return waiter.wait('value', expect, interval=0)
    elif method == 'callable':
        return waiter.wait(lambda x: x.count, expect, interval=0)


@pytest.mark.parametrize('expect', (4, 61))
@pytest.mark.parametrize('method', ('attr', 'key', 'callable'))
def test_waiter(expect, method):
    c = Counter()
    waiter = Waiter(c.increment)

    if expect > 10:
        with pytest.raises(ValueError):
            _do_wait(waiter, method, expect)
        assert c.count == 60

    else:
        result = _do_wait(waiter, method, expect)
        assert result.count == expect
        assert result is c

#!/usr/bin/env python
'''
Inspired by the post "Populating a sparse list with random 1's" on
StackOverflow:

    http://stackoverflow.com/q/17522753/78845

A "sparse list" is a list where most (say, more than 95% of) values will be
None (or some other default) and for reasons of memory efficiency you don't
wish to store these. cf. Sparse array:

    http://en.wikipedia.org/wiki/Sparse_array
'''

try:
    xrange
except NameError:
    # On Python 3, range() is equivalent to Python 2's xrange()
    xrange = range

from six import iteritems, itervalues
from six.moves import zip_longest


class SparseList(object):
    '''
    This implementation has a similar interface to Python's built-in list but
    stores the data in a dictionary to conserve memory.
    '''

    def __init__(self, arg, default_value=None):
        self.default = default_value
        self.elements = {}
        if isinstance(arg, int):
            self.size = int(arg)
        elif isinstance(arg, dict):
            self.__initialise_from_dict(arg)
        else:
            self.__initialise_from_iterable(arg)

    def __len__(self):
        return self.size

    def __setitem__(self, index, value):
        try:
            if index.start:
                self.size = index.start + len(value)
            s = slice(index.start, index.stop, index.step).indices(self.size)
            for v, i in enumerate(xrange(*s)):
                self.__setitem__(i, value[v])
        except AttributeError:
            self.elements[index] = value
            self.size = max(index + 1, self.size)

    def __getitem__(self, index):
        try:
            s = slice(index.start, index.stop, index.step).indices(self.size)
            return [self[i] for i in xrange(*s)]
        except AttributeError:
            i = slice(index).indices(self.size)[1]
            return self.elements.get(i, self.default)

    def __setslice__(self, start, stop, vals):
        '''
        __setslice__ is deprecated, but kept here for backwards compatibility
        '''
        return self.__setitem__(slice(start, stop), vals)

    def __delitem__(self, item):
        if isinstance(item, slice):
            indices = xrange(*item.indices(self.size))
        else:
            indices = (item, )

        for i in indices:
            try:
                del self.elements[i]
            except KeyError:
                pass

    def __delslice__(self, start, stop):
        '''
        __delslice__ is deprecated, but kept here for backwards compatibility
        '''
        return self.__delitem__(slice(start, stop))

    def __iter__(self):
        for index in xrange(self.size):
            yield self[index]

    def __contains__(self, index):
        return index in itervalues(self.elements)

    def __repr__(self):
        return '[{}]'.format(', '.join([str(e) for e in self]))

    def __add__(self, other):
        result = self[:]
        return result.__iadd__(other)

    def __iadd__(self, other):
        for element in other:
            self.append(element)
        return self

    def append(self, element):
        '''
        append element, increasing size by exactly one
        '''
        self.elements[self.size] = element
        self.size += 1

    push = append

    def __initialise_from_dict(self, arg):
        def __convert_and_size(key):
            try:
                key = int(key)
            except ValueError:
                raise ValueError('Invalid key: {}'.format(key))
            self.size = max(key + 1, self.size)
            return key
        self.size = 0
        self.elements = {__convert_and_size(k): v for k, v in iteritems(arg)}

    def __initialise_from_iterable(self, arg):
        self.elements = {k: v for k, v in enumerate(arg)}
        self.size = len(self.elements)

    def __eq__(self, other):
        return all(a == b for a, b in zip_longest(self, other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return any(a < b for a, b in zip_longest(self, other))

    def __ge__(self, other):
        return not self.__lt__(other)

    def __mul__(self, multiplier):
        result = []
        for _ in xrange(multiplier):
            result += self[:]
        return result

    def count(self, value):
        '''
        return number of occurrences of value
        '''
        return sum(v == value for v in itervalues(self.elements)) + (
            self.size - len(self.elements) if value == self.default else 0
        )

    def extend(self, iterable):
        '''
        extend sparse_list by appending elements from the iterable
        '''
        self.__iadd__(iterable)

    def index(self, value):
        '''
        return first index of value.
        Raises ValueError if the value is not present.
        '''

        if value == self.default:
            for k, v in enumerate(self):
                if v == value:
                    return k
            raise ValueError('{} not in SparseList'.format(value))
        for k, v in iteritems(self.elements):
            if v == value:
                return k
        raise ValueError('{} not in SparseList'.format(value))

    def pop(self):
        '''
        remove and return item at end of SparseList
        Raises IndexError if list is empty.
        '''
        if self.size < 1:
            raise IndexError('pop from empty SparseList')
        value = self[-1]
        del self[-1]
        self.size -= 1
        return value

    def remove(self, value):
        '''
        remove first occurrence of value.
        Raises ValueError if the value is not present.
        '''
        if value == self.default:
            return
        for k, v in iteritems(self.elements):
            if v == value:
                del self.elements[k]
                return
        raise ValueError('{} not in SparseList'.format(value))

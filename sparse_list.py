#!/usr/bin/env python

import itertools


class SparseList(object):
    def __init__(self, arg, default_value=None):
        self.default = default_value
        self.elements = {}
        if isinstance(arg, int):
            self.size = int(arg)
        elif isinstance(arg, dict):
            self.initialise_from_dict(arg)
        else:
            self.initialise_from_iterable(arg)

    def __len__(self):
        return self.size

    def __setitem__(self, index, value):
        self.elements[index] = value
        self.size = max(index + 1, self.size)

    def __getitem__(self, index):
        try:
            s = slice(index.start, index.stop, index.step).indices(self.size)
            return [self[i] for i in xrange(*s)]
        except AttributeError:
            i = slice(index).indices(self.size)[1]
            return self.elements.get(i, self.default)

    def __delitem__(self, index):
        try:
            del self.elements[index]
        except KeyError:
            pass

    def __delslice__(self, start, stop):
        map(self.__delitem__, xrange(start, stop))

    def __iter__(self):
        for index in xrange(self.size):
            yield self[index]

    def __contains__(self, index):
        return index in self.elements.itervalues()

    def __repr__(self):
        return '[{}]'.format(', '.join(map(str, self)))

    def __add__(self, other):
        map(self.append, other)
        return self

    def append(self, element):
        self.elements[self.size] = element
        self.size += 1

    def initialise_from_dict(self, arg):
        def convert_and_size(key):
            try:
                key = int(key)
            except ValueError:
                raise ValueError('Invalid key: {}'.format(key))
            self.size = max(key + 1, self.size)
            return key
        self.size = 0
        self.elements = {convert_and_size(k): v for k, v in arg.iteritems()}

    def initialise_from_iterable(self, arg):
        self.elements = {k: v for k, v in enumerate(arg)}
        self.size = len(self.elements)

    def __eq__(self, other):
        return all(a == b for a, b in itertools.izip_longest(self, other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return any(a < b for a, b in itertools.izip_longest(self, other))

    def __ge__(self, other):
        return not self.__lt__(other)

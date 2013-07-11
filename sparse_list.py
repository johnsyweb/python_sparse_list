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
        def normalise(index):
            if index and index < 0:
                index += self.size
            return index

        try:
            if index.step and index.step < 0:
                raise ValueError(
                    'SparseList does not support negative steps [{}]'.format(
                        index.step))
            return list(itertools.islice(self,
                                         normalise(index.start),
                                         normalise(index.stop),
                                         index.step))
        except AttributeError:
            return self.elements.get(normalise(index), self.default)

    def __iter__(self):
        for index in xrange(self.size):
            yield self.elements.get(index, self.default)

    def __contains__(self, index):
        return index in self.elements.itervalues()

    def __repr__(self):
        return '[{}]'.format(', '.join([str(x) for x in self]))

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

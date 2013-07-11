#!/usr/bin/env python


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

    def __getitem__(self, index):
        return self.elements.get(index, self.default)

    def __iter__(self):
        for i in xrange(self.size):
            yield self[i]

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

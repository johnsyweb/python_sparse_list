#!/usr/bin/env python


class SparseList(object):
    def __init__(self, size, default_value=None):
        self.size = int(size)
        self.default = default_value
        self.elements = {}

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

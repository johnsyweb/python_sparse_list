#!/usr/bin/env python

import sparse_list
import timeit

sl = sparse_list.SparseList(5)
t = timeit.Timer(setup='''
import sparse_list
sl = sparse_list.SparseList(5)
''',
                 stmt='''
repr(sl)
''')

try:
    print t.repeat()
except:
    print t.print_exc()

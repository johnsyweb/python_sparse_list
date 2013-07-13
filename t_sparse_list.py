#!/usr/bin/env python

import unittest
import sparse_list


class TestSparseList(unittest.TestCase):
    def test_init_zero(self):
        sl = sparse_list.SparseList(0)
        self.assertEquals(0, len(sl))

    def test_init_non_zero(self):
        sl = sparse_list.SparseList(10)
        self.assertEquals(10, len(sl))

    def test_init_no_default(self):
        sl = sparse_list.SparseList(1)
        self.assertEquals(None, sl.default)

    def test_init_default(self):
        sl = sparse_list.SparseList(1, 'test')
        self.assertEquals('test', sl.default)

    def test_random_access_write(self):
        sl = sparse_list.SparseList(1)
        sl[0] = 'alice'
        self.assertEquals({0: 'alice'}, sl.elements)

    def test_random_access_read_present(self):
        sl = sparse_list.SparseList(2)
        sl[0] = 'brent'
        self.assertEquals('brent', sl[0])

    def test_random_access_read_absent(self):
        sl = sparse_list.SparseList(2, 'absent')
        sl[1] = 'clint'
        self.assertEquals('absent', sl[0])

    def test_iteration_empty(self):
        sl = sparse_list.SparseList(3)
        l = [element for element in sl]
        self.assertEquals([None, None, None], l)

    def test_iteration_populated(self):
        sl = sparse_list.SparseList(5)
        sl[1], sl[3] = 'a', 'b'
        l = [element for element in sl]
        self.assertEquals([None, 'a', None, 'b', None], l)

    def test_membership_absent(self):
        sl = sparse_list.SparseList(5)
        sl[2], sl[3], = 1, 2
        self.assertEquals(False, 3 in sl)

    def test_membership_present(self):
        sl = sparse_list.SparseList(5)
        sl[2], sl[3], = 1, 2
        self.assertEquals(True, 2 in sl)

    def test_string_representations(self):
        sl = sparse_list.SparseList(5, 0)
        sl[3], sl[4] = 5, 6
        self.assertEquals('[0, 0, 0, 5, 6]', repr(sl))
        self.assertEquals('[0, 0, 0, 5, 6]', str(sl))

    def test_initialisation_by_dict(self):
        sl = sparse_list.SparseList({
            4: 6,
            3: 5,
        }, 0)
        self.assertEquals('[0, 0, 0, 5, 6]', repr(sl))

    def test_initialisation_by_dict_with_non_numeric_key(self):
        self.assertRaises(ValueError, sparse_list.SparseList, {'a': 5})

    def test_initialisation_by_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 4])
        self.assertEquals('[0, 1, 2, 4]', repr(sl))

    def test_initialisation_by_generator(self):
        gen = (x for x in (1, 2, 3))
        sl = sparse_list.SparseList(gen)
        self.assertEquals('[1, 2, 3]', repr(sl))

    def test_access_with_negative_index(self):
        sl = sparse_list.SparseList([0, 1, 2, 4])
        self.assertEquals(4, sl[-1])

    def test_access_with_negative_index_with_no_value(self):
        sl = sparse_list.SparseList(5, 0)
        self.assertEquals(0, sl[-1])

    def test_slice(self):
        sl = sparse_list.SparseList([0, 1, 2, 4], 10)
        self.assertEquals([1, 2], sl[1:3])

    def test_extended_slice(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6, ])
        self.assertEquals([1, 3, 5], sl[1:6:2])

    def test_extended_slice_with_negative_stop(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6, ])
        self.assertEquals([1, 3, 5], sl[1:-1:2])

    def test_slice_reversal_full(self):
        sl = sparse_list.SparseList([1, 2, 3])
        self.assertEquals([3, 2, 1], sl[::-1])

    def test_slice_reversal_empty(self):
        sl = sparse_list.SparseList(4)
        self.assertEquals([None, None, None, None], sl[::-1])

    def test_reversed(self):
        sl = sparse_list.SparseList([1, 2, 3])
        self.assertEquals([3, 2, 1], list(reversed(sl)))

    def test_sorted(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEquals([0, 0, 0, 1, 1], list(sorted(sl)))

    def test_get_out_of_bounds(self):
        sl = sparse_list.SparseList(1)
        self.assertEquals(None, sl[1])

    def test_set_out_of_bounds(self):
        sl = sparse_list.SparseList(1)
        sl[100] = 1
        self.assertEquals(101, len(sl))

    def test_present_item_removal(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        del sl[0]
        self.assertEquals('[0, 0, 0, 0, 1]', repr(sl))

    def test_missing_item_removal(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        del sl[1]
        self.assertEquals('[1, 0, 0, 0, 1]', repr(sl))

    def test_slice_removal(self):
        sl = sparse_list.SparseList(xrange(10), None)
        del sl[3:5]
        self.assertEquals('[0, 1, 2, None, None, 5, 6, 7, 8, 9]', repr(sl))

    def test_append(self):
        sl = sparse_list.SparseList(1, 0)
        sl.append(1)
        self.assertEquals('[0, 1]', repr(sl))

    def test_concatenation(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([4, 5, 6])
        self.assertEquals('[1, 2, 3, 4, 5, 6]', repr(a + b))

if __name__ == '__main__':
    unittest.main()

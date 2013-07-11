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
        pass

    def test_slice(self):
        pass

    def test_extended_slice(self):
        pass

    def test_get_out_of_bounds(self):
        pass

    def test_set_out_of_bounds(self):
        pass


if __name__ == '__main__':
    unittest.main()

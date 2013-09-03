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
        self.assertEquals([None, None, None], list(sl))

    def test_iteration_populated(self):
        sl = sparse_list.SparseList(5)
        sl[1], sl[3] = 'a', 'b'
        self.assertEquals([None, 'a', None, 'b', None], list(sl))

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
        self.assertEquals([0, 0, 0, 5, 6], sl)

    def test_initialisation_by_dict_with_non_numeric_key(self):
        self.assertRaises(ValueError, sparse_list.SparseList, {'a': 5})

    def test_initialisation_by_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 4])
        self.assertEquals([0, 1, 2, 4], sl)

    def test_initialisation_by_generator(self):
        gen = (x for x in (1, 2, 3))
        sl = sparse_list.SparseList(gen)
        self.assertEquals([1, 2, 3], sl)

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
        self.assertEquals([0, 0, 0, 0, 1], sl)

    def test_missing_item_removal(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        del sl[1]
        self.assertEquals([1, 0, 0, 0, 1], sl)

    def test_slice_removal(self):
        sl = sparse_list.SparseList(xrange(10), None)
        del sl[3:5]
        self.assertEquals([0, 1, 2, None, None, 5, 6, 7, 8, 9], sl)

    def test_append(self):
        sl = sparse_list.SparseList(1, 0)
        sl.append(1)
        self.assertEquals([0, 1], sl)

    def test_clone(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = a[:]
        b.append(4)
        self.assertEquals([1, 2, 3], a)
        self.assertEquals([1, 2, 3, 4], b)

    def test_concatenation(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([4, 5, 6])
        c = a + b
        self.assertEquals([1, 2, 3], a)
        self.assertEquals([4, 5, 6], b)
        self.assertEquals([1, 2, 3, 4, 5, 6], c)

    def test_in_place_concatenation(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([4, 5, 6])
        a += b
        self.assertEquals([1, 2, 3, 4, 5, 6], a)
        self.assertEquals([4, 5, 6], b)

    def test_equality(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 2, 3])
        self.assertTrue(a == b)
        self.assertTrue(not a != b)
        self.assertEquals(a, b)
        self.assertTrue(b == a)
        self.assertTrue(not b != a)
        self.assertEquals(b, a)

    def test_inequality_same_length(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 0, 3])
        self.assertTrue(a != b)
        self.assertTrue(not a == b)
        self.assertNotEqual(a, b)
        self.assertTrue(b != a)
        self.assertTrue(not b == a)
        self.assertNotEqual(b, a)

    def test_inequality_left_longer(self):
        a = sparse_list.SparseList([1, 2, 3, 4])
        b = sparse_list.SparseList([1, 2, 3])
        self.assertTrue(a != b)
        self.assertTrue(not (a == b))
        self.assertNotEqual(a, b)
        self.assertTrue(b != a)
        self.assertTrue(not (b == a))
        self.assertNotEqual(b, a)

    def test_less_than(self):
        a = sparse_list.SparseList([1, 2, 3, 0])
        b = sparse_list.SparseList([1, 2, 4, 5])
        self.assertTrue(a < b)
        self.assertFalse(a == b)
        self.assertFalse(a >= b)
        self.assertFalse(a > b)

    def test_greater_than(self):
        a = sparse_list.SparseList([1, 2, 3, 0])
        b = sparse_list.SparseList([1, 2, 4, 5])
        self.assertTrue(b > a)
        self.assertFalse(b == a)
        self.assertFalse(b <= a)
        self.assertFalse(b < a)

    def test_multiply(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        sl4 = sl * 4
        self.assertEquals([1, 0, 0, 0, 1], sl)
        self.assertEquals(
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], sl4)
        self.assertEquals(len(sl) * 4, len(sl4))

    def test_multiply_in_place(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        sl *= 4
        self.assertEquals(
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], sl)

    def test_count_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEquals(2, sl.count(1))

    def test_count_default_value(self):
        sl = sparse_list.SparseList(100, 1)
        sl[5] = 1
        self.assertEquals(100, sl.count(1))

    def test_extend(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.extend((4, 5, 6))
        self.assertEquals([1, 2, 3, 4, 5, 6], sl)

    def test_index_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEquals(0, sl.index(1))

    def test_index_default_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEquals(1, sl.index(0))

    def test_index_absent_default_value(self):
        sl = sparse_list.SparseList([1, 2, 3], 0)
        self.assertRaises(ValueError, sl.index, 0)

    def test_index_absent_value(self):
        sl = sparse_list.SparseList(1, 0)
        self.assertRaises(ValueError, sl.index, 2)

    def test_pop_no_value(self):
        sl = sparse_list.SparseList(4)
        self.assertEquals(None, sl.pop())

    def test_pop_empty(self):
        sl = sparse_list.SparseList(0)
        self.assertRaises(IndexError, sl.pop)

    def test_pop_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        popped = sl.pop()
        self.assertEquals(3, popped)
        self.assertEquals(2, len(sl))
        self.assertEquals([1, 2], sl)

    def test_push_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.push(4)
        self.assertEquals(4, len(sl))
        self.assertEquals([1, 2, 3, 4], sl)

    def test_remove_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.remove(2)
        self.assertEquals(3, len(sl))
        self.assertEquals([1, None, 3], sl)

    def test_remove_only_first_value(self):
        sl = sparse_list.SparseList([2, 2, 3])
        sl.remove(2)
        self.assertEquals(3, len(sl))
        self.assertEquals([None, 2, 3], sl)

    def test_remove_non_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        self.assertRaises(ValueError, sl.remove, 4)

    def test_remove_default_value_does_nothing(self):
        sl = sparse_list.SparseList(4, None)
        sl.remove(None)
        self.assertEquals([None, None, None, None], sl)

if __name__ == '__main__':
    unittest.main()

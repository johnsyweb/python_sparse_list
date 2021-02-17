#!/usr/bin/env python

import unittest
import sparse_list


class TestSparseList(unittest.TestCase):
    def test_init_zero(self):
        sl = sparse_list.SparseList(0)
        self.assertEqual(0, len(sl))
        self.assertEqual(0, sl.population())

    def test_init_non_zero(self):
        sl = sparse_list.SparseList(10)
        self.assertEqual(10, len(sl))
        self.assertEqual(0, sl.population())

    def test_init_no_default(self):
        sl = sparse_list.SparseList(1)
        self.assertEqual(None, sl.default)
        self.assertEqual(0, sl.population())

    def test_init_default(self):
        sl = sparse_list.SparseList(1, 'test')
        self.assertEqual('test', sl.default)
        self.assertEqual(0, sl.population())

    def test_random_access_write(self):
        sl = sparse_list.SparseList(1)
        sl[0] = 'alice'
        self.assertEqual({0: 'alice'}, sl.elements)
        self.assertEqual(1, sl.population())

    def test_random_access_read_present(self):
        sl = sparse_list.SparseList(2)
        sl[0] = 'brent'
        self.assertEqual('brent', sl[0])
        self.assertEqual(1, sl.population())

    def test_random_access_read_absent(self):
        sl = sparse_list.SparseList(2, 'absent')
        sl[1] = 'clint'
        self.assertEqual('absent', sl[0])
        self.assertEqual(1, sl.population())

    def test_iteration_empty(self):
        sl = sparse_list.SparseList(3)
        self.assertEqual([None, None, None], list(sl))

    def test_iteration_populated(self):
        sl = sparse_list.SparseList(5)
        sl[1], sl[3] = 'a', 'b'
        self.assertEqual([None, 'a', None, 'b', None], list(sl))

    def test_membership_absent(self):
        sl = sparse_list.SparseList(5)
        sl[2], sl[3], = 1, 2
        self.assertEqual(False, 3 in sl)

    def test_membership_present(self):
        sl = sparse_list.SparseList(5)
        sl[2], sl[3], = 1, 2
        self.assertEqual(True, 2 in sl)

    def test_string_representations(self):
        sl = sparse_list.SparseList(5, 0)
        sl[3], sl[4] = 5, 6
        self.assertEqual('[0, 0, 0, 5, 6]', repr(sl))
        self.assertEqual('[0, 0, 0, 5, 6]', str(sl))

    def test_initialisation_by_dict(self):
        sl = sparse_list.SparseList({
            4: 6,
            3: 5,
        }, 0)
        self.assertEqual([0, 0, 0, 5, 6], sl)
        self.assertEqual(2, sl.population())

    def test_initialisation_by_dict_does_not_add_defaults(self):
        sl = sparse_list.SparseList({
            3: 0,
            4: 6,
        }, 0)
        self.assertEqual([0, 0, 0, 0, 6], sl)
        self.assertEqual(1, sl.population())

    def test_initialisation_by_dict_with_non_numeric_key(self):
        self.assertRaises(ValueError, sparse_list.SparseList, {'a': 5})

    def test_initialisation_by_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 4])
        self.assertEqual([0, 1, 2, 4], sl)
        self.assertEqual(4, sl.population())

    def test_initialisation_by_list_does_not_add_defaults(self):
        sl = sparse_list.SparseList([0, 1, 2, 4], 0)
        self.assertEqual([0, 1, 2, 4], sl)
        self.assertEqual(3, sl.population())

    def test_initialisation_by_generator(self):
        gen = (x for x in (1, 2, 3))
        sl = sparse_list.SparseList(gen)
        self.assertEqual([1, 2, 3], sl)
        self.assertEqual(3, sl.population())

    def test_access_with_negative_index(self):
        sl = sparse_list.SparseList([0, 1, 2, 4])
        self.assertEqual(4, sl[-1])

    def test_access_with_negative_index_with_no_value(self):
        sl = sparse_list.SparseList(5, 0)
        self.assertEqual(0, sl[-1])

    def test_slice(self):
        sl = sparse_list.SparseList([0, 1, 2, 4], 10)
        self.assertEqual([1, 2], sl[1:3])

    def test_slice_is_sparse_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 4], 10)
        self.assertIsInstance(sl[1:3], sparse_list.SparseList)

    def test_extended_slice(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6])
        self.assertEqual([1, 3, 5], sl[1:6:2])

    def test_extended_slice_is_sparse_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6])
        self.assertIsInstance(sl[1:6:2], sparse_list.SparseList)

    def test_extended_slice_with_negative_stop(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6])
        self.assertEqual([1, 3, 5], sl[1:-1:2])

    def test_slice_reversal_full(self):
        sl = sparse_list.SparseList([1, 2, 3])
        self.assertEqual([3, 2, 1], sl[::-1])

    def test_slice_reversal_empty(self):
        sl = sparse_list.SparseList(4)
        self.assertEqual([None, None, None, None], sl[::-1])

    def test_default_slice(self):
        sl = sparse_list.SparseList(23)
        sl[0:2] = (1,2)
        self.assertEqual([None, None], sl[2:4])

    def test_slice_list_size(self):
        initial_size = 20
        sl = sparse_list.SparseList(initial_size)
        sample_tuple = (1, 2, 3, 4)
        sl[2:2+len(sample_tuple)] = sample_tuple
        self.assertEqual(len(sl), initial_size)

    def test_reversed(self):
        sl = sparse_list.SparseList([1, 2, 3])
        self.assertEqual([3, 2, 1], list(reversed(sl)))

    def test_sorted(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEqual([0, 0, 0, 1, 1], list(sorted(sl)))

    def test_get_out_of_bounds(self):
        sl = sparse_list.SparseList(1)
        self.assertEqual(None, sl[1])

    def test_set_out_of_bounds(self):
        sl = sparse_list.SparseList(1)
        sl[100] = 1
        self.assertEqual(101, len(sl))

    def test_present_item_removal(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        del sl[0]
        self.assertEqual([0, 0, 0, 1], sl)
        self.assertEqual(1, sl.population())

    def test_missing_item_removal(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        del sl[1]
        self.assertEqual([1, 0, 0, 1], sl)
        self.assertEqual(2, sl.population())

    def test_slice_removal(self):
        sl = sparse_list.SparseList(range(10))
        del sl[3:5]
        self.assertEqual([0, 1, 2, 5, 6, 7, 8, 9], sl)
        self.assertEqual(8, sl.population())

    def test_slice_removal_with_default_present(self):
        sl = sparse_list.SparseList(range(10), 0)
        del sl[3:5]
        self.assertEqual([0, 1, 2, 5, 6, 7, 8, 9], sl)
        self.assertEqual(7, sl.population())

    def test_unbounded_head_slice_removal(self):
        sl = sparse_list.SparseList(range(10))
        del sl[:3]
        self.assertEqual([3, 4, 5, 6, 7, 8, 9], sl)
        self.assertEqual(7, sl.population())

    def test_unbounded_head_slice_removal_with_default_present(self):
        sl = sparse_list.SparseList(range(10), 0)
        del sl[:3]
        self.assertEqual([3, 4, 5, 6, 7, 8, 9], sl)
        self.assertEqual(7, sl.population())

    def test_unbounded_tail_slice_removal(self):
        sl = sparse_list.SparseList(range(10), None)
        del sl[5:]
        self.assertEqual([0, 1, 2, 3, 4], sl)
        self.assertEqual(5, sl.population())

    def test_stepped_slice_removal(self):
        sl = sparse_list.SparseList(range(6), None)
        del sl[::2]
        self.assertEqual([1, 3, 5], sl)
        self.assertEqual(3, sl.population())

    def test_empty_removal(self):
        sl = sparse_list.SparseList(range(5), None)
        del sl[3:3]
        self.assertEqual([0, 1, 2, 3, 4], sl)
        self.assertEqual(5, sl.population())

    def test_append(self):
        sl = sparse_list.SparseList(1, 0)
        sl.append(1)
        self.assertEqual([0, 1], sl)
        self.assertEqual(1, sl.population())

    def test_clone(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = a[:]
        b.append(4)
        self.assertEqual([1, 2, 3], a)
        self.assertEqual([1, 2, 3, 4], b)
        self.assertEqual(a.population() + 1, b.population())

    def test_concatenation(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([4, 5, 6])
        c = a + b
        self.assertEqual([1, 2, 3], a)
        self.assertEqual([4, 5, 6], b)
        self.assertEqual([1, 2, 3, 4, 5, 6], c)
        self.assertEqual(a.population() + b.population(), c.population())

    def test_in_place_concatenation(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([4, 5, 6])
        a += b
        self.assertEqual([1, 2, 3, 4, 5, 6], a)
        self.assertEqual([4, 5, 6], b)
        self.assertEqual(6, a.population())

    def test_equality(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 2, 3])
        self.assertTrue(a == b)
        self.assertTrue(not a != b)
        self.assertEqual(a, b)
        self.assertTrue(b == a)
        self.assertTrue(not b != a)
        self.assertEqual(b, a)

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

    def test_inequality_length(self):
        a = sparse_list.SparseList(2)
        b = sparse_list.SparseList(4)
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

    def test_less_than_with_a_pair_that_is_greater(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 0, 4])
        self.assertFalse(a < b)
        self.assertFalse(a == b)
        self.assertTrue(b <= a)
        self.assertTrue(b < a)

    def test_less_than_prefix(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 2, 3, 4])
        self.assertTrue(a < b)
        self.assertFalse(a == b)
        self.assertFalse(b <= a)
        self.assertFalse(b < a)

    def test_less_than_different_lengths(self):
        a = sparse_list.SparseList([1, 2, 3, 4])
        b = sparse_list.SparseList([2, 1, 3])
        self.assertTrue(a < b)
        self.assertFalse(a == b)
        self.assertFalse(b <= a)
        self.assertFalse(b < a)


    def test_multiply(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        sl4 = sl * 4
        self.assertEqual([1, 0, 0, 0, 1], sl)
        self.assertEqual(
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], sl4)
        self.assertEqual(len(sl) * 4, len(sl4))
        self.assertEqual(sl.population() * 4, sl4.population())

    def test_multiply_in_place(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        sl *= 4
        self.assertEqual(
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], sl)
        self.assertEqual(8, sl.population())

    def test_count_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEqual(2, sl.count(1))

    def test_count_default_value(self):
        sl = sparse_list.SparseList(100, 1)
        sl[5] = 1
        self.assertEqual(100, sl.count(1))

    def test_extend(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.extend((4, 5, 6))
        self.assertEqual([1, 2, 3, 4, 5, 6], sl)

    def test_index_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEqual(0, sl.index(1))

    def test_index_default_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        self.assertEqual(1, sl.index(0))

    def test_index_absent_default_value(self):
        sl = sparse_list.SparseList([1, 2, 3], 0)
        self.assertRaises(ValueError, sl.index, 0)

    def test_index_absent_value(self):
        sl = sparse_list.SparseList(1, 0)
        self.assertRaises(ValueError, sl.index, 2)

    def test_pop_no_value(self):
        sl = sparse_list.SparseList(4)
        self.assertEqual(None, sl.pop())

    def test_pop_empty(self):
        sl = sparse_list.SparseList(0)
        self.assertRaises(IndexError, sl.pop)

    def test_pop_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        popped = sl.pop()
        self.assertEqual(3, popped)
        self.assertEqual(2, len(sl))
        self.assertEqual([1, 2], sl)
        self.assertEqual(2, sl.population())

    def test_push_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.push(4)
        self.assertEqual(4, len(sl))
        self.assertEqual([1, 2, 3, 4], sl)
        self.assertEqual(4, sl.population())

    def test_remove_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.remove(2)
        self.assertEqual(3, len(sl))
        self.assertEqual([1, None, 3], sl)
        self.assertEqual(2, sl.population())

    def test_remove_only_first_value(self):
        sl = sparse_list.SparseList([2, 2, 3])
        sl.remove(2)
        self.assertEqual(3, len(sl))
        self.assertEqual([None, 2, 3], sl)
        self.assertEqual(2, sl.population())

    def test_remove_non_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        self.assertRaises(ValueError, sl.remove, 4)

    def test_remove_default_value_does_nothing(self):
        sl = sparse_list.SparseList(4, None)
        sl.remove(None)
        self.assertEqual([None, None, None, None], sl)
        self.assertEqual(0, sl.population())

    def test_set_slice_observes_stop(self):
        sl = sparse_list.SparseList(4, None)
        sl[0:2] = [1, 2, 3]
        self.assertEqual([1, 2, None, None], sl)
        self.assertEqual(2, sl.population())

    def test_set_slice_resizes(self):
        sl = sparse_list.SparseList(0, None)
        sl[4:] = [4, 5]
        self.assertEqual([None, None, None, None, 4, 5], sl)
        self.assertEqual(len(sl), 6)
        self.assertEqual(2, sl.population())

    def test_set_slice_extends_past_end(self):
        sl = sparse_list.SparseList(5, None)
        sl[3:] = [6, 7, 8]
        self.assertEqual([None, None, None, 6, 7, 8], sl)
        self.assertEqual(3, sl.population())

    def test_set_slice_with_step(self):
        sl = sparse_list.SparseList(6, None)
        sl[::2] = [1, 2, 3]
        self.assertEqual([1, None, 2, None, 3, None], sl)
        self.assertEqual(3, sl.population())

    def test_setting_an_item_with_default_does_not_increase_population(self):
        sl = sparse_list.SparseList(6, None)
        sl[2] = None
        self.assertEqual(6, len(sl))
        self.assertEqual(0, sl.population())


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python

import sparse_list
import pytest


class TestSparseList:
    def test_init_zero(self):
        sl = sparse_list.SparseList(0)
        assert 0 == len(sl)
        assert 0 == sl.population()

    def test_init_non_zero(self):
        sl = sparse_list.SparseList(10)
        assert 10 == len(sl)
        assert 0 == sl.population()

    def test_init_no_default(self):
        sl = sparse_list.SparseList(1)
        assert None == sl.default
        assert 0 == sl.population()

    def test_init_default(self):
        sl = sparse_list.SparseList(1, 'test')
        assert 'test' == sl.default
        assert 0 == sl.population()

    def test_random_access_write(self):
        sl = sparse_list.SparseList(1)
        sl[0] = 'alice'
        assert {0: 'alice'} == sl.elements
        assert 1 == sl.population()

    def test_random_access_read_present(self):
        sl = sparse_list.SparseList(2)
        sl[0] = 'brent'
        assert 'brent' == sl[0]
        assert 1 == sl.population()

    def test_random_access_read_absent(self):
        sl = sparse_list.SparseList(2, 'absent')
        sl[1] = 'clint'
        assert 'absent' == sl[0]
        assert 1 == sl.population()

    def test_iteration_empty(self):
        sl = sparse_list.SparseList(3)
        assert [None, None, None] == list(sl)

    def test_iteration_populated(self):
        sl = sparse_list.SparseList(5)
        sl[1], sl[3] = 'a', 'b'
        assert [None, 'a', None, 'b', None] == list(sl)

    def test_membership_absent(self):
        sl = sparse_list.SparseList(5)
        sl[2], sl[3], = 1, 2
        assert False == (3 in sl)

    def test_membership_present(self):
        sl = sparse_list.SparseList(5)
        sl[2], sl[3], = 1, 2
        assert True == (2 in sl)

    def test_string_representations(self):
        sl = sparse_list.SparseList(5, 0)
        sl[3], sl[4] = 5, 6
        assert '[0, 0, 0, 5, 6]' == repr(sl)
        assert '[0, 0, 0, 5, 6]' == str(sl)

    def test_initialisation_by_dict(self):
        sl = sparse_list.SparseList({
            4: 6,
            3: 5,
        }, 0)
        assert [0, 0, 0, 5, 6] == sl
        assert 2 == sl.population()

    def test_initialisation_by_dict_does_not_add_defaults(self):
        sl = sparse_list.SparseList({
            3: 0,
            4: 6,
        }, 0)
        assert [0, 0, 0, 0, 6] == sl
        assert 1 == sl.population()

    def test_initialisation_by_dict_with_non_numeric_key(self):
        with pytest.raises(ValueError):
            sparse_list.SparseList({'a': 5})

    def test_initialisation_by_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 4])
        assert [0, 1, 2, 4] == sl
        assert 4 == sl.population()

    def test_initialisation_by_list_does_not_add_defaults(self):
        sl = sparse_list.SparseList([0, 1, 2, 4], 0)
        assert [0, 1, 2, 4] == sl
        assert 3 == sl.population()

    def test_initialisation_by_generator(self):
        gen = (x for x in (1, 2, 3))
        sl = sparse_list.SparseList(gen)
        assert [1, 2, 3] == sl
        assert 3 == sl.population()

    def test_access_with_negative_index(self):
        sl = sparse_list.SparseList([0, 1, 2, 4])
        assert 4 == sl[-1]

    def test_access_with_negative_index_with_no_value(self):
        sl = sparse_list.SparseList(5, 0)
        assert 0 == sl[-1]

    def test_slice(self):
        sl = sparse_list.SparseList([0, 1, 2, 4], 10)
        assert [1, 2] == sl[1:3]

    def test_slice_is_sparse_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 4], 10)
        assert isinstance(sl[1:3], sparse_list.SparseList)

    def test_extended_slice(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6])
        assert [1, 3, 5] == sl[1:6:2]

    def test_extended_slice_is_sparse_list(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6])
        assert isinstance(sl[1:6:2], sparse_list.SparseList)

    def test_extended_slice_with_negative_stop(self):
        sl = sparse_list.SparseList([0, 1, 2, 3, 4, 5, 6])
        assert [1, 3, 5] == sl[1:-1:2]

    def test_slice_reversal_full(self):
        sl = sparse_list.SparseList([1, 2, 3])
        assert [3, 2, 1] == sl[::-1]

    def test_slice_reversal_empty(self):
        sl = sparse_list.SparseList(4)
        assert [None, None, None, None] == sl[::-1]

    def test_default_slice(self):
        sl = sparse_list.SparseList(23)
        sl[0:2] = (1,2)
        assert [None, None] == sl[2:4]

    def test_slice_list_size(self):
        initial_size = 20
        sl = sparse_list.SparseList(initial_size)
        sample_tuple = (1, 2, 3, 4)
        sl[2:2+len(sample_tuple)] = sample_tuple
        assert len(sl) == initial_size

    def test_reversed(self):
        sl = sparse_list.SparseList([1, 2, 3])
        assert [3, 2, 1] == list(reversed(sl))

    def test_sorted(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        assert [0, 0, 0, 1, 1] == list(sorted(sl))

    def test_get_out_of_bounds(self):
        sl = sparse_list.SparseList(1)
        assert None == sl[1]

    def test_set_out_of_bounds(self):
        sl = sparse_list.SparseList(1)
        sl[100] = 1
        assert 101 == len(sl)

    def test_present_item_removal(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        del sl[0]
        assert [0, 0, 0, 1] == sl
        assert 1 == sl.population()

    def test_missing_item_removal(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        del sl[1]
        assert [1, 0, 0, 1] == sl
        assert 2 == sl.population()

    def test_slice_removal(self):
        sl = sparse_list.SparseList(range(10))
        del sl[3:5]
        assert [0, 1, 2, 5, 6, 7, 8, 9] == sl
        assert 8 == sl.population()

    def test_slice_removal_with_default_present(self):
        sl = sparse_list.SparseList(range(10), 0)
        del sl[3:5]
        assert [0, 1, 2, 5, 6, 7, 8, 9] == sl
        assert 7 == sl.population()

    def test_unbounded_head_slice_removal(self):
        sl = sparse_list.SparseList(range(10))
        del sl[:3]
        assert [3, 4, 5, 6, 7, 8, 9] == sl
        assert 7 == sl.population()

    def test_unbounded_head_slice_removal_with_default_present(self):
        sl = sparse_list.SparseList(range(10), 0)
        del sl[:3]
        assert [3, 4, 5, 6, 7, 8, 9] == sl
        assert 7 == sl.population()

    def test_unbounded_tail_slice_removal(self):
        sl = sparse_list.SparseList(range(10), None)
        del sl[5:]
        assert [0, 1, 2, 3, 4] == sl
        assert 5 == sl.population()

    def test_stepped_slice_removal(self):
        sl = sparse_list.SparseList(range(6), None)
        del sl[::2]
        assert [1, 3, 5] == sl
        assert 3 == sl.population()

    def test_empty_removal(self):
        sl = sparse_list.SparseList(range(5), None)
        del sl[3:3]
        assert [0, 1, 2, 3, 4] == sl
        assert 5 == sl.population()

    def test_append(self):
        sl = sparse_list.SparseList(1, 0)
        sl.append(1)
        assert [0, 1] == sl
        assert 1 == sl.population()

    def test_clone(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = a[:]
        b.append(4)
        assert [1, 2, 3] == a
        assert [1, 2, 3, 4] == b
        assert a.population() + 1 == b.population()

    def test_concatenation(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([4, 5, 6])
        c = a + b
        assert [1, 2, 3] == a
        assert [4, 5, 6] == b
        assert [1, 2, 3, 4, 5, 6] == c
        assert a.population() + b.population() == c.population()

    def test_in_place_concatenation(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([4, 5, 6])
        a += b
        assert [1, 2, 3, 4, 5, 6] == a
        assert [4, 5, 6] == b
        assert 6 == a.population()

    def test_equality(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 2, 3])
        assert a == b
        assert not a != b
        assert a == b
        assert b == a
        assert not b != a
        assert b == a

    def test_inequality_same_length(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 0, 3])
        assert a != b
        assert not a == b
        assert a != b
        assert b != a
        assert not b == a
        assert b != a

    def test_inequality_left_longer(self):
        a = sparse_list.SparseList([1, 2, 3, 4])
        b = sparse_list.SparseList([1, 2, 3])
        assert a != b
        assert not (a == b)
        assert a != b
        assert b != a
        assert not (b == a)
        assert b != a

    def test_inequality_length(self):
        a = sparse_list.SparseList(2)
        b = sparse_list.SparseList(4)
        assert a != b
        assert not (a == b)
        assert a != b
        assert b != a
        assert not (b == a)
        assert b != a

    def test_less_than(self):
        a = sparse_list.SparseList([1, 2, 3, 0])
        b = sparse_list.SparseList([1, 2, 4, 5])
        assert a < b
        assert not (a == b)
        assert not (a >= b)
        assert not (a > b)

    def test_greater_than(self):
        a = sparse_list.SparseList([1, 2, 3, 0])
        b = sparse_list.SparseList([1, 2, 4, 5])
        assert b > a
        assert not (b == a)
        assert not (b <= a)
        assert not (b < a)

    def test_less_than_with_a_pair_that_is_greater(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 0, 4])
        assert not (a < b)
        assert not (a == b)
        assert b <= a
        assert b < a

    def test_less_than_prefix(self):
        a = sparse_list.SparseList([1, 2, 3])
        b = sparse_list.SparseList([1, 2, 3, 4])
        assert a < b
        assert not (a == b)
        assert not (b <= a)
        assert not (b < a)

    def test_less_than_different_lengths(self):
        a = sparse_list.SparseList([1, 2, 3, 4])
        b = sparse_list.SparseList([2, 1, 3])
        assert a < b
        assert not (a == b)
        assert not (b <= a)
        assert not (b < a)


    def test_multiply(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        sl4 = sl * 4
        assert [1, 0, 0, 0, 1] == sl
        assert [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1] == sl4
        assert len(sl) * 4 == len(sl4)
        assert sl.population() * 4 == sl4.population()

    def test_multiply_in_place(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        sl *= 4
        assert [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1] == sl
        assert 8 == sl.population()

    def test_count_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        assert 2 == sl.count(1)

    def test_count_default_value(self):
        sl = sparse_list.SparseList(100, 1)
        sl[5] = 1
        assert 100 == sl.count(1)

    def test_extend(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.extend((4, 5, 6))
        assert [1, 2, 3, 4, 5, 6] == sl

    def test_index_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        assert 0 == sl.index(1)

    def test_index_default_value(self):
        sl = sparse_list.SparseList({0: 1, 4: 1}, 0)
        assert 1 == sl.index(0)

    def test_index_absent_default_value(self):
        sl = sparse_list.SparseList([1, 2, 3], 0)
        with pytest.raises(ValueError):
            sl.index(0)

    def test_index_absent_value(self):
        sl = sparse_list.SparseList(1, 0)
        with pytest.raises(ValueError):
            sl.index(2)

    def test_pop_no_value(self):
        sl = sparse_list.SparseList(4)
        assert None == sl.pop()

    def test_pop_empty(self):
        sl = sparse_list.SparseList(0)
        with pytest.raises(IndexError):
            sl.pop()

    def test_pop_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        popped = sl.pop()
        assert 3 == popped
        assert 2 == len(sl)
        assert [1, 2] == sl
        assert 2 == sl.population()

    def test_push_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.push(4)
        assert 4 == len(sl)
        assert [1, 2, 3, 4] == sl
        assert 4 == sl.population()

    def test_remove_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        sl.remove(2)
        assert 3 == len(sl)
        assert [1, None, 3] == sl
        assert 2 == sl.population()

    def test_remove_only_first_value(self):
        sl = sparse_list.SparseList([2, 2, 3])
        sl.remove(2)
        assert 3 == len(sl)
        assert [None, 2, 3] == sl
        assert 2 == sl.population()

    def test_remove_non_value(self):
        sl = sparse_list.SparseList([1, 2, 3])
        with pytest.raises(ValueError):
            sl.remove(4)

    def test_remove_default_value_does_nothing(self):
        sl = sparse_list.SparseList(4, None)
        sl.remove(None)
        assert [None, None, None, None] == sl
        assert 0 == sl.population()

    def test_set_slice_observes_stop(self):
        sl = sparse_list.SparseList(4, None)
        sl[0:2] = [1, 2, 3]
        assert [1, 2, None, None] == sl
        assert 2 == sl.population()

    def test_set_slice_resizes(self):
        sl = sparse_list.SparseList(0, None)
        sl[4:] = [4, 5]
        assert [None, None, None, None, 4, 5] == sl
        assert len(sl) == 6
        assert 2 == sl.population()

    def test_set_slice_extends_past_end(self):
        sl = sparse_list.SparseList(5, None)
        sl[3:] = [6, 7, 8]
        assert [None, None, None, 6, 7, 8] == sl
        assert 3 == sl.population()

    def test_set_slice_with_step(self):
        sl = sparse_list.SparseList(6, None)
        sl[::2] = [1, 2, 3]
        assert [1, None, 2, None, 3, None] == sl
        assert 3 == sl.population()

    def test_setting_an_item_with_default_does_not_increase_population(self):
        sl = sparse_list.SparseList(6, None)
        sl[2] = None
        assert 6 == len(sl)
        assert 0 == sl.population()

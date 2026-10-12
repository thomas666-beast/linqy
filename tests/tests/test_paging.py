import itertools

import pytest

from pylinq import Enumerable


def test_take():
    assert Enumerable([1, 2, 3, 4, 5]).take(3).to_list() == [1, 2, 3]


def test_take_more_than_available():
    assert Enumerable([1, 2]).take(10).to_list() == [1, 2]


def test_take_zero_and_negative():
    assert Enumerable([1, 2, 3]).take(0).to_list() == []
    assert Enumerable([1, 2, 3]).take(-5).to_list() == []


def test_take_works_on_infinite_sequence():
    result = Enumerable(itertools.count(1)).take(3).to_list()
    assert result == [1, 2, 3]


def test_skip():
    assert Enumerable([1, 2, 3, 4, 5]).skip(2).to_list() == [3, 4, 5]


def test_skip_more_than_available():
    assert Enumerable([1, 2]).skip(10).to_list() == []


def test_skip_zero_and_negative():
    assert Enumerable([1, 2, 3]).skip(0).to_list() == [1, 2, 3]
    assert Enumerable([1, 2, 3]).skip(-5).to_list() == [1, 2, 3]


def test_skip_take_paging():
    page = Enumerable(range(1, 21)).skip(10).take(5).to_list()
    assert page == [11, 12, 13, 14, 15]


def test_take_while():
    result = Enumerable([1, 2, 3, 10, 1, 2]).take_while(lambda x: x < 5).to_list()
    assert result == [1, 2, 3]


def test_take_while_none_match():
    assert Enumerable([5, 1]).take_while(lambda x: x < 5).to_list() == []


def test_skip_while():
    result = Enumerable([1, 2, 3, 10, 1, 2]).skip_while(lambda x: x < 5).to_list()
    assert result == [10, 1, 2]


def test_skip_while_all_match():
    assert Enumerable([1, 2, 3]).skip_while(lambda x: x < 5).to_list() == []


def test_chunk():
    result = Enumerable([1, 2, 3, 4, 5]).chunk(2).to_list()
    assert result == [[1, 2], [3, 4], [5]]


def test_chunk_exact_multiple():
    assert Enumerable([1, 2, 3, 4]).chunk(2).to_list() == [[1, 2], [3, 4]]


def test_chunk_empty():
    assert Enumerable([]).chunk(3).to_list() == []


def test_chunk_invalid_size():
    with pytest.raises(ValueError):
        Enumerable([1, 2, 3]).chunk(0)


def test_take_is_lazy():
    pulled = []

    def source():
        for i in range(100):
            pulled.append(i)
            yield i

    Enumerable(source()).take(3).to_list()
    assert pulled == [0, 1, 2]

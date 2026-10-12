from pylinq import Enumerable


# distinct
def test_distinct():
    assert Enumerable([1, 2, 2, 3, 1]).distinct().to_list() == [1, 2, 3]


def test_distinct_preserves_first_occurrence_order():
    assert Enumerable([3, 1, 3, 2, 1]).distinct().to_list() == [3, 1, 2]


def test_distinct_empty():
    assert Enumerable([]).distinct().to_list() == []


def test_distinct_with_key_selector():
    words = ["apple", "avocado", "banana", "blueberry", "cherry"]
    result = Enumerable(words).distinct(lambda w: w[0]).to_list()
    assert result == ["apple", "banana", "cherry"]


# union
def test_union():
    assert Enumerable([1, 2, 3]).union([3, 4, 5]).to_list() == [1, 2, 3, 4, 5]


def test_union_removes_duplicates_within_each_side():
    assert Enumerable([1, 1, 2]).union([2, 3, 3]).to_list() == [1, 2, 3]


def test_union_order():
    assert Enumerable([5, 1]).union([3, 1]).to_list() == [5, 1, 3]


# intersect
def test_intersect():
    assert Enumerable([1, 2, 3, 4]).intersect([3, 4, 5]).to_list() == [3, 4]


def test_intersect_removes_duplicates():
    assert Enumerable([1, 1, 2, 2]).intersect([1, 2]).to_list() == [1, 2]


def test_intersect_follows_first_sequence_order():
    assert Enumerable([3, 1, 2]).intersect([1, 2, 3]).to_list() == [3, 1, 2]


def test_intersect_no_overlap():
    assert Enumerable([1, 2]).intersect([3, 4]).to_list() == []


# except_
def test_except():
    assert Enumerable([1, 2, 3, 4]).except_([2, 4]).to_list() == [1, 3]


def test_except_removes_duplicates():
    assert Enumerable([1, 1, 2, 3, 3]).except_([2]).to_list() == [1, 3]


def test_except_empty_second():
    assert Enumerable([1, 2, 2]).except_([]).to_list() == [1, 2]


# general
def test_second_can_be_generator_or_enumerable():
    assert Enumerable([1, 2, 3]).intersect(x for x in [2, 3, 9]).to_list() == [2, 3]
    assert Enumerable([1, 2]).union(Enumerable([2, 3])).to_list() == [1, 2, 3]


def test_deferred_execution():
    calls = []

    def track(x):
        calls.append(x)
        return x

    query = Enumerable([1, 1, 2]).distinct(track)
    assert calls == []
    assert query.to_list() == [1, 2]
    assert calls == [1, 1, 2]

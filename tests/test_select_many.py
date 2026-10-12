from pylinq import Enumerable


def test_flattens_lists():
    result = Enumerable([[1, 2], [3], [4, 5]]).select_many(lambda x: x).to_list()
    assert result == [1, 2, 3, 4, 5]


def test_selector_extracts_inner_collection():
    people = [
        {"name": "Ann", "pets": ["cat", "dog"]},
        {"name": "Bob", "pets": []},
        {"name": "Cy", "pets": ["fish"]},
    ]
    result = Enumerable(people).select_many(lambda p: p["pets"]).to_list()
    assert result == ["cat", "dog", "fish"]


def test_result_selector():
    people = [
        {"name": "Ann", "pets": ["cat", "dog"]},
        {"name": "Cy", "pets": ["fish"]},
    ]
    result = (
        Enumerable(people)
        .select_many(lambda p: p["pets"], lambda p, pet: f"{p['name']}:{pet}")
        .to_list()
    )
    assert result == ["Ann:cat", "Ann:dog", "Cy:fish"]


def test_empty_inner_sequences():
    assert Enumerable([[], []]).select_many(lambda x: x).to_list() == []


def test_chains_with_where():
    result = (
        Enumerable([[1, 2, 3], [4, 5, 6]])
        .select_many(lambda x: x)
        .where(lambda n: n % 2 == 0)
        .to_list()
    )
    assert result == [2, 4, 6]


def test_deferred_execution():
    calls = []

    def selector(x):
        calls.append(x)
        return [x, x]

    query = Enumerable([1, 2]).select_many(selector)
    assert calls == []
    assert query.to_list() == [1, 1, 2, 2]
    assert calls == [1, 2]

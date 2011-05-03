
from guess_json_schema import guess_schema
import validictory

def make_test(d):
    s = guess_schema(d)
    return validictory.validate(d, s)

def test():
    import sys
    print "import validictory"
    make_test("a")
    make_test(123)
    make_test([])
    make_test({})

    make_test([1, 3, 4])
    make_test(['1, 3, 4'])
    make_test([[1,2],[2,3],[4,5],[6,7]])

    make_test([[1,2],[2,{}]])

    make_test([[1,2],[2,{}],[4,5],[6,7]])


    make_test({'a': 1, 'b': 2})
    make_test([{'a': 1, 'b': 2}, {'a': 234, 'c': 10}])

    make_test([{'a': 'here'}, {'a': ''}])
    sys.exit(0)

    S = [[{"a": "b"},{"a": "c"}], 1, "23452345"]
    make_test(S)
    S = [{"a": "b"},{"a": "c"},{"a": "c", "d": None}]
    make_test(S)
    S = [{"a": "c", "d": None},{"a": "b"},{"a": "c"},]
    make_test(S)
    S = [None,]
    make_test(S)
    S = {}
    make_test(S)

    print '#' * 10
    S = [{"a": 1},{"a": "b"},{"a": None},]
    make_test(S)

    S = [{"a": {}}, {"a": {"aa": 1, "bb": 2}},{"a": None},]
    make_test(S)


    S = {'places': [
            {'p': 1, 'h': [{'p': 1, 's': 1}, {'p': 1, 's': 1}]},
            {'p': 2, 'h': [{'p': 2, 's': 1}, {'p': 2, 's': 1}]},
            {'p': 3, 'h': [{'p': 2, 's': 1}, {'p': 3, 's': 1}]},
            ]}

    make_test(S)


if __name__ == '__main__':
    test()

#!/usr/bin/python

""" This code is more proof of concept.

Try to automatically deduce Json schema given sample.

For the moment:

* multiple samples can be given as array, but then array can be stripped from schema
to get the combined schema of the samples.

* "json schema" is python sctructure, which can be converted to json by e.g. simplejson

* validictory's "blank" not honoured (empty string will not validate with that)

The algorithm is two-phase one.

At the first phase a set of "access paths" is being created,
each "access" counted.

At the second phase paths are reconstructed to json schema.

"""

import urllib
import simplejson


TYPES = {
    type(1): 'integer',
    type(1.2): 'number',
    type("abc"): 'string',
    type(u"abc"): 'string',
    type(True): 'boolean',
    type([]): 'array',
    type(()): 'array',
    type({}): 'object',
    type(None): 'null',
    }

COMPOUND_TYPES = set(['array', 'object'])
SCALARS_TYPES = set(TYPES.values()) - COMPOUND_TYPES

def parse_sample(item, paths=None, base=None):
    base = base or ()
    paths = paths or {}  # path container and counters
    paths.setdefault(base, 0)
    paths[base] += 1
    type_ = TYPES.get(type(item), "any")
    base1 = base + (type_,)
    paths.setdefault(base1, 0)
    if type_ in SCALARS_TYPES:
        paths[base1] += 1
    elif type_ == "array":
        paths[base1] += 1
        base1b = base1 + (None,)   # adding extra place for possible extensions (eg array index)
        paths.setdefault(base1b, 0)
        for subitem in item:
            parse_sample(subitem, paths=paths, base=base1b)
    elif type_ == "object":
        paths[base1] += 1
        for (k, subitem) in item.items():
            base1b = base1 + (k,)
            parse_sample(subitem, paths=paths, base=base1b)

    return paths


def find_type(schema, typename):
    for t in schema["type"]:
        if isinstance(t, dict) and t.get("type") == typename:
            return t
    return None


def build_element(paths, schema, path, pos=0):
    if pos >= len(path):
        return
    typename = path[pos]
    if typename in SCALARS_TYPES:
        if "type" in schema:
            if schema["type"] != typename:
                if isinstance(schema["type"], list):
                    if typename in schema["type"]:
                        return
                    schema["type"].append(typename)
                else:
                    schema["type"] = [schema["type"], typename]
        else:
            schema["type"] = typename
        # scalar type is always a leaf. No need to call.
        #build_element(paths, schema, path, pos+1)
    elif typename == "object":
        if "type" in schema:
            if schema["type"] != typename:
                if isinstance(schema["type"], list):
                    typedef = find_type(schema, "object")
                    if typedef is None:
                        typedef = {"type": "object", "properties": {}}
                        schema["type"].append(typedef)
                else:
                    typedef = {"type": "object", "properties": {}}
                    schema["type"] = [schema["type"], typedef]
                props = typedef["properties"]
            else:
                props = schema["properties"]
        else:
            schema["type"] = typename
            props = schema["properties"] = {}
        # deal with properties
        if pos+1 < len(path):
            propname = path[pos+1]
            if propname in props:
                subschema = props[propname]
            else:
                subschema = props[propname] = {
                    "required": paths[path[:pos+1]] == paths[path[:pos+2]],  # property less frequent than base object
                    }
            build_element(paths, subschema, path, pos+2)
    elif typename == "array":
        if "type" in schema:
            if schema["type"] != typename:
                if isinstance(schema["type"], list):
                    typedef = find_type(schema, "array")
                    if typedef is None:
                        typedef = {"type": "array", "items": {}}
                        schema["type"].append(typedef)
                else:
                    typedef = {"type": "array", "items": {}}
                    schema["type"] = [schema["type"], typedef]
                items = typedef["items"]
            else:
                items = schema["items"]
        else:
            schema["type"] = typename
            items = schema["items"] = {}   #schema
        # deal with items
        if pos+1 < len(path):
            assert path[pos+1] is None  # for now
            subschema = items
            build_element(paths, subschema, path, pos+2)



def build_schema(paths):
    schema = {}
    for path in sorted(paths.keys()):
        build_element(paths, schema, path)

    return schema



def SCH(s):
    print "d=",repr(s)
    print "s=",
    paths = parse_sample(s)
    pp(build_schema(paths))
    print "validictory.validate(d,s)"



def from_json(url):
    u = urllib.urlopen(url).read()
    return simplejson.loads(u)


from pprint import pprint as pp
def test():
    import sys
    print "import validictory"
    SCH("a")
    SCH(123)
    SCH([])
    SCH({})

    SCH([1, 3, 4])
    SCH(['1, 3, 4'])
    SCH([[1,2],[2,3],[4,5],[6,7]])

    SCH([[1,2],[2,{}]])

    SCH([[1,2],[2,{}],[4,5],[6,7]])


    SCH({'a': 1, 'b': 2})
    SCH([{'a': 1, 'b': 2}, {'a': 234, 'c': 10}])

    SCH([{'a': 'here'}, {'a': ''}])
    sys.exit(0)

    S = [[{"a": "b"},{"a": "c"}], 1, "23452345"]
    SCH(S)
    S = [{"a": "b"},{"a": "c"},{"a": "c", "d": None}]
    SCH(S)
    S = [{"a": "c", "d": None},{"a": "b"},{"a": "c"},]
    SCH(S)
    S = [None,]
    SCH(S)
    S = {}
    SCH(S)

    print '#' * 10
    S = [{"a": 1},{"a": "b"},{"a": None},]
    SCH(S)

    S = [{"a": {}}, {"a": {"aa": 1, "bb": 2}},{"a": None},]
    SCH(S)


    S = {'places': [
            {'p': 1, 'h': [{'p': 1, 's': 1}, {'p': 1, 's': 1}]},
            {'p': 2, 'h': [{'p': 2, 's': 1}, {'p': 2, 's': 1}]},
            {'p': 3, 'h': [{'p': 2, 's': 1}, {'p': 3, 's': 1}]},
            ]}

    SCH(S)


if __name__ == '__main__':
    test()

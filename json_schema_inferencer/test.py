
from guess_json_schema import guess_schema
from validictory.validator import SchemaError
from validictory.validator import SchemaValidator
import copy
import validictory
import warnings

# the only reason for this class is to workaround problem
# in the validictory, which requires string to be non-blank
class FixedSchemaValidator(SchemaValidator):
    def _SchemaValidator__validate(self, fieldname, data, schema):

        if schema is not None:
            if not isinstance(schema, dict):
                raise SchemaError("Schema structure is invalid.")

            newschema = copy.copy(schema)

            # handle 'optional', replace it with 'required'
            if 'required' in schema and 'optional' in schema:
                raise SchemaError('cannot specify optional and required')
            elif 'optional' in schema:
                warnings.warn('The "optional" attribute has been replaced by "required"', DeprecationWarning)
                newschema['required'] = not schema['optional']
            elif 'required' not in schema:
                newschema['required'] = self.required_by_default

            if 'blank' not in schema:
                newschema['blank'] = True

            for schemaprop in newschema:

                validatorname = "validate_" + schemaprop

                validator = getattr(self, validatorname, None)
                if validator:
                    validator(data, fieldname, schema,
                              newschema.get(schemaprop))

        return data

def make_test(d):
    s = guess_schema(d)
    return validictory.validate(d, s, validator_cls=FixedSchemaValidator)

def test():
    import sys
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

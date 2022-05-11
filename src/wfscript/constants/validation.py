from . import ConstantNamespace


class DataType(ConstantNamespace):
    STRING = 'string'
    INTEGER = 'integer'
    NUMBER = 'number'
    FLOAT = 'float'
    BOOLEAN = 'boolean'
    OBJECT = 'object'
    ARRAY = 'array'
    RECORD = 'record'
    TAG = 'tag'
    # NODE = 'node'


class ValidatorKeyword(ConstantNamespace):
    REQUIRED = 'required'
    DATA_TYPE = 'data_type'
    MEMBER_SPEC = 'member_spec'
    MIN_SIZE = 'min_size'
    MAX_SIZE = 'max_size'
    MEMBER_DATA_TYPE = 'member_data_type'
    MEMBER_SPEC = 'member_spec'
from . import ConstantNamespace


class TagName(ConstantNamespace):
    META = '!META'
    State = '!State'
    Data = '!Data'
    Action = '!Action'
    Method = '!Method'


class MetaSectionKey(ConstantNamespace):
    NAMESPACE = 'namespace'
    NAME = 'name'
    VERSION = 'version'
    STATUS = 'status'


class MetaStatusChoice(ConstantNamespace):
    PRODUCTION = 'production'
    TESTING = 'testing'
    DEVELOPMENT = 'development'


class MethodKeyword(ConstantNamespace):
    RETURN = 'return'
    IDENTITY = 'id'
    BODY = 'body'
    INPUT = 'input'
    OUTPUT_TARGET = 'output>>'

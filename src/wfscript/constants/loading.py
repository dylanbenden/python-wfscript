from . import ConstantNamespace


class TagName(ConstantNamespace):
    META = '!META'
    INPUT = '!INPUT'
    BODY = '!BODY'
    RETURN = '!RETURN'
    ALIASES = '!ALIASES'
    Material = '!Material'
    Materials = '!Materials'
    Asset = '!Asset'
    Assets = '!Assets'
    State = '!State'
    Input = '!Input'
    Output = '!Output'
    Action = '!Action'
    Validator = '!Validator'
    Method = '!Method'
    Step = '!Step'


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

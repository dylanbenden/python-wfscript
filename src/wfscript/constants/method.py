from . import ConstantNamespace


class TagName(ConstantNamespace):
    IDENTITY = '!IDENTITY'
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

    NAMESPACE = '!NAMESPACE'
    NAME = '!NAME'
    VERSION = '!VERSION'
    STATUS = '!STATUS'


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

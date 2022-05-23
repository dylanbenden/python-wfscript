from . import ConstantNamespace


class TagName(ConstantNamespace):
    IDENTITY = '!IDENTITY'
    INPUT = '!INPUT'
    BODY = '!BODY'
    OUTPUT = '!OUTPUT'

    NAMESPACE = '!NAMESPACE'
    NAME = '!NAME'
    VERSION = '!VERSION'
    STATUS = '!STATUS'

    Action = '!Action'
    Method = '!Method'
    Step = '!Step'
    Ticket = '!Ticket'

    State = '!State'
    Input = '!Input'
    Output = '!Output'

    Material = '!Material'
    Materials = '!Materials'
    Asset = '!Asset'
    Assets = '!Assets'

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

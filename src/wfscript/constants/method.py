from . import ConstantNamespace


class TagName(ConstantNamespace):
    # Method interface
    IDENTITY = '!IDENTITY'
    INPUT = '!INPUT'
    OUTPUT = '!OUTPUT'

    # Labels
    namespace = '!namespace'
    name = '!name'
    version = '!version'
    status = '!status'

    # Containers
    BODY = '!BODY'
    CHOICES = '!CHOICES'
    STEPS = '!STEPS'
    REPEAT = '!REPEAT'

    # Containables
    Action = '!Action'
    Method = '!Method'
    Step = '!Step'
    Ticket = '!Ticket'
    Choice = '!Choice'
    Verify = '!Verify'

    # Runtime data sources
    State = '!State'
    Input = '!Input'
    Output = '!Output'
    Material = '!Material'
    Materials = '!Materials'
    Asset = '!Asset'
    Assets = '!Assets'
    Item = '!Item'
    Collection = '!Collection'

    # Selection
    SelectionSource = '!SelectionSource'
    SelectionValue = '!SelectionValue'


class MetaStatusChoice(ConstantNamespace):
    PRODUCTION = 'production'
    TESTING = 'testing'
    DEVELOPMENT = 'development'
    DEPRECATED = 'deprecated'


class MethodKeyword(ConstantNamespace):
    # RETURN = 'return'
    # IDENTITY = 'id'
    # BODY = 'body'
    # INPUT = 'input'
    OUTPUT_TARGET = 'output>>'

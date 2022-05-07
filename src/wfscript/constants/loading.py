from . import ConstantNamespace


class TagName(ConstantNamespace):
    META = '!META'


class MetaSectionKey(ConstantNamespace):
    NAMESPACE = 'namespace'
    NAME = 'name'
    VERSION = 'version'
    STATUS = 'status'

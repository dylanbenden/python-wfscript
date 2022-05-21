from . import ConstantNamespace


class IdentityDelimeter(ConstantNamespace):
    DOMAIN = '++'
    NAMESPACE = '::'
    VERSION = '=='
    MATERIAL = '::'


class DocumentStatus(ConstantNamespace):
    PRODUCTION = 'production'
    TESTING = 'testing'
    DEVELOPMENT = 'development'
    DEPRECATED = 'deprecated'

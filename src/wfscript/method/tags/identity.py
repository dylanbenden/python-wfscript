from .base import YAMLConfigured
from ...constants.identity import IdentityDelimeter
from ...constants.method import TagName
from ...utils.identity import deconstruct_identity


class IdentitySectionTag(YAMLConfigured):
    tag_name = TagName.IDENTITY

    @classmethod
    def construct_value(cls, loader, node):
        value = super(IdentitySectionTag, cls).construct_value(loader, node)
        if isinstance(value, list):
            return {
                node.tag: node.value
                for node in value
            }
        elif isinstance(value, str) and IdentityDelimeter.NAMESPACE in value:
            return deconstruct_identity(value)
        else:
            raise RuntimeError(f'{cls.tag_name} is not expecting the configuration value {value}')

    def render(self, *_):
        return self.value

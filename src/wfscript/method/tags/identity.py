from .base import YAMLConfigured
from ...constants.identity import IdentityDelimeter
from ...constants.method import TagName
from ...utils.identity import deconstruct_identity


class IdentitySectionTag(YAMLConfigured):
    tag_name = TagName.IDENTITY
    construct_value_as_mapping = True

    @classmethod
    def construct_value(cls, loader, node):
        value = super(IdentitySectionTag, cls).construct_value(loader, node)
        if isinstance(value, str) and IdentityDelimeter.NAMESPACE in value:
            return deconstruct_identity(value)
        return value

    def render(self, *_):
        return self.value

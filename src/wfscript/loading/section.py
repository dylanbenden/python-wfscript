from .base import YAMLConfiguredObject
from ..constants.loading import TagName


class MetaTag(YAMLConfiguredObject):
    tag_name = TagName.META

    @classmethod
    def construct_value(cls, loader, node):
        value = super(MetaTag, cls).construct_value(loader, node)
        # meta section values are *always* strings, even if they *could* be represented as a float or int
        return {k: str(v) for k, v in value.items()}

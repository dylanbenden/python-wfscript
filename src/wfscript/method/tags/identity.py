from .base import YAMLConfigured
from ...constants.method import TagName
from ...utils.identity import deconstruct_identity


class IDTag(YAMLConfigured):
    tag_name = TagName.ID

    @classmethod
    def construct_value(cls, loader, node):
        value = super(IDTag, cls).construct_value(loader, node)
        if isinstance(value, list):
            return {
                node.tag: node.value
                for node in value
            }
        elif isinstance(value, dict):
            return dict
        else:
            return deconstruct_identity(value)
        # meta section values are *always* strings, even if they *could* be represented as a float or int
        return {k: str(v) for k, v in value.items()}

    def render(self, *_):
        return {
            node.tag: node.value
            for node in self.value
        }
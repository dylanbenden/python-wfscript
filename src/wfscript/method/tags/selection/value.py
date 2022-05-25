from ..base import YAMLConfigured
from ....constants.method import TagName


class SelectionValueTag(YAMLConfigured):
    tag_name = TagName.SelectionValue

    @classmethod
    def construct_value(cls, loader, node):
        # for now, assuming that there is only one input provided
        value = super(SelectionValueTag, cls).construct_value(loader, node)
        return value[0]
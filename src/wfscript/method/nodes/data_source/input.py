from .base import DataSourceNode
from ....constants.method import TagName


class InputNode(DataSourceNode):
    tag_name = TagName.Input

    def data_source(self, context):
        return context.input

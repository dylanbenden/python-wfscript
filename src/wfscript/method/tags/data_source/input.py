from .base import DataSourceTag
from ....constants.method import TagName


class InputTag(DataSourceTag):
    tag_name = TagName.Input

    def data_source(self, context):
        return context.input
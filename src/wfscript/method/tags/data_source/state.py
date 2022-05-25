from .base import DataSourceTag
from ....constants.method import TagName


class StateTag(DataSourceTag):
    tag_name = TagName.State

    def data_source(self, context):
        return context.state
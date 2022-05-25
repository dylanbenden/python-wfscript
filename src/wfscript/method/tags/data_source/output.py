from .base import DataSourceTag
from ....constants.method import TagName


class OutputTag(DataSourceTag):
    tag_name = TagName.Output

    def data_source(self, context):
        return context.output


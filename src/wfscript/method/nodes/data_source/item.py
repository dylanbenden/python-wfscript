from .base import DataSourceNode
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class ItemNode(DataSourceNode):
    tag_name = TagName.Item

    def data_source(self, context):
        return context.item

    def execute_render_from_scalar(self, context):
        if self.value != '':
            return self.traverse_name_key(self.value, item=context.item.value)
        return execute_render(context.item.value, context)

    def output_render_from_scalar(self, context):
        raise RuntimeError(f'{self.tag_name} does not support scalar-configured rendering during OutputPhase; '
                           f'Value: {self.value}')

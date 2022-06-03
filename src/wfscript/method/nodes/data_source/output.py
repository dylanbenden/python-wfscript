from .base import DataSourceNode
from ....constants.method import TagName


class OutputNode(DataSourceNode):
    tag_name = TagName.Output

    def data_source(self, context):
        return context.output

    def execute_render_from_scalar(self, context):
        if self.value == '':
            return context.output.value
        return super(OutputNode, self).output_render_from_scalar(context)

    def output_render_from_scalar(self, context):
        raise RuntimeError(f'{self.tag_name} does not support scalar-configured rendering during OutputPhase; '
                           f'Value: {self.value}')

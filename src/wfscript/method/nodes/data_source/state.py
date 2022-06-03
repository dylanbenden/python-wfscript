from .base import DataSourceNode
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class StateNode(DataSourceNode):
    tag_name = TagName.State

    def data_source(self, context):
        return context.state

    def execute_render_from_dict(self, context):
        context.state.update(execute_render(self.value, context))
        return '!State updated'


from ..base import WorkflowNode, ExecutionPhase
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class SelectionValueTag(WorkflowNode, ExecutionPhase):
    tag_name = TagName.SelectionValue

    @classmethod
    def construct_value(cls, loader, node):
        # for now, assuming that there is only one input provided
        value = super(SelectionValueTag, cls).construct_value(loader, node)
        return value[0]

    def execute_render_from_list(self, context):
        return execute_render(self.value, context)

from ..base import WorkflowNode, ExecutionPhase
from ....constants.method import TagName


class SelectionSourceTag(WorkflowNode, ExecutionPhase):
    tag_name = TagName.SelectionSource

    def execute_render_from_list(self, context):
        return self.value[0].execute_render(context)

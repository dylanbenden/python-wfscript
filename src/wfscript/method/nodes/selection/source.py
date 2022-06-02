from ..base import WorkflowNode
from ....constants.method import TagName


class SelectionSourceTag(WorkflowNode):
    tag_name = TagName.SelectionSource

    def execute_render_from_list(self, context):
        return self.value[0].execute_render(context)

from ..base import WorkflowNode, DualPhase
from ....constants.method import TagName
from ....runtime.utils.render import output_render, execute_render


class OutputBindingNode(WorkflowNode, DualPhase):
    tag_name = TagName.OUTPUT

    def output_render_from_dict(self, context):
        return output_render(self.value, context)

    def output_render_from_list(self, context):
        return output_render(self.value, context)

    def execute_render_from_list(self, context):
        return execute_render(self.value, context)


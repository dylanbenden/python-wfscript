from ..base import WorkflowNode, ExecutionPhase
from ....constants.method import TagName
from ....runtime.utils.identity import deconstruct_identity, construct_identity
from ....runtime.utils.render import execute_render


class IdentityBindingNode(WorkflowNode, ExecutionPhase):
    tag_name = TagName.IDENTITY

    @property
    def constructed(self):
        if isinstance(self.value, str):
            return self.value
        else:
            return construct_identity(self.node_for_tag)

    @property
    def deconstructed(self):
        if isinstance(self.value, str):
            return deconstruct_identity(self.value)
        return self.node_for_tag

    def execute_render_from_scalar(self, context):
        return self.value

    def execute_render_from_list(self, context):
        return execute_render(self.node_for_tag, context)

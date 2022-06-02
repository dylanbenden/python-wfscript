from ..base import WorkflowNode, ExecutionPhase
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class CollectionNode(WorkflowNode, ExecutionPhase):
    tag_name = TagName.Collection

    @property
    def source_node(self):
        return self.value[0]

    def execute_render_from_list(self, context):
        return execute_render(self.source_node, context)

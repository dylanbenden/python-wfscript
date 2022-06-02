from ..base import WorkflowNode, ExecutionPhase
from ....constants.method import TagName
from ....constants.payload import PayloadKey
from ....runtime.utils.render import execute_render
from ....runtime.utils.validation import validate_input


class InputBindingNode(WorkflowNode, ExecutionPhase):
    tag_name = TagName.INPUT

    def validate_input(self, context):
        validate_input(
            spec_part=self.value,
            data_part=context.request[PayloadKey.INPUT].value,
            namespace_root=context.namespace_root
        )
        return 'OK'

    def execute_render_from_dict(self, context, is_validation_spec=False):
        return execute_render(self.value, context)

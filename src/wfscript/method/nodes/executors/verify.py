from .base import ExecutorNode
from ....constants.method import TagName
from ....runtime.utils.validation import validate_input


class VerifyNode(ExecutorNode):
    tag_name = TagName.Verify

    def execute_render_from_list(self, context):
        if TagName.State in self.node_for_tag:
            validate_input(
                spec_part=self.node_for_tag[TagName.State].value,
                data_part=context.state.value,
                namespace_root=context.namespace_root
            )
        if TagName.Output in self.node_for_tag:
            validate_input(
                spec_part=self.node_for_tag[TagName.Output].value,
                data_part=context.output.value,
                namespace_root=context.namespace_root
            )
        return 'OK'

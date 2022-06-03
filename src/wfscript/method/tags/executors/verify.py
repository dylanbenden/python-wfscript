from .base import ExecutorTag
from ....constants.method import TagName
from ....runtime.utils.validation import validate_input


class VerifyTag(ExecutorTag):
    tag_name = TagName.Verify

    def execute(self, context):
        if TagName.State in self.value:
            validate_input(
                spec_part=self.value[TagName.State],
                data_part=context.state.value,
                namespace_root=context.namespace_root
            )
        if TagName.Output in self.value:
            validate_input(
                spec_part=self.value[TagName.Output],
                data_part=context.output.value,
                namespace_root=context.namespace_root
            )
        return 'OK'

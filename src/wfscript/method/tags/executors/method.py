from .base import ExecutorTag
from ....constants.method import TagName, MethodKeyword
from ....runtime.context import get_inner_context


class MethodTag(ExecutorTag):
    tag_name = TagName.Method
    construct_value_as_mapping = True


    def execute(self, context):
        executor = context.namespace_root.get_method(self.identity)
        new_context = get_inner_context(self.identity, context, input_data=self.value.get(TagName.INPUT, dict()))
        output_target = self.value.get(MethodKeyword.OUTPUT_TARGET)
        return executor.run_from_tag(new_context, output_target)


    def render_kwargs(self, context):
        import ipdb; ipdb.set_trace()
        pass
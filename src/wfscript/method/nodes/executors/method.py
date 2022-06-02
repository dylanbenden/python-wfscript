from .base import ExecutorNode
from ....constants.method import TagName
from ....runtime.context import get_inner_context
from ....runtime.output import MethodReturn
from ....runtime.utils.render import execute_render


class MethodNode(ExecutorNode):
    tag_name = TagName.Method
    use_child_tags_as_labels = True

    def execute_render_from_list(self, context):
        executor = context.namespace_root.get_method(self.identity)
        new_context = get_inner_context(
            new_identity=self.identity,
            old_context=context,
            input_data=execute_render(
                data=self.node_for_tag.get(TagName.INPUT, dict()),
                context=context
            )
        )
        context.set_output(executor.execute(context=new_context).result)
        execute_render(self.output, context)
        return MethodReturn(context.output.value)

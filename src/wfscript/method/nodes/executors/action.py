from .base import ExecutorNode
from ....constants.method import TagName
from ....runtime.output import ActionReturn
from ....runtime.utils.render import execute_render


class ActionNode(ExecutorNode):
    tag_name = TagName.Action

    def execute_render_from_list(self, context):
        executor = context.namespace_root.get_action(self.identity)
        rendered_input = execute_render(self.input, context)
        context.set_output(executor(**rendered_input))
        execute_render(self.output, context)
        return ActionReturn(context.output.value)

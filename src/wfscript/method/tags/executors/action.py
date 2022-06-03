from .base import ExecutorTag
from ....constants.method import TagName
from ....runtime.output import ActionReturn


class ActionTag(ExecutorTag):
    tag_name = TagName.Action

    def render_kwargs(self, context):
        return self.input

    def execute(self, context):
        executor = context.namespace_root.get_action(self.identity)
        return ActionReturn(executor(**self.input))

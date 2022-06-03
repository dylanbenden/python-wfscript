from .base import ExecutorTag
from ....constants.method import TagName
from ....runtime.output import StepReturn


class StepTag(ExecutorTag):
    tag_name = TagName.Step
    label_child_tags = True
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]

    @property
    def name(self):
        return self.value[TagName.name].value

    @property
    def input(self):
        return self.value[TagName.INPUT]

    @property
    def body(self):
        return self.value[TagName.BODY]

    @property
    def output(self):
        return self.value.get(TagName.OUTPUT)

    def execute(self, context):
        context.append_debug(self.body.render(context))
        if self.output:
            result = self.output.render(context)
            return StepReturn(result)
        return StepReturn({})


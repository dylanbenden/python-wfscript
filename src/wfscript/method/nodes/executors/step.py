from .base import ExecutorNode
from ....constants.method import TagName
from ....runtime.output import StepReturn
from ....runtime.utils.render import execute_render, output_render


class StepNode(ExecutorNode):
    tag_name = TagName.Step

    @property
    def name(self):
        return self.node_for_tag[TagName.name].value

    @property
    def body(self):
        return self.node_for_tag[TagName.BODY]

    @property
    def output(self):
        return self.node_for_tag[TagName.OUTPUT]

    def execute_render_from_list(self, context):
        context.append_debug(execute_render(self.body, context))
        return StepReturn(output_render(self.output, context))


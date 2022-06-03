from .base import ContainerNode
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class ChoiceNode(ContainerNode):
    tag_name = TagName.Choice

    @property
    def body(self):
        return self.node_for_tag[TagName.BODY]

    @property
    def output(self):
        return self.node_for_tag.get(TagName.OUTPUT)

    @property
    def selection_value(self):
        return self.node_for_tag[TagName.SelectionValue].value

    def execute_render_from_list(self, context):
        context.output.set(execute_render(self.body, context))
        if self.output:
            execute_render(self.output, context)
        return context.output.value

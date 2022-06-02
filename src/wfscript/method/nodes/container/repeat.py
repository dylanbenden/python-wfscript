from .base import ContainerNode
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class RepeatContainerNode(ContainerNode):
    tag_name = TagName.REPEAT

    @property
    def collection(self):
        return self.node_for_tag[TagName.Collection]

    @property
    def body(self):
        return self.node_for_tag[TagName.BODY]

    def execute_render_from_list(self, context):
        output = list()
        collection = execute_render(self.collection, context)
        for item in collection:
            context.set_item(item)
            output.append(execute_render(self.body, context))
        context.append_debug(output)
        return output

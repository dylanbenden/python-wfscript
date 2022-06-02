from .base import ContainerNode
from ....constants.method import TagName
from ....runtime.output import StepReturn
from ....runtime.utils.render import execute_render


class BodyContainerNode(ContainerNode):
    tag_name = TagName.BODY

    def execute_render_from_list(self, context):
        output = list()
        for operation in self.value:
            result = execute_render(operation, context)
            context.append_debug(result)
            output.append(result)
            if isinstance(result, StepReturn):
                return result
        return output

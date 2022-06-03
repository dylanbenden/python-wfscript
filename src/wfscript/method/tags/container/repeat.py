from .base import ContainerTag
from ....constants.method import TagName


class RepeatSectionTag(ContainerTag):
    tag_name = TagName.REPEAT
    label_child_tags = True
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]

    def render_from_dict(self, context, **kwargs):
        output = list()
        collection = self.value[TagName.Collection].render(context)
        body_node = self.value[TagName.BODY]
        for item in collection:
            context.update_runtime({TagName.Item: item})
            output.append((item, body_node.render(context)))
        return output

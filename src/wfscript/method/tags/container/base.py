from ....constants.method import TagName
from ..base import YAMLConfigured


class ContainerTag(YAMLConfigured):
    permitted_contents = None

    @property
    def items(self):
        return self.value[TagName.BODY]

    def render_from_list(self, context, **_):
        return [
            item.render(context)
            for item in self.items
        ]

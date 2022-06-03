from .base import ContainerTag
from ....constants.method import TagName


class ChoiceTag(ContainerTag):
    tag_name = TagName.Choice
    label_child_tags = True

    @property
    def selection_value(self):
        return self.value[TagName.SelectionValue].value

    def render_from_dict(self, context, **kwargs):
        return self.value[TagName.BODY].render(context)

from .base import ContainerTag
from ....constants.method import TagName


class ChoiceTag(ContainerTag):
    tag_name = TagName.Choice
    construct_value_as_mapping = True

    @property
    def body(self):
        return self.value[TagName.BODY]

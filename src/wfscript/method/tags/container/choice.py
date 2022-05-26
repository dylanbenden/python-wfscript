from .base import ContainerTag
from ....constants.method import TagName


class ChoiceTag(ContainerTag):
    tag_name = TagName.Choice
    use_child_tags_as_labels = True

    @property
    def body(self):
        return self.value[TagName.BODY]

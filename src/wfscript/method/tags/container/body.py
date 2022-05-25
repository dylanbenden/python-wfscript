from .base import ContainerTag
from ....constants.method import TagName


class BodySectionTag(ContainerTag):
    tag_name = TagName.BODY
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]

    @property
    def items(self):
        return self.value
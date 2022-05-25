from .base import ContainerTag
from ....constants.method import TagName


class RepeatSectionTag(ContainerTag):
    tag_name = TagName.REPEAT
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]
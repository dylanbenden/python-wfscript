from .base import LabelTag
from ....constants.method import TagName


class VersionTag(LabelTag):
    tag_name = TagName.version
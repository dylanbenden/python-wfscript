from .base import YAMLConfigured
from ...constants.method import TagName


class LabelTag(YAMLConfigured):
    def render_from_scalar(self, *_, **kwargs):
        return self.value


class NameTag(LabelTag):
    tag_name = TagName.NAME


class NamespaceTag(LabelTag):
    tag_name = TagName.NAMESPACE


class VersionTag(LabelTag):
    tag_name = TagName.VERSION


class StatusTag(LabelTag):
    tag_name = TagName.STATUS

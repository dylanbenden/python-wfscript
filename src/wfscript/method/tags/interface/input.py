from ..base import YAMLConfigured
from ....constants.method import TagName


class InputSectionTag(YAMLConfigured):
    tag_name = TagName.INPUT

    def render(self, *_):
        return self.value

from ..base import YAMLConfigured
from ....constants.method import TagName


class CollectionTag(YAMLConfigured):
    tag_name = TagName.Collection

    def render(self, context, **kwargs):
        raise NotImplementedError('not sure we will use this')
from ..base import YAMLConfigured
from ....constants.method import TagName


class SelectionSourceTag(YAMLConfigured):
    tag_name = TagName.SelectionSource

    def render_from_list(self, context, **kwargs):
        # for now, assume that there is only one data item provided
        return self.value[0].render(context)

from .base import DataSourceTag
from ....constants.method import TagName


class ItemTag(DataSourceTag):
    tag_name = TagName.Item

    def render_from_scalar(self, context, **kwargs):
        item_obj = context.runtime[TagName.Item]
        if self.value:
            return self.traverse_name_key(self.value, item=item_obj)
        return item_obj

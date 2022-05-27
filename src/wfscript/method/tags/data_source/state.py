from .base import DataSourceTag
from ..base import YAMLConfigured
from ....constants.method import TagName


class StateTag(DataSourceTag):
    tag_name = TagName.State

    def data_source(self, context):
        return context.state

    def render_from_dict(self, context, **kwargs):
        # mapping config means we are *setting* !State
        context.state.update(
            dict(
                {
                    key: value.render(context)
                    for key, value in self.value.items() if isinstance(value, YAMLConfigured)
                },
                **{
                    key: value
                    for key, value in self.value.items() if not isinstance(value, YAMLConfigured)
                }
            )
        )
        return '!State updated'

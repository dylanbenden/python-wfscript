from ..base import YAMLConfigured
from ....constants.method import TagName


class OutputSectionTag(YAMLConfigured):
    tag_name = TagName.OUTPUT

    def render_from_dict(self, context, **kwargs):
        return dict(
            {
                key: value.render_for_output(context)
                for key, value in self.value.items() if isinstance(value, YAMLConfigured)
            },
            **{
                key: value
                for key, value in self.value.items() if not isinstance(value, YAMLConfigured)
            }
        )
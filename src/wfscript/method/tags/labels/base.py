from ..base import YAMLConfigured


class LabelTag(YAMLConfigured):
    def render_from_scalar(self, *_, **kwargs):
        return self.value
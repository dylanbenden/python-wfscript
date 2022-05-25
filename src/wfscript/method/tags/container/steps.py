from .base import ContainerTag
from ....constants.method import TagName


class StepsSectionTag(ContainerTag):
    tag_name = TagName.STEPS
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]

    def render(self, context, from_item=0):
        # steps render one per request
        return self.value[from_item].render()
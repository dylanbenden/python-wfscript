from .base import ContainerTag
from ....constants.method import TagName
from ....constants.payload import PayloadKey


class StepsSectionTag(ContainerTag):
    tag_name = TagName.STEPS
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]

    def render(self, context, from_item=0):
        last_step_name = context.resume_info.get(PayloadKey.STEP)
        if last_step_name is None:
            next_step_tag = self.value[0]
        else:
            try:
                last_step_index = [i.name for i in self.value].index(last_step_name)
            except ValueError:
                raise RuntimeError(f'No such step name: {last_step_name}; '
                                   f'Options: {[step.name for step in self.value]}')
            if last_step_index < len(self.value):
                next_step_tag = self.value[last_step_index + 1]
            else:
                raise RuntimeError(f'There are no steps after {last_step_name}')
        result = next_step_tag.render(context)
        result.add_step_resume_info(
            method=context.method,
            step=next_step_tag.name
        )
        return result

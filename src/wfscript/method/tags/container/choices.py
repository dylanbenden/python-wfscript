from .base import ContainerTag
from ....constants.method import TagName


class ChoicesSectionTag(ContainerTag):
    tag_name = TagName.CHOICES
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]

    def select_choice(self, runtime_selection):
        options = list()
        for choice in self.value[1:]:
            options.append(choice.selection_value)
            if choice.selection_value == runtime_selection:
                return choice
        raise RuntimeError(f'No choice defined matching selection "{runtime_selection}"; '
                           f'Valid options: {options}')

    def render_from_list(self, context, **kwargs):
        runtime_selection = self.value[0].render(context)
        choice_for_selection = self.select_choice(runtime_selection)
        return choice_for_selection.render(context)

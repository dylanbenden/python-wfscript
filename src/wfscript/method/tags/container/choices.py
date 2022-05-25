from .base import ContainerTag
from ....constants.method import TagName


class ChoicesSectionTag(ContainerTag):
    tag_name = TagName.CHOICES
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]

    def select_choice_body(self, runtime_selection):
        options = {
            option.value[TagName.SelectionValue]: option.value[TagName.BODY]
            for option in self.value[1:]
        }
        if runtime_selection in options:
            return options[runtime_selection]
        raise RuntimeError(f'No choice defined for "{runtime_selection}"; Valid options: {list(options.keys())}')

    def render_from_list(self, context, **kwargs):
        runtime_selection = self.value[0].render(context)
        return [
            item.render(context)
            for item in self.select_choice_body(runtime_selection)
        ]
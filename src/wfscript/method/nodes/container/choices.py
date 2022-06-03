from .base import ContainerNode
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class ChoicesContainerNode(ContainerNode):
    tag_name = TagName.CHOICES

    @property
    def selection(self):
        return self.value[0]

    @property
    def choices(self):
        return self.value[1:]

    def select_choice(self, runtime_selection):
        options = list()
        for choice_node in self.choices:
            options.append(choice_node.selection_value)
            if choice_node.selection_value == runtime_selection:
                return choice_node
        raise RuntimeError(f'No choice defined matching selection "{runtime_selection}"; '
                           f'Valid options: {options}')

    def execute_render_from_list(self, context):
        runtime_selection = execute_render(self.selection, context)
        return execute_render(self.select_choice(runtime_selection), context)

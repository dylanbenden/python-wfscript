from ....runtime.utils.render import output_render
from ..base import WorkflowNode, DualPhase


class DataSourceNode(WorkflowNode, DualPhase):
    tag_name = None

    def data_source(self, context):
        raise NotImplementedError(f'{self.__class__.__name__} must implement data_source()')

    def update(self, data, context):
        self.data_source(context).update(data)

    def traverse_name_key(self, name_key, data_source=None, item=None):
        elements_to_traverse = name_key.split('.')
        current_name = elements_to_traverse[0]
        additional_names = None
        if len(elements_to_traverse) > 1:
            additional_names = '.'.join(elements_to_traverse[1:])
        if item is None:
            source_data = data_source.value
            if isinstance(source_data, dict):
                item = source_data[current_name]
            elif isinstance(source_data, list):
                item = source_data[int(current_name)]
            else:
                item = getattr(source_data, current_name, None)
        else:
            if isinstance(item, dict):
                item = item[current_name]
            elif isinstance(item, list):
                item = item[int(current_name)]
            else:
                item = getattr(item, current_name)
        if additional_names:
            return self.traverse_name_key(name_key=additional_names, item=item)
        return item

    def execute_render_from_scalar(self, context):
        return self.traverse_name_key(name_key=self.value, data_source=self.data_source(context))

    def output_render_from_scalar(self, context):
        return output_render(
            self.traverse_name_key(name_key=self.value, data_source=self.data_source(context)),
            context
        )

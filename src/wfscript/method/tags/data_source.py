from .base import YAMLConfigured
from ...constants.method import TagName


class DataSourceTag(YAMLConfigured):
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
            item = data_source[current_name]
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

    def render_from_scalar(self, context):
        return self.traverse_name_key(name_key=self.value, data_source=self.data_source(context))


class StateTag(DataSourceTag):
    tag_name = TagName.State

    def data_source(self, context):
        return context.state


class InputTag(DataSourceTag):
    tag_name = TagName.Input

    def data_source(self, context):
        return context.input


class OutputTag(DataSourceTag):
    tag_name = TagName.Output

    def data_source(self, context):
        return context.output

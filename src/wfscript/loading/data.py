from .base import YAMLConfiguredObject
from ..constants.loading import TagName


class ContextRenderedTag(YAMLConfiguredObject):
    _lock = False

    def data_source(self, context):
        raise NotImplementedError(f'{self.__class__.__name__}.data_source must be implemented by subclass')

    def lock(self):
        self._lock = True

    def update(self, data, context):
        if self._lock:
            raise RuntimeError(f'{self.__class__.__name__} data may not be updated')
        self.data_source(context).update(data)

    def render_payload(self, context):
        name_key = self.value
        attribute = None
        data_source = self.data_source(context)
        if '.' in name_key:
            name_key, attribute = name_key.split('.')
        if attribute:
            return getattr(data_source[name_key], attribute)
        else:
            return data_source[name_key]


class StateTag(ContextRenderedTag):
    tag_name = TagName.State

    def data_source(self, context):
        return context.state


class InputTag(ContextRenderedTag):
    tag_name = TagName.Input

    def data_source(self, context):
        return context.input


class OutputTag(ContextRenderedTag):
    tag_name = TagName.Output

    def data_source(self, context):
        return context.output

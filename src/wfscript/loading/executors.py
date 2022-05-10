from ..constants.loading import TagName, MethodKeyword
from ..loading.base import YAMLConfiguredObject


class ExecutorTag(YAMLConfiguredObject):
    tag_name = None
    return_value = None

    @property
    def identity(self):
        return self._value[MethodKeyword.IDENTITY]

    @property
    def input(self):
        return self._value.get(MethodKeyword.INPUT, dict())

    @property
    def output_target(self):
        return self._value.get(MethodKeyword.OUTPUT_TARGET)

    def execute(self, context):
        executor = self.get_executor(context)
        return_value = executor(**self.input)
        if self.output_target:
            return {self.output_target.tag: {self.output_target.value: return_value}}


class ActionTag(ExecutorTag):
    tag_name = TagName.Action

    def get_executor(self, context):
        return context.namespace_root.get_action(self.identity)


class MethodTag(ExecutorTag):
    tag_name = TagName.Method

    def get_executor(self, context):
        return context.namespace_root.get_method(self.identity)

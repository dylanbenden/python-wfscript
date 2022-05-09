from ..constants.loading import TagName, MethodKeyword
from ..loading.base import YAMLConfiguredObject


class ActionTag(YAMLConfiguredObject):
    tag_name = TagName.Action
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
        executor = context.namespace_root.get_action(self.identity)
        return_value = executor(**self.input)
        if self.output_target:
            return {self.output_target.tag: {self.output_target.value: return_value}}

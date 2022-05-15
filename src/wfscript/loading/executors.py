from ..constants.loading import TagName, MethodKeyword
from ..loading.base import YAMLConfiguredObject
from ..runtime.context import get_inner_context
from ..runtime.output import MethodReturn, ActionReturn, StepReturn


class ExecutorTag(YAMLConfiguredObject):
    return_klass = None
    tag_name = None
    execute_method = None
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

    def handle_return(self, return_value):
        if self.output_target:
            return {self.output_target.tag: {self.output_target.value: return_value}}

    def render_payload(self, context):
        from ..utils.method import render_tag_dict
        return render_tag_dict(self.value[MethodKeyword.INPUT], context)


class ActionTag(ExecutorTag):
    tag_name = TagName.Action
    return_klass = ActionReturn

    def execute(self, context):
        executor = context.namespace_root.get_action(self.identity)
        return ActionReturn(executor(**self.input), context)


class MethodTag(ExecutorTag):
    tag_name = TagName.Method
    return_klass = MethodReturn

    def execute(self, context):
        executor = context.namespace_root.get_method(self.identity)
        new_context = get_inner_context(self.identity, context, self.render_payload(context))
        output_target = self.value.get(MethodKeyword.OUTPUT_TARGET, dict())
        return executor.run_from_tag(new_context, output_target)


class StepTag(ExecutorTag):
    tag_name = TagName.Step
    return_klass = StepReturn


class ValidatorTag(ExecutorTag):
    tag_name = TagName.Validator

    def get_executor(self, context):
        return context.namespace_root.get_validator(self.identity)

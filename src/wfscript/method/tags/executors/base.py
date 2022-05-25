from ..base import YAMLConfigured
from ....constants.method import TagName, MethodKeyword
from ....runtime.utils.identity import construct_identity


class ExecutorTag(YAMLConfigured):
    # return_klass = None
    tag_name = None
    construct_value_as_mapping = True
    # execute_method = None
    # return_value = None

    @property
    def identity(self):
        try:
            identity_info = self._value[TagName.IDENTITY]
        except:
            import ipdb; ipdb.set_trace()
            pass
        if isinstance(identity_info, dict):
            return construct_identity(identity_info)
        return identity_info

    @property
    def input(self):
        return self._value.get(TagName.INPUT, dict())

    @property
    def output(self):
        return self._value.get(TagName.OUTPUT)

    @property
    def output_target(self):
        return self._value.get(MethodKeyword.OUTPUT_TARGET)

    def handle_return(self, return_value):
        if self.output_target:
            return {self.output_target.tag: {self.output_target.value: return_value}}

    def render_from_dict(self, context, **_):
        return self.execute(context)

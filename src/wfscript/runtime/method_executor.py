from .utils.render import output_render
from ..constants.method import TagName
from ..constants.payload import PayloadKey
from ..runtime.context import get_context
from ..runtime.output import MethodReturn, StepReturn


class MethodExecutor(object):
    def __init__(self, identity, loaded_yaml, namespace_root):
        self._identity = identity
        self._document = loaded_yaml
        self._namespace_root = namespace_root

    @property
    def identity(self):
        return self._identity

    @property
    def document(self):
        return self._document

    @property
    def namespace_root(self):
        return self._namespace_root

    @property
    def input(self):
        if TagName.OUTPUT in self.document:
            return self.document[TagName.INPUT]

    @property
    def output(self):
        if TagName.OUTPUT in self.document:
            return self.document[TagName.OUTPUT]

    @property
    def container(self):
        non_container_tag_types = [TagName.IDENTITY, TagName.INPUT, TagName.OUTPUT]
        container_tags = [item for item in self.document if item not in non_container_tag_types]
        if len(container_tags) not in [0, 1]:
            raise RuntimeError(f'Each method must have exactly zero or one container tag; Received: {container_tags}')
        if len(container_tags) == 1:
            return self.document[container_tags[0]]

    def execute(self, input_data=None, state=None, resume_info=None, context=None):
        from .utils.render import execute_render
        if context is None:
            context = get_context(
                identity=self.identity,
                namespace_root=self.namespace_root,
                input_data=input_data,
                state=state,
                resume_info=resume_info
            )
        try:
            context.set_output(execute_render(self.container, context))
            if isinstance(context.output.value, StepReturn):
                return context.output.value
            return MethodReturn(output_render(self.output, context))
        except RuntimeError as err:
            msg = f'While executing {context.method} the following exception was raised:\n' \
                  f'\t - {str(err)}' \
                  f'\n\n' \
                  f'Input Data: {context.request[PayloadKey.INPUT].value}\n' \
                  f'Resume Info: {context.resume_info}'
            raise RuntimeError(msg)

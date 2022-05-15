from .base import DocumentExecutor
from ..constants.loading import TagName
from ..constants.payload import PayloadKey
from ..runtime.context import get_context
from ..runtime.output import MethodReturn
from ..utils.method import handle_method_or_step_body, render_tag_dict


class MethodExecutor(DocumentExecutor):
    @property
    def meta_section(self):
        return self._document[TagName.META].value

    @property
    def input_section(self):
        return self._document[TagName.INPUT].value

    @property
    def body_section(self):
        if TagName.BODY in self._document:
            return self._document[TagName.BODY].value
        return list()

    @property
    def return_section(self):
        if self._document.get(TagName.RETURN):
            return self._document[TagName.RETURN].value
        else:
            raise RuntimeError(f'Method {self.identity} is missing a !RETURN section')

    def run_from_tag(self, context, output_target):
        output = self._run(context)
        if output_target:
            return {output_target.tag: output.result}
        return output

    def run(self, input_data=None, state=None):
        context = get_context(self.identity, self.namespace_root, input_data, state)
        result = self._run(context)
        return result.render()

    def _run(self, context):
        try:
            next_items = self._load_next_items(context)
            possible_step_return = handle_method_or_step_body(next_items, context)
            if possible_step_return is None:
                # we got to the end of the Method body, time to render a return
                result = MethodReturn(
                    result=render_tag_dict(self.return_section, context),
                    context=context
                )
            return result
        except RuntimeError as err:
            msg = f'While executing {context.method} the following exception was raised:\n' \
                  f'\t - {str(err)}' \
                  f'\n\n' \
                  f'Input Data: {context.request[PayloadKey.INPUT].value}'
            raise RuntimeError(msg)

    def _load_next_items(self, context):
        if context.state.last_method is not None:
            raise NotImplemented('todo: body_items_after_node')
        return self.body_section

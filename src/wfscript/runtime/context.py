from .data import Output, State, Input, Item
from ..constants.payload import PayloadKey


class RunContext(object):
    def __init__(self, namespace_root=None, request=None, state=None, resume_info=None):
        self._namespace_root = namespace_root
        self._request = request
        self._output = Output()
        self._item = Item()
        if state is not None:
            if isinstance(state, State):
                self._state = state
            else:
                self._state = State(state)
        else:
            self._state = State()
        self._resume_info = resume_info or dict()
        self._debug = list()

    @property
    def method(self):
        return self._request[PayloadKey.METHOD]

    @property
    def namespace_root(self):
        return self._namespace_root

    @property
    def request(self):
        return self._request

    @property
    def input(self):
        return self._request.get(PayloadKey.INPUT, dict())

    @property
    def output(self):
        return self._output

    @property
    def item(self):
        return self._item

    @property
    def state(self):
        return self._state

    @property
    def runtime(self):
        return self._runtime

    @property
    def resume_info(self):
        return self._resume_info

    @property
    def debug(self):
        return self._debug

    def set_output(self, value):
        self._output.set(value)

    def set_item(self, value):
        self._item.set(value)

    def append_debug(self, result):
        self._debug.append(result)


def get_context(identity, namespace_root, input_data=None, state=None, resume_info=None):
    if input_data is None:
        input_data = dict()
    if state is None:
        state = dict()
    request = {
        PayloadKey.METHOD: identity,
        PayloadKey.INPUT: Input(input_data)
    }
    return RunContext(
        namespace_root=namespace_root,
        request=request,
        resume_info=resume_info,
        state=state
    )

def get_inner_context(new_identity, old_context, input_data):
    return get_context(new_identity, old_context.namespace_root, input_data, old_context.state)

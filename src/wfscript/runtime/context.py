import uuid

from .data import Output, State, Input
from ..constants.payload import PayloadKey


class RunContext(object):
    def __init__(self, namespace_root=None, request=None, state=None, resume_info=None, skip_validation=False):
        self._namespace_root = namespace_root
        self._request = request
        self._output = Output()
        if state is not None:
            if isinstance(state, State):
                self._state = state
            else:
                self._state = State(state)
        else:
            self._state = State()
        self._runtime = dict()
        self._last_step = resume_info
        self._run_id = request.get('run_id', str(uuid.uuid4()))
        # if not skip_validation:
        #     self.validate_input()

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
    def state(self):
        return self._state

    @property
    def runtime(self):
        return self._runtime

    @property
    def last_step(self):
        return self._last_step

    @property
    def run_id(self):
        return self._run_id

    def update_runtime(self, data):
        self._runtime.update(data)

    # probably not the correct moment to do validation
    # def validate_input(self):
    #     validator = self.namespace_root.get_validator(self.method, self.last_step)
    #     validator.validate(self.input.value)


def get_context(identity, namespace_root, input_data=None, state=None, resume_info=None, skip_validation=False):
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
        state=state,
        skip_validation=skip_validation
    )

def get_inner_context(new_identity, old_context, input_data):
    return get_context(new_identity, old_context.namespace_root, input_data, old_context.state)

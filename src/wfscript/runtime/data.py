from copy import deepcopy

from .utils.json import unfloat
from ..constants.payload import PayloadKey


class BaseRuntimeData(object):
    def __init__(self, data=None, run_identity=None):
        self._run_identity = run_identity
        if data is not None:
            self._value = unfloat(deepcopy(data))
        else:
            self._value = dict()

    @property
    def value(self):
        return self._value

    @property
    def run_identity(self):
        return self._run_identity

    def update(self, new_data):
        self._value.update(unfloat(new_data))

    def __getitem__(self, item):
        if item not in self.value:
            raise RuntimeError(f'{self.__class__.__name__} has no item {item}')
        return self.value[item]

    def __setitem__(self, key, value):
        raise RuntimeError(f'You may not set values directly on {self.__class__.__name__}, use '
                           f'update() instead')


class Input(BaseRuntimeData):
    # non-persisted store for data provided at invocation
    pass


class Output(BaseRuntimeData):
    # non-persisted collector for data generated at runtime
    pass

class State(BaseRuntimeData):
    _last_method = None
    _last_step = None

    @property
    def last_method(self):
        return self._last_method

    @property
    def last_step(self):
        return self._last_step

    @property
    def resume_info(self):
        return {
            PayloadKey.STATE: self.value,
            PayloadKey.METHOD: self.last_method,
            PayloadKey.STEP: self.last_step
        }

    def set_resume_state(self, method, step):
        self._last_method = method
        self._last_step = step

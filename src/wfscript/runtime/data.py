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
        unfloated_data = unfloat(new_data)
        if isinstance(unfloated_data, dict):
            self._value.update(unfloated_data)
        else:
            if not isinstance(self.value, dict):
                self._value.update({self.value: unfloated_data})

    def set(self, new_data):
        self._value = unfloat(new_data)

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
    pass

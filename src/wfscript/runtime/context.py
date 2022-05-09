class RunContext(object):
    def __init__(self, namespace_root, data, state):
        self._namespace_root = namespace_root
        self._data = data
        self._state = state

    @property
    def namespace_root(self):
        return self._namespace_root

    @property
    def data(self):
        return self._data

    @property
    def state(self):
        return self._state

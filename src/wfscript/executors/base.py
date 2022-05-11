class DocumentExecutor(object):
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
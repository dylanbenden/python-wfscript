from ..constants.loading import TagName
from ..utils.identity import construct_identity
from ..utils.names import find_yaml_files


class NamespaceRoot(object):
    def __init__(self, identity, file_path, actions, contained_namespaces):
        self._identity = identity
        self._path = '/'.join(file_path.split('/')[:-1])
        self._actions = actions
        self._contained_namespaces = contained_namespaces
        self._methods = dict()

    @property
    def identity(self):
        return self._identity

    @property
    def path(self):
        return self._path

    @property
    def actions(self):
        return self._actions

    @property
    def contained_namespaces(self):
        return self._contained_namespaces

    @property
    def methods(self):
        return self._methods

    def load_methods(self):
        from ..loading.loader import load_yaml_document
        for method_path in find_yaml_files(self):
            with open(method_path, 'r') as document:
                method = load_yaml_document(document.read())
                # todo: WFS-16 - validate method on load
                method_identity = construct_identity(method[TagName.META].value)
                self._methods[method_identity] = method

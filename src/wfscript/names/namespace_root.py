from ..constants.identity import IdentityDelimeter
from ..constants.loading import TagName, MetaSectionKey, MetaStatusChoice
from ..utils.identity import construct_identity
from ..utils.names import find_yaml_files


class NamespaceRoot(object):
    def __init__(self, identity, file_path, actions, contained_namespaces, unit_test_loading_bypass=False):
        self._identity = identity
        self._path = '/'.join(file_path.split('/')[:-1])
        self._actions = dict()
        self._action_functions = actions
        self._contained_namespaces = contained_namespaces
        self._methods = dict()
        if not unit_test_loading_bypass:
            self.load_methods()
            self.load_actions()

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
        semantic_versions = dict()
        for method_path in find_yaml_files(self):
            with open(method_path, 'r') as document:
                method = load_yaml_document(document.read())
                # todo: WFS-16 - validate method on load
                method_identity = construct_identity(method[TagName.META].value)
                numeric_version = method[TagName.META].value[MetaSectionKey.VERSION]
                semantic_version = method[TagName.META].value[MetaSectionKey.STATUS]
                if numeric_version > semantic_versions.get(semantic_version, 0):
                    semantic_versions[semantic_version] = numeric_version
                    default_identity = f'{method_identity.split(IdentityDelimeter.VERSION)[0]}'
                    semantic_identity = f'{default_identity}{IdentityDelimeter.VERSION}{semantic_version}'
                    self._methods[semantic_identity] = method
                    if semantic_version == MetaStatusChoice.PRODUCTION:
                        # latest production version is also default version
                        self._methods[default_identity] = method
                self._methods[method_identity] = method

    def load_actions(self):
        from .store import NameStore
        for action in self._action_functions:
            action_versions = NameStore.pop_action_versions(action.__name__)
            for action_identity, fx in action_versions:
                self._actions[action_identity] = fx

    def get_action(self, identity):
        if identity in self.actions:
            return self.actions[identity]
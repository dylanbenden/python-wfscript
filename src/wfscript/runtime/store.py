from collections import defaultdict

from .namespace_root import NamespaceRoot

_names = dict()
_actions = defaultdict(list)


class NameStore(object):
    @classmethod
    def exists(cls, identity):
        return identity in _names

    @classmethod
    def namespace_root(cls, identity, file_path, actions, contained_namespaces, unit_test_loading_bypass=False):
        global _names
        if identity in _names:
            raise RuntimeError(f'Attempt to register the same namespace root more than once: {identity}'
                               f'Attempted registration from unique_names: {_names[identity].unique_name} and '
                               f'{identity}')
        nsr = NamespaceRoot(
            identity=identity,
            file_path=file_path,
            actions=actions,
            contained_namespaces=contained_namespaces,
            unit_test_loading_bypass=unit_test_loading_bypass
        )
        _names[identity] = nsr
        return nsr

    @classmethod
    def register_action(cls, action_identity, fx):
        global _actions
        _actions[fx.__module__].append((action_identity, fx))

    @classmethod
    def pop_action_versions(cls, fx_module):
        global _actions
        return _actions.pop(fx_module)

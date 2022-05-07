from .namespace_root import NamespaceRoot

_names = dict()


class NameStore(object):
    @classmethod
    def exists(cls, identity):
        return identity in _names

    @classmethod
    def namespace_root(cls, identity, file_path, actions, contained_namespaces):
        global _names
        if identity in _names:
            raise RuntimeError(f'Attempt to register the same namespace root more than once: {identity}'
                               f'Attempted registration from unique_names: {_names[identity].unique_name} and '
                               f'{identity}')
        nsr = NamespaceRoot(
            identity=identity,
            file_path=file_path,
            actions=actions,
            contained_namespaces=contained_namespaces
        )
        _names[identity] = nsr
        return nsr

from ...names.store import NameStore

validation_namespace_root = NameStore.namespace_root(
    identity=__name__,
    file_path=__file__,
    actions=[],
    contained_namespaces=[]
)
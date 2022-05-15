from . import hello_world
from ....names.store import NameStore

executing_namespace_root = NameStore.namespace_root(
    identity=__name__,
    file_path=__file__,
    actions=[hello_world],
    contained_namespaces=[]
)
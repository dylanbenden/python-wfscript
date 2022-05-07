import os

from ...names.store import NameStore
from ...names.namespace_root import NamespaceRoot

content_root_path = os.path.sep.join(__file__.split(os.path.sep)[:-1])

content_root_module = __name__

testing_namespace_root = NameStore.namespace_root(
    identity=__name__,
    file_path=__file__,
    actions=[],
    contained_namespaces=[]
)
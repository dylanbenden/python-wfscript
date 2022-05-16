from . import hello_world, accept_offer, add_prospect, send_hire_letter
from ....names.store import NameStore

executing_namespace_root = NameStore.namespace_root(
    identity=__name__,
    file_path=__file__,
    actions=[hello_world, accept_offer, add_prospect, send_hire_letter],
    contained_namespaces=[]
)
from ..content_root.loading import loading_namespace_root
from ...names.store import NameStore


def test_exists():
    assert NameStore.exists(loading_namespace_root.identity) is True


def test_namespace_root():
    assert NameStore.exists(__name__) is False
    new_ns_root = NameStore.namespace_root(
        identity=__name__,
        file_path=__file__,
        actions=list(),
        contained_namespaces=list()
    )
    assert new_ns_root.identity == __name__
    assert NameStore.exists(new_ns_root.identity) is True

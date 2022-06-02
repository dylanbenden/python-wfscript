from ..constants import TagName
from . import run_label_node_tests


def test_namespace_node():
    run_label_node_tests(TagName.namespace)

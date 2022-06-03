from ..constants import TagName
from . import run_label_node_tests


def test_version_node():
    run_label_node_tests(TagName.version)

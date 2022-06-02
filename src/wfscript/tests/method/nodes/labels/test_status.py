from ..constants import TagName
from . import run_label_node_tests


def test_status_node():
    run_label_node_tests(TagName.status)

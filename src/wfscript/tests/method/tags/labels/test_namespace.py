from ..constants import TagName
from . import run_label_tag_tests


def test_namespace_tag():
    run_label_tag_tests(TagName.namespace)

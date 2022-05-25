from ..constants import TagName
from . import run_label_tag_tests


def test_version_tag():
    run_label_tag_tests(TagName.version)

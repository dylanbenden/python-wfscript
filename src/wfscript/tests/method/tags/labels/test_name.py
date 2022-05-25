from ..constants import TagName
from . import run_label_tag_tests


def test_name_tag():
    run_label_tag_tests(TagName.name)

from . import TestParam, run_data_source_tag_tests
from ..constants import TagName
from ....testing_tools.context import get_empty_context

def test_input_tag():
    tag_name = TagName.Input
    context = get_empty_context(input_data={TestParam.key_name: TestParam.value})
    run_data_source_tag_tests(tag_name, context)


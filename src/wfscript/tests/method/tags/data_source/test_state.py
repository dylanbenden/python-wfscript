from . import TestParam, run_data_source_tag_tests
from ..constants import TagName
from ....testing_tools.context import get_empty_context

def test_state_tag():
    tag_name = TagName.State
    context = get_empty_context(state={TestParam.key_name: TestParam.value})
    run_data_source_tag_tests(tag_name, context)


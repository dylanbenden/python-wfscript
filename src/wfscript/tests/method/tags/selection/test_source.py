from ..constants import TagName
from ....testing_tools.context import get_empty_context
from .....constants import ConstantNamespace
from .....method.document_loader import load_yaml


class TestParam(ConstantNamespace):
    input_name_key = 'my_input_name'
    input_value = 'my input value'


def test_selection_source_tag():
    snippet = f'''
      - {TagName.SelectionSource}
        - {TagName.Input} {TestParam.input_name_key}
    '''
    context = get_empty_context(input_data={TestParam.input_name_key: TestParam.input_value})
    node = load_yaml(snippet)[0]
    assert node.tag_name == TagName.SelectionSource
    assert node.value[0].tag_name == TagName.Input
    assert node.render(context) == TestParam.input_value

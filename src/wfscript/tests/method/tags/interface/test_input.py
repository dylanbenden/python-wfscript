from ....testing_tools.context import get_empty_context
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....constants.validation import DataType
from .....method.document_loader import load_method


class TestParam(ConstantNamespace):
    first_key_name = 'my_first_key'
    second_key_name = 'my_second_key'


def test_input_section_tag():
    snippet = f'''
    - {TagName.INPUT}
      {TestParam.first_key_name}:
        data_type: {DataType.STRING}
        required: true
      {TestParam.second_key_name}:
        data_type: {DataType.ARRAY}
        required: false
    '''
    result = load_method(snippet)
    input_node = result[TagName.INPUT]
    empty_context = get_empty_context()
    assert input_node.tag == TagName.INPUT
    assert input_node.value == {
        TestParam.first_key_name: {
            'data_type': DataType.STRING,
            'required': True
        },
        TestParam.second_key_name: {
            'data_type': DataType.ARRAY,
            'required': False
        }
    }
    assert input_node.render(empty_context) == input_node.value

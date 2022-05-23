from ....constants.method import TagName
from ....method.document_loader import load_yaml_document
from ....testing import get_empty_context


def test_input_section_tag():
    snippet = '''
    - !INPUT
      some_key_name:
        data_type: string
        required: true
      another_key_name:
        data_type: string
        required: true
    '''
    result = load_yaml_document(snippet)
    input_node = result[TagName.INPUT]
    empty_context = get_empty_context()
    assert input_node.tag == TagName.INPUT
    assert input_node.value == {
        'some_key_name': {
            'data_type': 'string',
            'required': True
        },
        'another_key_name': {
            'data_type': 'string',
            'required': True
        }
    }
    assert input_node.render(empty_context) == input_node.value

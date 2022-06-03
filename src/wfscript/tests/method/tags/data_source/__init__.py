from .....constants import ConstantNamespace
from .....method.document_loader import load_yaml


class TestParam(ConstantNamespace):
    key_name = 'my_key'
    value = 'some value'


def run_data_source_tag_tests(tag_name, context):
    print(f'Running data_source tag tests for {tag_name}')
    snippet = f'''
      - {tag_name} {TestParam.key_name}
    '''
    node = load_yaml(snippet)[0]
    assert node.tag == tag_name
    assert node.value == TestParam.key_name
    assert node.render(context) == TestParam.value

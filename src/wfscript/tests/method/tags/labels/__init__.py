from ....testing_tools.context import get_empty_context
from .....constants import ConstantNamespace
from .....method.document_loader import load_yaml


class TestParam(ConstantNamespace):
    value = 'some value'


def run_label_tag_tests(tag_name):
    snippet = f'''
    - {tag_name} {TestParam.value}
    '''
    node = load_yaml(snippet)[0]
    empty_context = get_empty_context()
    assert node.tag == tag_name
    assert node.value == TestParam.value
    assert node.render(empty_context) == TestParam.value


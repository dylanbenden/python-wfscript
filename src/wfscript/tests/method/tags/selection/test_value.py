from ..constants import TagName
from ....testing_tools.context import get_empty_context
from .....constants import ConstantNamespace
from .....method.document_loader import load_yaml


class TestParam(ConstantNamespace):
    selection_value = 'my selection value'


def test_selection_value_tag():
    snippet = f'''
      - {TagName.SelectionValue}
        - {TestParam.selection_value}
    '''
    context = get_empty_context()
    node = load_yaml(snippet)[0]
    assert node.tag_name == TagName.SelectionValue
    assert node.render(context) == TestParam.selection_value

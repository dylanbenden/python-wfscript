from ....testing_tools.mocks import get_context_with_mocks
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.document_loader import load_yaml
from .....method.tags.container import ChoiceTag


class TestParam(ConstantNamespace):
    method_identity = 'path/to::some_method==production'
    user_selection_value = 'some_selection_name'


def test_choice_tag():
    snippet = f'''
      - {TagName.Choice}
        - {TagName.SelectionValue}
          - {TestParam.user_selection_value}
        - {TagName.BODY}
          - {TagName.Method}
            - {TagName.IDENTITY} {TestParam.method_identity}
    '''
    context = get_context_with_mocks()
    node = load_yaml(snippet)[0]
    assert isinstance(node, ChoiceTag) is True
    # output will be outputs of !BODY, a collection of executor outputs
    output = node.render(context)
    assert output[0].result == f'Mock-executed method {TestParam.method_identity}'

from ....testing_tools.mocks import get_context_with_mocks
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.document_loader import load_yaml
from .....method.tags.container import ChoiceTag, RepeatSectionTag


class TestParam(ConstantNamespace):
    method_identity = 'path/to::some_method==production'
    item_list_name = 'my_list_of_stuff'
    first_list_item = 'abc'
    second_list_item = '123'
    item_list_value = [first_list_item, second_list_item]



def test_repeat_tag():
    snippet = f'''
      - {TagName.REPEAT}
        - {TagName.Collection}
          - {TagName.Input} {TestParam.item_list_name}
        - {TagName.BODY}
          - {TagName.Method}
            - {TagName.IDENTITY} {TestParam.method_identity}
            - {TagName.INPUT}
              collected_ids: {TagName.Item}
    '''
    context = get_context_with_mocks(
        input_data={TestParam.item_list_name: TestParam.item_list_value}
    )
    node = load_yaml(snippet)[0]
    assert isinstance(node, RepeatSectionTag) is True
    # output will be list of outputs of each !BODY run
    output = node.render(context)

    first_iteration = output[0]
    item, body_output = first_iteration
    assert body_output[0].result == f'Mock-executed method {TestParam.method_identity}'
    assert item == TestParam.first_list_item

    second_iteration = output[1]
    item, body_output = second_iteration
    assert body_output[0].result == f'Mock-executed method {TestParam.method_identity}'
    assert item == TestParam.second_list_item

from ....testing_tools.mocks import get_context_with_mocks
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.document_loader import load_yaml
from .....runtime.output import MethodReturn


class TestParam(ConstantNamespace):
    data_source_key = 'user_selection'
    user_selection_value = 'my choice'
    alternate_user_selection_value = 'my different choice'
    selected_method_id = 'path/to::first_method==1.0'
    alternate_method_id = 'path/to::second_method==1.0'


def test_choices_tag():
    snippet = f'''
      - {TagName.CHOICES}
        - {TagName.SelectionSource}
          - {TagName.Input} {TestParam.data_source_key}
        - {TagName.Choice}
          - {TagName.SelectionValue}
            - {TestParam.user_selection_value}
          - {TagName.BODY}
            - {TagName.Method}
              - {TagName.IDENTITY} {TestParam.selected_method_id}
        - {TagName.Choice}
          - {TagName.SelectionValue}
            - {TestParam.alternate_user_selection_value}
          - {TagName.BODY}
            - {TagName.Method}
              - {TagName.IDENTITY} {TestParam.alternate_method_id}
    '''
    context = get_context_with_mocks(
        input_data={
            TestParam.data_source_key: TestParam.user_selection_value
        }
    )
    choices_node = load_yaml(snippet)[0]
    data_source_node = choices_node.value[0]
    assert data_source_node.render(context) == TestParam.user_selection_value

    first_choice_node = choices_node.value[1]
    first_for_value_node = first_choice_node.value[TagName.SelectionValue]
    assert first_for_value_node.value == TestParam.user_selection_value
    first_body_node = first_choice_node.value[TagName.BODY]
    first_method_node = first_body_node.value[0]
    assert first_method_node.identity == TestParam.selected_method_id

    second_choice_node = choices_node.value[2]
    second_for_value_node = second_choice_node.value[TagName.SelectionValue]
    assert second_for_value_node.value == TestParam.alternate_user_selection_value
    second_body_node = second_choice_node.value[TagName.BODY]
    second_method_node = second_body_node.value[0]
    assert second_method_node.identity == TestParam.alternate_method_id

    first_results = choices_node.render(context)[0]
    assert isinstance(first_results, MethodReturn) is True
    assert first_results.result == f'Mock-executed method {TestParam.selected_method_id}'

    # make alternate selection
    alt_context = get_context_with_mocks(
        input_data={
            TestParam.data_source_key: TestParam.alternate_user_selection_value
        }
    )
    alt_results = choices_node.render(alt_context)[0]
    assert isinstance(alt_results, MethodReturn) is True
    assert alt_results.result == f'Mock-executed method {TestParam.alternate_method_id}'

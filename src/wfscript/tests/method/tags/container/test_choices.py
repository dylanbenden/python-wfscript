from ....testing_tools.mocks import get_context_with_mock_domain
from .....constants.method import TagName
from .....method.document_loader import load_yaml


def test_choices_tag():
    data_source_key = 'user_selection'

    user_selection_value = 'my choice'
    alternate_user_selection_value = 'my different choice'

    selected_method_id = 'path/to::first_method==1.0'
    alternate_method_id = 'path/to::second_method==1.0'

    snippet = f'''
      - {TagName.CHOICES}
        - {TagName.SelectionSource}
          - {TagName.Input} {data_source_key}
        - {TagName.Choice}
          - {TagName.SelectionValue}
            - {user_selection_value}
          - {TagName.BODY}
            - {TagName.Method}
              - {TagName.IDENTITY} {selected_method_id}
        - {TagName.Choice}
          - {TagName.SelectionValue}
            - {alternate_user_selection_value}
          - {TagName.BODY}
            - {TagName.Method}
              - {TagName.IDENTITY} {alternate_method_id}
    '''
    context = get_context_with_mock_domain(
        input_data={
            data_source_key: user_selection_value
        }
    )
    choices_node = load_yaml(snippet)[0]
    data_source_node = choices_node.value[0]
    assert data_source_node.render(context) == user_selection_value

    first_choice_node = choices_node.value[1]
    first_for_value_node = first_choice_node.value[TagName.SelectionValue]
    assert first_for_value_node == user_selection_value
    first_body_node = first_choice_node.body
    first_method_node = first_body_node[0]
    assert first_method_node.identity == selected_method_id

    second_choice_node = choices_node.value[2]
    second_for_value_node = second_choice_node.value[TagName.SelectionValue]
    assert second_for_value_node == alternate_user_selection_value
    second_body_node = second_choice_node.body
    second_method_node = second_body_node[0]
    assert second_method_node.identity == alternate_method_id

    results = choices_node.render(context)
    assert results[0]['mock_result'] == f'Mock executor {selected_method_id} run, output_target: None'

    # make alternate selection
    alt_context = get_context_with_mock_domain(
        input_data={
            data_source_key: alternate_user_selection_value
        }
    )
    results = choices_node.render(alt_context)
    assert results[0]['mock_result'] == f'Mock executor {alternate_method_id} run, output_target: None'

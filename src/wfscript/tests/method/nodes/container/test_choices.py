from ....testing_tools.mocks import get_context_with_mocks
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    data_source_key = 'user_selection'
    user_selection_value = 'my choice'
    alternate_user_selection_value = 'my different choice'
    selected_method_id = 'path/to::first_method==1.0'
    alternate_method_id = 'path/to::second_method==1.0'


def test_choices_tag():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.CHOICES}
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
    )

    # Case: Select one choice
    context = get_context_with_mocks(
        input_data={
            TestParam.data_source_key: TestParam.user_selection_value
        }
    )
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert result[0].result == f'Mock-executed method {TestParam.selected_method_id}'

    # Case: Select the other choice
    context = get_context_with_mocks(
        input_data={
            TestParam.data_source_key: TestParam.alternate_user_selection_value
        }
    )
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert result[0].result == f'Mock-executed method {TestParam.alternate_method_id}'

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

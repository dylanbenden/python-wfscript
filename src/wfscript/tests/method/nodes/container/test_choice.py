from ....testing_tools.context import get_empty_context
from ....testing_tools.mocks import get_context_with_mocks
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    method_identity = 'path/to::some_method==production'
    user_selection_value = 'some_selection_name'
    state_target = 'state_target'


def test_choice_tag():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.Choice}
            - {TagName.SelectionValue}
              - {TestParam.user_selection_value}
            - {TagName.BODY}
              - {TagName.Method}
                - {TagName.IDENTITY} {TestParam.method_identity}
            - {TagName.OUTPUT}
              - {TagName.State}
                {TestParam.state_target}: {TagName.Output}            
        '''
    )
    context = get_context_with_mocks()
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert output[0].result == f'Mock-executed method {TestParam.method_identity}'

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    context = get_empty_context()
    assert_unsupported(unsupported, node, context)
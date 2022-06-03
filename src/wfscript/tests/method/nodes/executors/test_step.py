from ....testing_tools.mocks import get_context_with_mocks
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml
from .....runtime.output import StepReturn


class TestParam(ConstantNamespace):
    step_name = 'my_test_step'
    first_method_id = 'path/to::first_method==production'
    second_method_id = 'path/to::second_method==1.0'
    output_target_name = 'name'
    output_target_value = 'some value'


def test_step_tag_output():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.Step}
            - {TagName.name} {TestParam.step_name}
            - {TagName.BODY}
              - {TagName.Method}
                - {TagName.IDENTITY} {TestParam.first_method_id}
              - {TagName.Method}
                - {TagName.IDENTITY} {TestParam.second_method_id}
            - {TagName.OUTPUT}
              {TestParam.output_target_name}: {TestParam.output_target_value}
        '''
    )
    context = get_context_with_mocks(state={})
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert isinstance(output, StepReturn) is True
    assert output.result == {TestParam.output_target_name: TestParam.output_target_value}
    assert context.debug[0].result == f'Mock-executed method {TestParam.first_method_id}'
    assert context.debug[1].result == f'Mock-executed method {TestParam.second_method_id}'

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

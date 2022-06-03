from ....testing_tools.mocks import get_context_with_mocks
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml
from .....runtime.output import MethodReturn


class TestParam(ConstantNamespace):
    identity = 'content_root/executing::greet_user==1.0'
    input_name = 'input_name'
    input_value = 'input_value'
    output_target_name = 'output_name'


def test_method_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.Method}
            - {TagName.IDENTITY} {TestParam.identity}
            - {TagName.INPUT}
              {TestParam.input_name}: {TagName.Input} {TestParam.input_name}
            - {TagName.OUTPUT}
              - {TagName.State}
                {TestParam.output_target_name}: {TagName.Output}
      '''
    )
    context = get_context_with_mocks(input_data={TestParam.input_name: TestParam.input_value})
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert isinstance(output, MethodReturn) is True
    assert output.result == f'Mock-executed method {TestParam.identity}'
    assert context.state.value[TestParam.output_target_name] == f'Mock-executed method {TestParam.identity}'

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

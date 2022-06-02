from ....testing_tools.mocks import get_context_with_mocks
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    identity = 'content_root/executing::greet_user==1.0'
    input_name = 'input_name'
    input_value = 'input_value'
    input_target = 'input_target'


def test_ticket_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.Ticket}
            - {TagName.IDENTITY} {TestParam.identity}
            - {TagName.INPUT}
              {TestParam.input_name}: {TagName.Input} {TestParam.input_target}
        '''
    )
    context = get_context_with_mocks(input_data={TestParam.input_target: TestParam.input_value})
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    # Processing tickets happens at the domain level; this confirms we used the right interface
    assert output.result.startswith(f'Ticket mock-created for {TestParam.identity}') is True
    assert f"with input {{'{TestParam.input_name}': '{TestParam.input_value}'}}" in output.result

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

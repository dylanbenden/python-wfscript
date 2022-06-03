from ....content_root.executing import executing_namespace_root
from ....testing_tools.context import get_execution_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml
from .....runtime.output import ActionReturn


class TestParam(ConstantNamespace):
    identity = 'content_root/executing::hello_world==production'
    name = 'Alia'
    expected_greeting = 'Hello there, Alia!'
    output_target_name = 'some_target'
    input_field_name = 'name'


def test_action_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.Action}
           - {TagName.IDENTITY} {TestParam.identity}
           - {TagName.INPUT}
               {TestParam.input_field_name}: {TestParam.name}
           - {TagName.OUTPUT}
             - {TagName.State}
               {TestParam.output_target_name}: {TagName.Output}
        '''
    )
    context = get_execution_context(identity=TestParam.identity, namespace_root=executing_namespace_root)
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert isinstance(output, ActionReturn) is True
    assert output.result == TestParam.expected_greeting

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

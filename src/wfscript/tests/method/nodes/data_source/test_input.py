from .....constants import ConstantNamespace
from ..constants import TagName
from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....method.loading import load_yaml


class TestParams(ConstantNamespace):
    input_target = 'input_target'
    input_key = 'input_key'
    input_value = 'my input value'


def test_input_node():
    # Phase.EXECUTE, ConfigShape.SCALAR
    node = load_yaml(
        f'''
          {TagName.Input} {TestParams.input_key}
        '''
    )
    context = get_empty_context(input_data={TestParams.input_key: TestParams.input_value})
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParams.input_value

    # Phase.OUTPUT, ConfigShape.SCALAR
    node = load_yaml(
        f'''
          {TagName.Input} {TestParams.input_key}
        '''
    )
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context) == TestParams.input_value

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
    ]
    context = get_empty_context()
    assert_unsupported(unsupported, node, context)

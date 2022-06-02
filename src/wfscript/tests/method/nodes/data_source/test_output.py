from ....testing_tools.nodes import Phase, ConfigShape, assert_unsupported, render_for_phase_and_shape
from .....constants import ConstantNamespace
from .....method.loading import load_yaml
from ..constants import TagName
from ....testing_tools.context import get_empty_context

# NB: Somewhat counter-intuitively, !Output is only rendered during ExecutePhase
# That's because it's the output of the current executor

class TestParam(ConstantNamespace):
    key_name = 'key_name'
    value = 'some value'


def test_output_node():
    # Phase.EXECUTE, ConfigShape.SCALAR
    # Case: no name key, returns entire output of containing executor
    node = load_yaml(
        f'''
          {TagName.Output}
        '''
    )
    context = get_empty_context()
    context.output.update({TestParam.key_name: TestParam.value})
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == {TestParam.key_name:
                                                                                           TestParam.value}

    # Case: name key provided, returns element/attribute/key of output\
    node = load_yaml(
        f'''
          {TagName.Output} {TestParam.key_name}
        '''
    )
    context = get_empty_context()
    context.output.update({TestParam.key_name: TestParam.value})
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParam.value

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

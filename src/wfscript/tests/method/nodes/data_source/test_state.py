from ....testing_tools.nodes import Phase, ConfigShape, render_for_phase_and_shape, assert_unsupported
from .....constants import ConstantNamespace
from .....method.loading import load_yaml
from ..constants import TagName
from ....testing_tools.context import get_empty_context


class TestParam(ConstantNamespace):
    key_name = 'some_key'
    value = 'my value'


def test_state_node():
    # Phase.EXECUTE, ConfigShape.DICT
    # Set one or more runtime values in !State
    node = load_yaml(
        f'''
          {TagName.State}
            {TestParam.key_name}: {TestParam.value}
        '''
    )
    context = get_empty_context()
    render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.DICT, node, context)
    assert context.state[TestParam.key_name] == TestParam.value

    # Phase.EXECUTE, ConfigShape.SCALAR
    # Return data from !State
    node = load_yaml(
        f'''
          {TagName.State} {TestParam.key_name}
        '''
    )
    # using the same context as above, so state is already set
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParam.value

    # Phase.OUTPUT, ConfigShape.SCALAR
    # Return data from !State
    node = load_yaml(
        f'''
          {TagName.State} {TestParam.key_name}
        '''
    )
    # using the same context as above, so state is already set
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context) == TestParam.value

    # Unsupported uses - should raise error
    unsupported = [
        (Phase.EXECUTE, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.LIST),
    ]
    assert_unsupported(unsupported, node, context)



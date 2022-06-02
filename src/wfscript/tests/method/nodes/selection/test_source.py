from ..constants import TagName
from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    input_name_key = 'my_input_name'
    input_value = 'my input value'


def test_selection_source_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.SelectionSource}
            - {TagName.Input} {TestParam.input_name_key}
        '''
    )
    context = get_empty_context(input_data={TestParam.input_name_key: TestParam.input_value})
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context) == TestParam.input_value

    # Unsupported uses - should raise error
    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

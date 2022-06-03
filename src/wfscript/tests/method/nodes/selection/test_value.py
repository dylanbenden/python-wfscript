import pytest

from ..constants import TagName
from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    selection_value = 'my selection value'


def test_selection_value_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.SelectionValue}
            - {TestParam.selection_value}
        '''
    )
    context = get_empty_context()
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context) == TestParam.selection_value

    # Unsupported uses - should raise error
    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

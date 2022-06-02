import pytest

from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants.method import TagName
from .....method.loading import load_yaml


def test_verify_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.Verify}
            - {TagName.State}
              state_item:
                data_type: string
                required: true
            - {TagName.Output}
              output_item_list:
                data_type: array
                member_data_type: string
                min_size: 3
        '''
    )
    context = get_empty_context()

    # missing key
    with pytest.raises(RuntimeError) as excinfo:
        render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert "Required data/payload key(s) missing: {'state_item'}" in str(excinfo)

    # !State passes muster, validation rule not satisfied in !Output
    context = get_empty_context(state={'state_item': 'foo'})
    context.output.update({'output_item_list': ['item/id::123']})
    with pytest.raises(RuntimeError) as excinfo:
        render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert 'Not enough elements provided; Required: 3; Provided: 1' in str(excinfo)

    # Verification successful!
    context = get_empty_context(state={'state_item': 'foo'})
    context.output.update({'output_item_list': ['item/id::123', 'item/id::456', 'item/id::789']})
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context) == 'OK'

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

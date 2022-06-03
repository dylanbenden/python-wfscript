from ..constants import TagName
from ....testing_tools.context import get_empty_context
from ....testing_tools.mocks import ValueAssignableObject, MockMaterial
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.identity import IdentityDelimeter
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    obj_id = 456
    obj_value = 'some value'
    sub_key = 'data_subkey'


def test_item_node():
    # Phase.EXECUTE, ConfigShape.SCALAR
    # Case: no argument provided
    node = load_yaml(
        f'''
          {TagName.Item}
        '''
    )
    context = get_empty_context()
    context.set_item(MockMaterial(TestParam.obj_id))
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
    assert isinstance(output, MockMaterial) is True
    assert output.identity == f'{output.model_identity}{IdentityDelimeter.MATERIAL}{output.pk}'

    # Case: arg path provided
    node = load_yaml(
        f'''
          {TagName.Item} pk
        '''
    )
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
    assert output == TestParam.obj_id

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

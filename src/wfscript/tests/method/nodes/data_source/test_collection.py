from .....constants import ConstantNamespace
from ..constants import TagName
from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....method.loading import load_yaml


class TestParams(ConstantNamespace):
    collection_name = 'my_collection'
    collection_value = [1, 2, 3]


def test_collection_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.Collection}
           - {TagName.Input} {TestParams.collection_name}
        '''
    )
    context = get_empty_context(input_data={TestParams.collection_name: TestParams.collection_value})
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context) == TestParams.collection_value

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

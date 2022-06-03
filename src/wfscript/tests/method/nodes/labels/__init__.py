from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    value = 'some value'


def run_label_node_tests(tag_name):
    # Phase.EXECUTE, ConfigShape.SCALAR
    snippet = f'''
    - {tag_name} {TestParam.value}
    '''
    node = load_yaml(snippet)[0]
    context = get_empty_context()
    assert node.tag == tag_name
    assert node.value == TestParam.value
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParam.value

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)
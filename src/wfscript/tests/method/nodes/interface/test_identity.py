from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    namespace = 'tests/loading'
    name = 'test_loader'
    version = '1.0'
    status = 'testing'


def test_identity_binding_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
        {TagName.IDENTITY}
          - {TagName.namespace} {TestParam.namespace}
          - {TagName.name} {TestParam.name}
          - {TagName.version} {TestParam.version}
          - {TagName.status} {TestParam.status}
        '''
    )
    context = get_empty_context()
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert result == {
        TagName.namespace: TestParam.namespace,
        TagName.name: TestParam.name,
        TagName.version: TestParam.version,
        TagName.status: TestParam.status
    }

    # Phase.EXECUTE, ConfigShape.SCALAR
    # Case: identity uses numeric version
    node = load_yaml(
        f'''
          {TagName.IDENTITY} {TestParam.namespace}::{TestParam.name}=={TestParam.version}
        '''
    )
    context = get_empty_context()
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
    assert result == f'{TestParam.namespace}::{TestParam.name}=={TestParam.version}'

    # Case: identity uses semantic status
    node = load_yaml(
        f'''
          {TagName.IDENTITY} {TestParam.namespace}::{TestParam.name}=={TestParam.status}
        '''
    )
    context = get_empty_context()
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
    assert result == f'{TestParam.namespace}::{TestParam.name}=={TestParam.status}'

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)



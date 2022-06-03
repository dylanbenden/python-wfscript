from ....testing_tools.context import get_empty_context
from ....testing_tools.mocks import ValueAssignableObject, MockMaterial
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape
from .....constants import ConstantNamespace
from .....constants.identity import IdentityDelimeter
from .....constants.method import TagName
from .....method.loading import load_yaml


class TestParams(ConstantNamespace):
    key_name = 'my_key_name'
    sub_key_name = 'foo'
    inner_value = 'bar'
    value_as_obj = ValueAssignableObject(**{sub_key_name: inner_value})
    value_as_list = [value_as_obj]
    index_position = 0


def test_dotted_notation():
    # obtain attribute value from object
    node = load_yaml(
        f'''
          {TagName.State} {TestParams.key_name}.foo
        '''
    )
    context = get_empty_context(state={TestParams.key_name: TestParams.value_as_obj})
    # Phase.EXECUTE, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParams.inner_value
    # Phase.OUTPUT, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context) == TestParams.inner_value

    # obtain item from list
    node = load_yaml(
        f'''
          {TagName.State} {TestParams.key_name}.{TestParams.index_position}
        '''
    )
    context = get_empty_context(state={TestParams.key_name: TestParams.value_as_list})
    # Phase.EXECUTE, ConfigShape.SCALAR
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
    assert isinstance(result, ValueAssignableObject)
    assert getattr(result, TestParams.sub_key_name) == TestParams.inner_value
    # Phase.OUTPUT, ConfigShape.SCALAR
    result = render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context)
    assert isinstance(result, ValueAssignableObject)
    assert getattr(result, TestParams.sub_key_name) == TestParams.inner_value

    # obtain attribute from item in list
    node = load_yaml(
        f'''
          {TagName.State} {TestParams.key_name}.{TestParams.index_position}.{TestParams.sub_key_name}
        '''
    )
    context = get_empty_context(state={TestParams.key_name: TestParams.value_as_list})
    # Phase.EXECUTE, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParams.inner_value
    # Phase.OUTPUT, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context) == TestParams.inner_value

    # obtain item from dict
    node = load_yaml(
        f'''
          {TagName.State} {TestParams.key_name}.{TestParams.sub_key_name}
        '''
    )
    context = get_empty_context(state={TestParams.key_name: TestParams.value_as_obj})
    # Phase.EXECUTE, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParams.inner_value
    # Phase.OUTPUT, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context) == TestParams.inner_value

    # obtain attribute from item in list in dict in dict ;)
    inner_key_one = 'key1'
    inner_key_two = 'key2'
    attr_path = f'{TestParams.key_name}.{inner_key_one}.{inner_key_two}.{TestParams.index_position}.' \
                f'{TestParams.sub_key_name}'
    node = load_yaml(
        f'''
          {TagName.State} {attr_path}
        '''
    )
    context = get_empty_context(state={TestParams.key_name: {inner_key_one: {inner_key_two: TestParams.value_as_list}}})
    # Phase.EXECUTE, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context) == TestParams.inner_value
    # Phase.OUTPUT, ConfigShape.SCALAR
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context) == TestParams.inner_value

    # OutputPhase and ExecutePhase primarily differ in how materials are returned
    object_pk = 123
    obj = MockMaterial(object_pk)
    assert obj.identity == f'{MockMaterial.model_identity}{IdentityDelimeter.MATERIAL}{object_pk}'
    node = load_yaml(
        f'''
          {TagName.Material} {TestParams.key_name}
        '''
    )
    context = get_empty_context(state={TestParams.key_name: obj})
    # Phase.EXECUTE, ConfigShape.SCALAR
    # returns object
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
    assert isinstance(result, MockMaterial) is True
    assert result.identity == obj.identity
    # Phase.OUTPUT, ConfigShape.SCALAR
    # returns object identity
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context) == obj.identity

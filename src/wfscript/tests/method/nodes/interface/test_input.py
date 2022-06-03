import pytest

from ....testing_tools.context import get_empty_context
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....constants.validation import DataType
from .....method.loading import load_yaml


class TestParam(ConstantNamespace):
    first_key_name = 'my_first_key'
    second_key_name = 'my_second_key'
    input_key = 'input_key'
    input_value = 'input value'


def test_input_binding_node_as_validator():
    # When used at the top-level of a document or !Step, !INPUT provides a data input specification
    # Prior to executing the related container, validate_input is called against this specification
    node = load_yaml(
        f'''
          {TagName.INPUT}
            {TestParam.first_key_name}:
              data_type: {DataType.STRING}
              required: true
            {TestParam.second_key_name}:
              data_type: {DataType.ARRAY}
              required: false
        '''
    )
    context = get_empty_context(input_data={TestParam.second_key_name: [1, 2, 3]})

    # invalid input raises an exception
    with pytest.raises(RuntimeError) as excinfo:
        node.validate_input(context)
    assert 'Required data/payload key(s) missing' in str(excinfo)

    # with valid input, we just get back 'OK'
    context = get_empty_context(input_data={TestParam.first_key_name: 'hello', TestParam.second_key_name: [1, 2, 3]})
    assert node.validate_input(context) == 'OK'


def test_input_binding_node_as_executor_input():
    # Phase.EXECUTE, ConfigShape.DICT
    node = load_yaml(
        f'''
          {TagName.INPUT}
            {TestParam.input_key}: {TagName.State} {TestParam.input_key}
        '''
    )
    context = get_empty_context(state={TestParam.input_key: TestParam.input_value})
    result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.DICT, node, context)
    assert result == {TestParam.input_key: TestParam.input_value}


def test_unsupported():
    unsupported = [
        (Phase.EXECUTE, ConfigShape.LIST),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    node = load_yaml(f'{TagName.INPUT}')
    context = get_empty_context()
    assert_unsupported(unsupported, node, context)

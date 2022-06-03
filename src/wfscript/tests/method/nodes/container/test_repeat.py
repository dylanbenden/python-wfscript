from ....testing_tools.mocks import get_context_with_mocks
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml
from .....runtime.output import MethodReturn


class TestParam(ConstantNamespace):
    method_identity = 'path/to::some_method==production'
    item_list_name = 'my_list_of_stuff'
    first_list_item = 'abc'
    second_list_item = '123'
    item_list_value = [first_list_item, second_list_item]


def test_repeat_node():
    # Phase.EXECUTE, ConfigShape.LIST
    node = load_yaml(
        f'''
          {TagName.REPEAT}
           - {TagName.Collection}
             - {TagName.Input} {TestParam.item_list_name}
           - {TagName.BODY}
             - {TagName.Method}
               - {TagName.IDENTITY} {TestParam.method_identity}
               - {TagName.INPUT}
                 collected_ids: {TagName.Item}
             # TODO: we need some kind of "append to data_source" noce
             # - {TagName.OUTPUT}
             #   {TagName.State}
        '''
    )
    context = get_context_with_mocks(
        input_data={TestParam.item_list_name: TestParam.item_list_value}
    )
    output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    first_method_output = output[0][0]
    second_method_output = output[1][0]
    assert isinstance(first_method_output, MethodReturn)
    assert first_method_output.result == f'Mock-executed method {TestParam.method_identity}'
    assert isinstance(second_method_output, MethodReturn)
    assert second_method_output.result == f'Mock-executed method {TestParam.method_identity}'

    # todo
    # we will want to bind the outputs of a repeat by appending loop results to an array-shaped object

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, node, context)

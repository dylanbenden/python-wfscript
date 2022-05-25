from ....testing_tools.context import get_empty_context
from ....testing_tools.mocks import ValueAssignableObject
from .....constants.method import TagName
from .....method.document_loader import load_method


def test_dotted_notation():
    key_name = 'my_key_name'
    sub_key_name = 'foo'
    inner_value = 'bar'
    value_as_obj = ValueAssignableObject(**{sub_key_name: inner_value})

    # obtain attribute value from object
    snippet = f'''
    - !State {key_name}.foo
    '''
    result = load_method(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: value_as_obj})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{sub_key_name}'
    assert state_node.render(empty_context) == inner_value

    # obtain item from list
    value_as_list = [value_as_obj]
    index_position = 0
    snippet = f'''
    - !State {key_name}.{index_position}
    '''
    result = load_method(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: value_as_list})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{index_position}'
    rendered_result = state_node.render(empty_context)
    assert isinstance(rendered_result, ValueAssignableObject) is True
    assert getattr(rendered_result, sub_key_name) == inner_value

    # obtain attribute from item in list
    snippet = f'''
    - !State {key_name}.{index_position}.{sub_key_name}
    '''
    result = load_method(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: value_as_list})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{index_position}.{sub_key_name}'
    assert state_node.render(empty_context) == inner_value

    # obtain item from dict
    snippet = f'''
    - !State {key_name}.{sub_key_name}
    '''
    result = load_method(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: value_as_obj})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{sub_key_name}'
    assert state_node.render(empty_context) == inner_value

    # obtain attribute from item in list in dict in dict ;)
    inner_key_one = 'key1'
    inner_key_two = 'key2'
    snippet = f'''
    - !State {key_name}.{inner_key_one}.{inner_key_two}.{index_position}.{sub_key_name}
    '''
    result = load_method(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: {inner_key_one: {inner_key_two: value_as_list}}})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{inner_key_one}.{inner_key_two}.{index_position}.{sub_key_name}'
    assert state_node.render(empty_context) == inner_value

from ....constants.method import TagName
from ....method.document_loader import load_yaml_document
from ....testing.context import get_empty_context


class BogusObject(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_state_tag():
    key_name = 'my_key'
    value = 'some value'
    snippet = f'''
    - !State {key_name}
    '''
    result = load_yaml_document(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: value})
    assert state_node.tag == TagName.State
    assert state_node.value == key_name
    assert state_node.render(empty_context) == value


def test_input_tag():
    key_name = 'my_key'
    value = 'some value'
    snippet = f'''
    - !Input {key_name}
    '''
    result = load_yaml_document(snippet)
    input_node = result[TagName.Input]
    empty_context = get_empty_context(input_data={key_name: value})
    assert input_node.tag == TagName.Input
    assert input_node.value == key_name
    assert input_node.render(empty_context) == value


def test_dotted_notation():
    key_name = 'my_key_name'
    sub_key_name = 'foo'
    inner_value = 'bar'
    value_as_obj = BogusObject(**{sub_key_name: inner_value})

    # obtain attribute value from object
    snippet = f'''
    - !State {key_name}.foo
    '''
    result = load_yaml_document(snippet)
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
    result = load_yaml_document(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: value_as_list})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{index_position}'
    rendered_result = state_node.render(empty_context)
    assert isinstance(rendered_result, BogusObject) is True
    assert getattr(rendered_result, sub_key_name) == inner_value

    # obtain attribute from item in list
    snippet = f'''
    - !State {key_name}.{index_position}.{sub_key_name}
    '''
    result = load_yaml_document(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: value_as_list})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{index_position}.{sub_key_name}'
    assert state_node.render(empty_context) == inner_value

    # obtain item from dict
    snippet = f'''
    - !State {key_name}.{sub_key_name}
    '''
    result = load_yaml_document(snippet)
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
    result = load_yaml_document(snippet)
    state_node = result[TagName.State]
    empty_context = get_empty_context(state={key_name: {inner_key_one: {inner_key_two: value_as_list}}})
    assert state_node.tag == TagName.State
    assert state_node.value == f'{key_name}.{inner_key_one}.{inner_key_two}.{index_position}.{sub_key_name}'
    assert state_node.render(empty_context) == inner_value


def test_locking():
    initial_data = {'foo': 'bar'}
    snippet = f'''
    - !Input foo
    '''
    empty_context = get_empty_context(input_data=initial_data)
    result = load_yaml_document(snippet)
    input_node = result[TagName.Input]
    assert input_node.render(empty_context)

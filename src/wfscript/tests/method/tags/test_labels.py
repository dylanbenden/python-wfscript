from ...testing_tools.context import get_empty_context
from ....constants.method import TagName
from ....method.document_loader import load_method


def test_name_tag():
    value = 'some_name'
    snippet = f'''
    - {TagName.name} {value}
    '''
    result = load_method(snippet)
    name_node = result[TagName.name]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.name
    assert name_node.value == value
    assert name_node.render(empty_context) == value


def test_namespace_tag():
    value = 'some_namespace'
    document = f'''
    - {TagName.namespace} {value}
    '''
    result = load_method(document)
    name_node = result[TagName.namespace]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.namespace
    assert name_node.value == value
    assert name_node.render(empty_context) == value


def test_version_tag():
    value = 'some_version'
    document = f'''
    - {TagName.version} {value}
    '''
    result = load_method(document)
    name_node = result[TagName.version]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.version
    assert name_node.value == value
    assert name_node.render(empty_context) == value


def test_status_tag():
    value = 'some_status'
    document = f'''
    - {TagName.status} {value}
    '''
    result = load_method(document)
    name_node = result[TagName.status]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.status
    assert name_node.value == value
    assert name_node.render(empty_context) == value

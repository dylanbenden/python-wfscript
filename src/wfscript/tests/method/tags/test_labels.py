from ....constants.method import TagName
from ....method.document_loader import load_yaml_document
from ....testing import get_empty_context


def test_name_tag():
    value = 'some_name'
    snippet = f'''
    - !NAME {value}
    '''
    result = load_yaml_document(snippet)
    name_node = result[TagName.NAME]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.NAME
    assert name_node.value == value
    assert name_node.render(empty_context) == value


def test_namespace_tag():
    value = 'some_namespace'
    document = f'''
    - !NAMESPACE {value}
    '''
    result = load_yaml_document(document)
    name_node = result[TagName.NAMESPACE]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.NAMESPACE
    assert name_node.value == value
    assert name_node.render(empty_context) == value


def test_version_tag():
    value = 'some_version'
    document = f'''
    - !VERSION {value}
    '''
    result = load_yaml_document(document)
    name_node = result[TagName.VERSION]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.VERSION
    assert name_node.value == value
    assert name_node.render(empty_context) == value


def test_status_tag():
    value = 'some_status'
    document = f'''
    - !STATUS {value}
    '''
    result = load_yaml_document(document)
    name_node = result[TagName.STATUS]
    empty_context = get_empty_context()
    assert name_node.tag == TagName.STATUS
    assert name_node.value == value
    assert name_node.render(empty_context) == value

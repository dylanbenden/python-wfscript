from .....constants.method import TagName
from .....method.document_loader import load_method


def test_identity_tag():
    snippet = '''
    - !IDENTITY
      - !namespace tests/loading
      - !name test_loader
      - !version 1.0
      - !status testing
    '''
    result = load_method(snippet)
    id_node = result[TagName.IDENTITY]
    assert id_node.tag == TagName.IDENTITY
    assert id_node.value == {
        TagName.namespace: 'tests/loading',
        TagName.name: 'test_loader',
        TagName.version: '1.0',
        TagName.status: 'testing'
    }

    alternate_syntax_versioned = '''
- !IDENTITY tests/loading::test_loader==1.0
'''
    result = load_method(alternate_syntax_versioned)
    id_node = result[TagName.IDENTITY]
    assert id_node.tag == TagName.IDENTITY
    assert id_node.value == {
        TagName.namespace: 'tests/loading',
        TagName.name: 'test_loader',
        TagName.version: '1.0'
    }

    alternate_syntax_status = '''
- !IDENTITY tests/loading::test_loader==testing
'''
    result = load_method(alternate_syntax_status)
    id_node = result[TagName.IDENTITY]
    assert id_node.tag == TagName.IDENTITY
    assert id_node.value == {
        TagName.namespace: 'tests/loading',
        TagName.name: 'test_loader',
        TagName.status: 'testing'
    }


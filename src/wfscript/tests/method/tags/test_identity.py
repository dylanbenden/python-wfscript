from ....constants.method import TagName
from ....method.document_loader import load_yaml_document


def test_identity_tag():
    document = '''
    - !ID
      - !NAMESPACE tests/loading
      - !NAME test_loader
      - !VERSION 1.0
      - !STATUS testing
    '''
    result = load_yaml_document(document)
    id_node = result[TagName.ID]
    assert id_node.tag == TagName.ID
    assert id_node.value == {
        TagName.NAMESPACE: 'tests/loading',
        TagName.NAME: 'test_loader',
        TagName.VERSION: '1.0',
        TagName.STATUS: 'testing'
    }

    alternate_syntax_versioned = '''
- !ID tests/loading::test_loader==1.0
'''
    result = load_yaml_document(alternate_syntax_versioned)
    id_node = result[TagName.ID]
    assert id_node.tag == TagName.ID
    assert id_node.value == {
        TagName.NAMESPACE: 'tests/loading',
        TagName.NAME: 'test_loader',
        TagName.VERSION: '1.0'
    }

    alternate_syntax_status = '''
- !ID tests/loading::test_loader==testing
'''
    result = load_yaml_document(alternate_syntax_status)
    id_node = result[TagName.ID]
    assert id_node.tag == TagName.ID
    assert id_node.value == {
        TagName.NAMESPACE: 'tests/loading',
        TagName.NAME: 'test_loader',
        TagName.STATUS: 'testing'
    }


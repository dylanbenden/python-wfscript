from ...constants.loading import TagName, MetaSectionKey
from ...loading.loader import load_yaml_document


def test_load_yaml_document():
    document = '''
- !META
  namespace: tests/loading
  name: test_loader
  version: 1.0
  status: testing
'''
    result = load_yaml_document(document)
    meta_node = result[TagName.META]
    assert meta_node.tag == TagName.META
    assert meta_node.value == {
        MetaSectionKey.NAMESPACE: 'tests/loading',
        MetaSectionKey.NAME: 'test_loader',
        MetaSectionKey.VERSION: 1.0,
        MetaSectionKey.STATUS: 'testing'
    }

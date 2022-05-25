from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.document_loader import load_method


class TestParam(ConstantNamespace):
    namespace = 'tests/loading'
    name = 'test_loader'
    version = '1.0'
    status = 'testing'



def test_identity_tag():
    snippet = f'''
    - {TagName.IDENTITY}
      - {TagName.namespace} {TestParam.namespace}
      - {TagName.name} {TestParam.name}
      - {TagName.version} {TestParam.version}
      - {TagName.status} {TestParam.status}
    '''
    result = load_method(snippet)
    id_node = result[TagName.IDENTITY]
    assert id_node.tag == TagName.IDENTITY
    assert id_node.value == {
        TagName.namespace: TestParam.namespace,
        TagName.name: TestParam.name,
        TagName.version: TestParam.version,
        TagName.status: TestParam.status
    }

    alternate_syntax_versioned = f'''
- {TagName.IDENTITY} {TestParam.namespace}::{TestParam.name}=={TestParam.version}
'''
    result = load_method(alternate_syntax_versioned)
    id_node = result[TagName.IDENTITY]
    assert id_node.tag == TagName.IDENTITY
    assert id_node.value == {
        TagName.namespace: TestParam.namespace,
        TagName.name: TestParam.name,
        TagName.version: TestParam.version
    }

    alternate_syntax_status = f'''
- {TagName.IDENTITY} {TestParam.namespace}::{TestParam.name}=={TestParam.status}
'''
    result = load_method(alternate_syntax_status)
    id_node = result[TagName.IDENTITY]
    assert id_node.tag == TagName.IDENTITY
    assert id_node.value == {
        TagName.namespace: TestParam.namespace,
        TagName.name: TestParam.name,
        TagName.status: TestParam.status
    }


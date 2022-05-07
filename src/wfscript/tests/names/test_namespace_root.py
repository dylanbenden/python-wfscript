from ..content_root import testing_namespace_root, content_root_path
from ...constants.loading import TagName


def test_properties():
    assert testing_namespace_root.identity == 'wfscript.tests.content_root'
    assert testing_namespace_root.path == content_root_path
    assert testing_namespace_root.actions == list()
    assert testing_namespace_root.contained_namespaces == list()
    assert testing_namespace_root.methods == dict()


def test_load_methods():
    assert testing_namespace_root.methods == dict()
    testing_namespace_root.load_methods()
    v1_identity = 'content_root/loading::versioned_method==1.0'
    v1_1_identity = 'content_root/loading::versioned_method==1.1'
    expected = [
        v1_identity,
        v1_1_identity
    ]
    assert list(testing_namespace_root.methods.keys()) == expected

    v1_expected_meta = {
        'name': 'versioned_method',
        'namespace': 'content_root/loading',
        'status': 'testing',
        'version': 1.0
    }
    v1_1_expected_meta = {
        'name': 'versioned_method',
        'namespace': 'content_root/loading',
        'status': 'testing',
        'version': 1.1
    }
    assert testing_namespace_root.methods[v1_identity][TagName.META].value == v1_expected_meta
    assert testing_namespace_root.methods[v1_1_identity][TagName.META].value == v1_1_expected_meta

from ..content_root import testing_namespace_root, content_root_path
from ...constants.loading import TagName, MetaStatusChoice


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
    v1_2_identity = 'content_root/loading::versioned_method==1.2'
    prod_identity = 'content_root/loading::versioned_method==production'
    test_identity = 'content_root/loading::versioned_method==testing'
    unversioned_identity = 'content_root/loading::versioned_method'
    expected = [
        unversioned_identity,
        v1_identity,
        v1_1_identity,
        v1_2_identity,
        prod_identity,
        test_identity
    ]
    assert sorted(list(testing_namespace_root.methods.keys())) == sorted(expected)

    v1_expected_meta = {
        'name': 'versioned_method',
        'namespace': 'content_root/loading',
        'status': MetaStatusChoice.PRODUCTION,
        'version': 1.0
    }
    v1_1_expected_meta = {
        'name': 'versioned_method',
        'namespace': 'content_root/loading',
        'status': MetaStatusChoice.PRODUCTION,
        'version': 1.1
    }
    v1_2_expected_meta = {
        'name': 'versioned_method',
        'namespace': 'content_root/loading',
        'status': MetaStatusChoice.TESTING,
        'version': 1.2
    }
    prod_expected_meta = v1_1_expected_meta
    test_expected_meta = v1_2_expected_meta
    unversioned_expected_meta = prod_expected_meta
    assert testing_namespace_root.methods[v1_identity][TagName.META].value == v1_expected_meta
    assert testing_namespace_root.methods[v1_1_identity][TagName.META].value == v1_1_expected_meta
    assert testing_namespace_root.methods[v1_2_identity][TagName.META].value == v1_2_expected_meta
    assert testing_namespace_root.methods[prod_identity][TagName.META].value == prod_expected_meta
    assert testing_namespace_root.methods[test_identity][TagName.META].value == test_expected_meta
    assert testing_namespace_root.methods[unversioned_identity][TagName.META].value == unversioned_expected_meta

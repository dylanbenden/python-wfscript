from ..content_root_loading import loading_namespace_root, content_root_path
from ...constants.loading import TagName, MetaStatusChoice


def test_properties():
    assert loading_namespace_root.identity == 'wfscript.tests.content_root_loading'
    assert loading_namespace_root.path == content_root_path
    assert loading_namespace_root.contained_namespaces == list()
    assert loading_namespace_root.yaml_documents == dict()
    assert loading_namespace_root.actions == dict()


def test_load_methods():
    assert loading_namespace_root.yaml_documents == dict()
    loading_namespace_root.load_yaml_documents()
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
    assert sorted(list(loading_namespace_root.yaml_documents.keys())) == sorted(expected)

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
    assert loading_namespace_root.yaml_documents[v1_identity][TagName.META].value == v1_expected_meta
    assert loading_namespace_root.yaml_documents[v1_1_identity][TagName.META].value == v1_1_expected_meta
    assert loading_namespace_root.yaml_documents[v1_2_identity][TagName.META].value == v1_2_expected_meta
    assert loading_namespace_root.yaml_documents[prod_identity][TagName.META].value == prod_expected_meta
    assert loading_namespace_root.yaml_documents[test_identity][TagName.META].value == test_expected_meta
    assert loading_namespace_root.yaml_documents[unversioned_identity][TagName.META].value == unversioned_expected_meta


def test_load_actions():
    assert loading_namespace_root.actions == dict()
    loading_namespace_root.load_actions()
    v1_identity = 'content_root/loading::hello_world==1.0'
    v2_identity = 'content_root/loading::hello_world==2.0'
    v2_1_identity = 'content_root/loading::hello_world==2.1'
    prod_identity = 'content_root/loading::hello_world==production'
    test_identity = 'content_root/loading::hello_world==testing'
    unversioned_identity = 'content_root/loading::hello_world'
    expected = [
        unversioned_identity,
        v1_identity,
        v2_identity,
        v2_1_identity,
        prod_identity,
        test_identity
    ]
    assert sorted(list(loading_namespace_root.actions.keys())) == sorted(expected)

    name = 'Alia'
    v1_expected = 'Hello there, you beautiful person!'
    v2_no_name_expected = 'Hello there, you beautiful person!'
    v2_with_name_expected = f'Hello there, Alia!'
    v2_1_no_name_expected = f'{v2_no_name_expected} Shall we play a game?'
    v2_1_with_name_expected = f'{v2_with_name_expected} Shall we play a game?'
    prod_name_expected = v2_with_name_expected
    unversioned_name_expected = prod_name_expected
    test_name_expected = v2_1_with_name_expected
    assert loading_namespace_root.actions[unversioned_identity](name) == unversioned_name_expected
    assert loading_namespace_root.actions[v1_identity]() == v1_expected
    assert loading_namespace_root.actions[v2_identity]() == v2_no_name_expected
    assert loading_namespace_root.actions[v2_identity](name) == v2_with_name_expected
    assert loading_namespace_root.actions[v2_1_identity]() == v2_1_no_name_expected
    assert loading_namespace_root.actions[v2_1_identity](name) == v2_1_with_name_expected
    assert loading_namespace_root.actions[prod_identity](name) == prod_name_expected
    assert loading_namespace_root.actions[test_identity](name) == test_name_expected

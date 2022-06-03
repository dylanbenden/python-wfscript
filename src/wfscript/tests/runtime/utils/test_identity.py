from ....constants.method import TagName, MetaStatusChoice
from ....runtime.utils.identity import deconstruct_identity, construct_identity


def test_deconstruct_identity():
    versioned_identity = 'domain/name::method_name==1.0'
    meta_values = {
        TagName.namespace: 'domain/name',
        TagName.name: 'method_name',
        TagName.version: '1.0'
    }
    assert deconstruct_identity(versioned_identity) == meta_values
    assert construct_identity(deconstruct_identity(versioned_identity)) == versioned_identity

    semantic_identity = f'domain/name::method_name=={MetaStatusChoice.PRODUCTION}'
    meta_values = {
        TagName.namespace: 'domain/name',
        TagName.name: 'method_name',
        TagName.status: MetaStatusChoice.PRODUCTION
    }
    assert deconstruct_identity(semantic_identity) == meta_values
    assert construct_identity(deconstruct_identity(semantic_identity)) == semantic_identity


def test_construct_identity():
    versioned_identity = 'domain/name::method_name==1.0'
    meta_values = {
        TagName.namespace: 'domain/name',
        TagName.name: 'method_name',
        TagName.version: '1.0'
    }
    assert construct_identity(meta_values) == versioned_identity
    assert deconstruct_identity(construct_identity(meta_values)) == meta_values

    semantic_identity = f'domain/name::method_name=={MetaStatusChoice.PRODUCTION}'
    meta_values = {
        TagName.namespace: 'domain/name',
        TagName.name: 'method_name',
        TagName.status: MetaStatusChoice.PRODUCTION
    }
    assert construct_identity(meta_values) == semantic_identity
    assert deconstruct_identity(construct_identity(meta_values)) == meta_values

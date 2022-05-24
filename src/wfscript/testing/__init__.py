from ..constants.payload import PayloadKey
from ..runtime.context import RunContext, get_context
from ..runtime.data import Input


def get_empty_context(input_data=None, state=None, namespace_root=None):
    return RunContext(
        state=state,
        namespace_root=namespace_root,
        request={
            PayloadKey.INPUT: Input(input_data or dict()),
            PayloadKey.METHOD: 'bogus/namespace::bogus_method==production'
        },
        skip_validation=True)


def get_test_execution_context(identity, namespace_root, **kwargs):
    return get_context(identity, namespace_root, skip_validation=True, **kwargs)
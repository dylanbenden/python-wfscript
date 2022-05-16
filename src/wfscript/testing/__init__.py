from ..constants.payload import PayloadKey
from ..runtime.context import RunContext


def get_test_context(namespace_root, method_identity):
    return RunContext(
        namespace_root=namespace_root,
        request={PayloadKey.METHOD: method_identity},
        skip_validation=True)

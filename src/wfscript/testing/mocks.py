from ..constants.payload import PayloadKey
from ..runtime.context import RunContext
from ..runtime.data import Input


class MockIdentifiedObject(object):
    def __init__(self, identity):
        self.identity = identity
        self.value = identity


class MockDomain(object):
    def load_material(self, identity):
        return MockIdentifiedObject(identity)

    def load_materials(self, values):
        return [MockIdentifiedObject(v) for v in values]


class MockNamespaceRoot(object):
    domain = MockDomain()


def get_context_with_mock_domain(input_data=None, state=None):
    return RunContext(
        state=state,
        namespace_root=MockNamespaceRoot(),
        request={
            PayloadKey.INPUT: Input(input_data or dict()),
            PayloadKey.METHOD: 'bogus/namespace::bogus_method==production'
        }
    )

from ...constants.payload import PayloadKey
from ...runtime.context import RunContext
from ...runtime.data import Input
from ...runtime.output import MethodReturn


class ValueAssignableObject(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockIdentifiedObject(object):
    def __init__(self, identity):
        self.identity = identity
        self.value = identity


class MockDomain(object):
    def load_material(self, identity):
        return MockIdentifiedObject(identity)

    def load_materials(self, values):
        return [MockIdentifiedObject(v) for v in values]


class MockMethodExecutor(object):
    def __init__(self, identity):
        self.identity = identity

    def run_from_tag(self, context, output_target):
        return MethodReturn(
            result=f'Mock-executed {self.identity}',
            context=context
        )


class MockNamespaceRoot(object):
    domain = MockDomain()
    retrieved_methods = list()
    executed_methods = list()

    def get_method(self, identity):
        self.retrieved_methods.append(identity)
        return MockMethodExecutor(identity)


def get_context_with_mocks(input_data=None, state=None):
    return RunContext(
        state=state,
        namespace_root=MockNamespaceRoot(),
        request={
            PayloadKey.INPUT: Input(input_data or dict()),
            PayloadKey.METHOD: 'bogus/namespace::bogus_method==production'
        }
    )

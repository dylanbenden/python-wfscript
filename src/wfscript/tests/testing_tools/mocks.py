from ...constants.payload import PayloadKey
from ...runtime.context import RunContext
from ...runtime.data import Input
from ...runtime.materials import WorkflowMaterial
from ...runtime.output import MethodReturn, TicketReturn


class ValueAssignableObject(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockIdentifiedObject(WorkflowMaterial):
    def __init__(self, identity):
        self.mock_identity = identity
        self.value = identity

    @property
    def identity(self):
        return self.mock_identity


class MockDomain(object):
    def load_material(self, identity):
        return MockIdentifiedObject(identity)

    def load_materials(self, identities):
        return [MockIdentifiedObject(identity) for identity in identities]

    def add_ticket(self, identity, input_data):
        return TicketReturn(f'Ticket mock-created for {identity} with input {input_data}')


class MockExecutor(object):
    def __init__(self, identity):
        self.identity = identity


class MockMethodExecutor(MockExecutor):
    def execute(self, context):
        return MethodReturn(
            result=f'Mock-executed method {self.identity}'
        )


class MockActionExecutor(MockMethodExecutor):
    def __call__(self, *args, **kwargs):
        return f'Mock-executed action {self.identity}'


class MockNamespaceRoot(object):
    domain = MockDomain()
    retrieved_methods = list()
    executed_methods = list()

    def get_method(self, identity):
        self.retrieved_methods.append(identity)
        return MockMethodExecutor(identity)

    def get_action(self, identity):
        self.executed_methods.append(identity)
        return MockActionExecutor(identity)


def get_context_with_mocks(input_data=None, state=None, resume_info=None, method=None):
    return RunContext(
        state=state,
        namespace_root=MockNamespaceRoot(),
        request={
            PayloadKey.INPUT: Input(input_data or dict()),
            PayloadKey.METHOD: method or 'bogus/namespace::bogus_method==production'
        },
        resume_info=resume_info
    )

import pytest

from ..content_root.onboarding import onboarding_namespace_root
from ...constants.payload import PayloadKey
from ...runtime.context import RunContext
from ...runtime.data import BaseRuntimeData


def test_context_properties():
    method_identity = 'onboarding/hr::add_person==1.0'
    data_provided = BaseRuntimeData({
        'first_name': 'Kira',
        'last_name': 'Nerys'
    })
    # RunContext will only initialize if it validates, try first with valid data
    context = RunContext(
        namespace_root=onboarding_namespace_root,
        request={
            PayloadKey.METHOD: method_identity,
            PayloadKey.INPUT: data_provided
        }
    )
    assert context.method == method_identity
    assert context.input == data_provided
    assert context.state.value == dict()

    # Fail cases, just to show validation is wired up
    missing_input = BaseRuntimeData({
        'first_name': 'Q'
    })
    with pytest.raises(RuntimeError) as excinfo:
        RunContext(
            namespace_root=onboarding_namespace_root,
            request={
                PayloadKey.METHOD: method_identity,
                PayloadKey.INPUT: missing_input
            }
        )
    assert 'Required data/payload key(s) missing' in str(excinfo.value)

    unexpected_input = BaseRuntimeData({
        'first_name': 'Seven',
        'last_name': 'of Nine',
        'designation': 'Seven of Nine, tertiary adjunct to Unimatrix Zero'
    })
    with pytest.raises(RuntimeError) as excinfo:
        RunContext(
            namespace_root=onboarding_namespace_root,
            request={
                PayloadKey.METHOD: method_identity,
                PayloadKey.INPUT: unexpected_input
            }
        )
    assert 'Unexpected data/payload key(s) provided' in str(excinfo.value)


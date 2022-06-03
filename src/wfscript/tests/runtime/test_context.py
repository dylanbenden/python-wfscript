from ...constants import ConstantNamespace
from ...runtime.context import RunContext


class TestParams(ConstantNamespace):
    item_key = 'item_key'
    item_value = 'item value'
    output_key = 'output_key'
    output_value = 'output value'

def test_context_settable_data():
    context = RunContext()

    assert context.output.value == {}
    context.set_output({TestParams.output_key: TestParams.output_value})
    assert context.output.value == {TestParams.output_key: TestParams.output_value}

    assert context.item.value == {}
    context.set_item({TestParams.item_key: TestParams.item_value})
    assert context.item.value == {TestParams.item_key: TestParams.item_value}


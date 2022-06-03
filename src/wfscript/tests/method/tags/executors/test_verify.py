import pytest

from ....testing_tools.context import get_empty_context
from .....constants.method import TagName
from .....method.document_loader import load_yaml


def test_verify_tag():
    snippet = f'''
        - {TagName.Verify}
          - {TagName.State}
            state_item:
              data_type: string
              required: true
          - {TagName.Output}
            output_item_list:
              data_type: array
              member_data_type: string
              min_size: 3
    '''
    node = load_yaml(snippet)[0]
    assert node.value == {
        TagName.State:
            {'state_item': {'data_type': 'string', 'required': True}},
        TagName.Output:
            {'output_item_list': {'data_type': 'array', 'member_data_type': 'string', 'min_size': 3}}
    }

    # missing key
    context = get_empty_context()
    with pytest.raises(RuntimeError) as excinfo:
        node.render(context)
    assert "Required data/payload key(s) missing: {'state_item'}" in str(excinfo)

    # !State passes muster, validation rule not satisfied in !Output
    context = get_empty_context(state={'state_item': 'foo'})
    context.output.update({'output_item_list': ['item/id::123']})
    with pytest.raises(RuntimeError) as excinfo:
        node.render(context)
    assert 'Not enough elements provided; Required: 3; Provided: 1' in str(excinfo)

    # Verification successful!
    context = get_empty_context(state={'state_item': 'foo'})
    context.output.update({'output_item_list': ['item/id::123', 'item/id::456', 'item/id::789']})
    assert node.render(context) == 'OK'

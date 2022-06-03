from ....testing_tools.mocks import get_context_with_mocks
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.document_loader import load_yaml


class TestParam(ConstantNamespace):
    identity = 'content_root/executing::greet_user==1.0'
    input_name = 'input_name'
    input_value = 'input_value'
    input_target = 'input_target'


def test_ticket_tag():
    snippet = f'''
        - {TagName.Ticket}
          - {TagName.IDENTITY} {TestParam.identity}
          - {TagName.INPUT}
            {TestParam.input_name}: {TagName.Input} {TestParam.input_target}
    '''
    context = get_context_with_mocks(input_data={TestParam.input_name: TestParam.input_value})
    node = load_yaml(snippet)[0]
    result = node.render(context)
    # Processing tickets happens at the domain/models level; this confirms we used the right interface
    assert result.result.startswith(f'Ticket mock-created for {TestParam.identity}') is True
    assert "{'input_name': <wfscript.method.tags.data_source.input.InputTag object" in result.result

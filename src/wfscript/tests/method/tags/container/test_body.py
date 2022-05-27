from ....testing_tools.mocks import get_context_with_mocks
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.document_loader import load_yaml
from .....runtime.output import MethodReturn, ActionReturn


class TestParam(ConstantNamespace):
    state_key_name = 'state_key'
    method_identity = 'path/to::some_method==production'
    action_identity = 'path/to::some_executable==production'
    input_name = 'some_input_name'


def test_body_tag():
    snippet = f'''
      - {TagName.BODY}
        - {TagName.State}
          {TestParam.input_name}: {TagName.Input} {TestParam.input_name}
        - {TagName.Method}
          - {TagName.IDENTITY} {TestParam.method_identity}
        - {TagName.Action}
          - {TagName.IDENTITY} {TestParam.action_identity}
        - {TagName.Verify}
          - {TagName.State}
            {TestParam.input_name}:
              data_type: array
              member_data_type: string
              min_size: 3
    '''
    context = get_context_with_mocks(
        input_data={
            TestParam.input_name: ['my/db::123', 'my/db::456', 'my/db::789']
        }
    )
    node = load_yaml(snippet)[0]
    # output of a !BODY render is just a collection of executor returns
    output = node.render(context)
    assert output[0] == '!State updated'
    assert isinstance(output[1], MethodReturn) is True
    assert output[1].result == f'Mock-executed method {TestParam.method_identity}'
    assert isinstance(output[2], ActionReturn) is True
    assert output[2].result == f'Mock-executed action {TestParam.action_identity}'
    assert output[3] == 'OK'

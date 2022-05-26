from ....content_root.executing import executing_namespace_root
from ....testing_tools.context import get_execution_context
from .....constants import ConstantNamespace
from .....constants.method import TagName, MethodKeyword
from .....method.document_loader import load_yaml
from .....runtime.output import ActionReturn


class TestParam(ConstantNamespace):
    identity = 'content_root/executing::hello_world==production'
    name = 'Alia'
    expected_greeting = 'Hello there, Alia!'
    output_target_name = 'some_target'
    input_field_name = 'name'


def test_action_tag():
    snippet = f'''
        - {TagName.Action}
          - {TagName.IDENTITY} {TestParam.identity}
          - {TagName.INPUT}
              {TestParam.input_field_name}: {TestParam.name}
          - {TagName.OUTPUT}
              {MethodKeyword.OUTPUT_TARGET}: {TagName.State} {TestParam.output_target_name}
    '''
    context = get_execution_context(identity=TestParam.identity, namespace_root=executing_namespace_root)
    node = load_yaml(snippet)[0]

    assert node.tag == TagName.Action
    assert node.identity == TestParam.identity
    assert node.input == {TestParam.input_field_name: TestParam.name}
    output = node.render(context)
    assert isinstance(output, ActionReturn)
    assert output.result == TestParam.expected_greeting

from ..content_root_executing import executing_namespace_root
from ...constants.loading import TagName, MethodKeyword
from ...loading.loader import _load_yaml
from ...runtime.context import RunContext


def test_action_tag():
    identity = 'content_root/executing::hello_world==production'
    name = 'Alia'
    expected_greeting = 'Hello there, Alia!'
    output_target_name = 'some_target'

    snippet = f'''
        - !Action
          {MethodKeyword.IDENTITY}: {identity}
          {MethodKeyword.INPUT}:
            name: {name}
          {MethodKeyword.OUTPUT_TARGET}: {TagName.Data} {output_target_name}
    '''
    context = RunContext(namespace_root=executing_namespace_root, data=None, state=None)
    node = _load_yaml(snippet)[0]

    assert node.tag == TagName.Action
    assert node.identity == identity
    assert node.input == {'name': name}
    assert node.execute(context) == {TagName.Data: {output_target_name: expected_greeting}}


def test_method_tag():
    identity = 'content_root/executing::greet_user==1.0'
    output_target_name = 'some_target'

    snippet = f'''
        - !Method
          {MethodKeyword.IDENTITY}: {identity}
          {MethodKeyword.INPUT}:
            foo: bar
          {MethodKeyword.OUTPUT_TARGET}: {TagName.Data} {output_target_name}
    '''
    node = _load_yaml(snippet)[0]

    assert node.tag == TagName.Method
    assert node.identity == identity
    # todo: test execution in WFS-20

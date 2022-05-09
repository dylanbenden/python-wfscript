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

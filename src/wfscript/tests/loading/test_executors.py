from ..content_root.executing import executing_namespace_root
from ...constants.loading import TagName, MethodKeyword
from ...loading.loader import _load_yaml
from ...runtime.context import get_context
from ...runtime.output import MethodReturn, ActionReturn
from ...testing import get_test_context


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
          {MethodKeyword.OUTPUT_TARGET}: {TagName.State} {output_target_name}
    '''
    context = get_test_context(namespace_root=executing_namespace_root, method_identity=identity)
    node = _load_yaml(snippet)[0]

    assert node.tag == TagName.Action
    assert node.identity == identity
    assert node.input == {'name': name}
    output = node.execute(context)
    assert isinstance(output, ActionReturn)
    assert output.result == expected_greeting


def test_method_tag_plain_return():
    identity = 'content_root/executing::greet_user==1.0'
    snippet = f'''
        - !Method
          {MethodKeyword.IDENTITY}: {identity}
          {MethodKeyword.INPUT}:
            name: !Input name
    '''
    node = _load_yaml(snippet)[0]

    assert node.tag == TagName.Method
    assert node.identity == identity

    # Tag-described Methods are called with the parent context and return a MethodReturn object
    context = get_context(identity, executing_namespace_root, {'name': 'Alia'}, {})
    output = node.execute(context)
    assert isinstance(output, MethodReturn)
    assert output.result == {'greeting': 'Hello there, Alia!'}


def test_method_tag_directed_return():
    identity = 'content_root/executing::greet_user==1.0'
    output_target_name = 'name'
    snippet = f'''
        - !Method
          {MethodKeyword.IDENTITY}: {identity}
          {MethodKeyword.INPUT}:
            name: !Input name
          {MethodKeyword.OUTPUT_TARGET}: {TagName.Output} {output_target_name}
    '''
    node = _load_yaml(snippet)[0]
    context = get_context(identity, executing_namespace_root, {'name': 'Alia'}, {})
    output = node.execute(context)
    assert output == {TagName.Output: {'greeting': 'Hello there, Alia!'}}

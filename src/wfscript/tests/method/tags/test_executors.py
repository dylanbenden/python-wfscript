from ...content_root.executing import executing_namespace_root
from ...testing_tools.context import get_execution_context
from ....constants.method import TagName, MethodKeyword
from ....method.document_loader import load_yaml
from ....runtime.context import get_context
from ....runtime.output import ActionReturn


def test_action_tag():
    identity = 'content_root/executing::hello_world==production'
    name = 'Alia'
    expected_greeting = 'Hello there, Alia!'
    output_target_name = 'some_target'

    snippet = f'''
        - {TagName.Action}
          - {TagName.IDENTITY} {identity}
          - {TagName.INPUT}
              name: {name}
          - {TagName.OUTPUT}
              {MethodKeyword.OUTPUT_TARGET}: {TagName.State} {output_target_name}
    '''
    context = get_execution_context(identity=identity, namespace_root=executing_namespace_root)
    node = load_yaml(snippet)[0]

    assert node.tag == TagName.Action
    assert node.identity == identity
    assert node.input == {'name': name}
    output = node.render(context)
    assert isinstance(output, ActionReturn)
    assert output.result == expected_greeting


def test_method_tag_plain_return():
    identity = 'content_root/executing::greet_user==1.0'
    snippet = f'''
        - {TagName.Method}
          - {TagName.IDENTITY} {identity}
          - {TagName.INPUT}
            name: {TagName.Input} name
          
    '''
    node = load_yaml(snippet)[0]

    assert node.tag == TagName.Method
    assert node.identity == identity

    # Tag-described Methods are called with the parent context and return a MethodReturn object
    context = get_context(identity, executing_namespace_root, {'name': 'Alia'}, {})
    # todo: plug in execution and test
    # import ipdb; ipdb.set_trace()
    # output = node.execute(context)
    # assert isinstance(output, MethodReturn)
    # assert output.result == {'greeting': 'Hello there, Alia!'}


def test_method_tag_directed_return():
    identity = 'content_root/executing::greet_user==1.0'
    output_target_name = 'name'
    snippet = f'''
        - !Method
          - {TagName.IDENTITY} {identity}
          - {TagName.INPUT}
              name: {TagName.Input} name
          - {TagName.OUTPUT}
              {MethodKeyword.OUTPUT_TARGET}: {TagName.Output} {output_target_name}
    '''
    node = load_yaml(snippet)[0]
    context = get_context(identity, executing_namespace_root, {'name': 'Alia'}, {})
    # todo: plug in exectution and test
    # output = node.execute(context)
    # assert output == {TagName.Output: {'greeting': 'Hello there, Alia!'}}

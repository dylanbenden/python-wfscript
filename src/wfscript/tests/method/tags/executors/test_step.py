from ....testing_tools.mocks import get_context_with_mocks
from .....constants import ConstantNamespace
from .....constants.method import TagName, MethodKeyword
from .....method.document_loader import load_yaml
from .....runtime.output import MethodReturn, StepReturn
from .....runtime.utils.identity import deconstruct_identity


class TestParam(ConstantNamespace):
    step_name = 'my_test_step'
    first_method_id = 'path/to::first_method==production'
    second_method_id = 'path/to::second_method==1.0'
    output_target_name = 'name'
    step_output_key = 'some_output'
    step_output_value = 'my data'


def test_step_tag_output():
    no_output_snippet = f'''
        - {TagName.Step}
          - {TagName.name} {TestParam.step_name}
          - {TagName.BODY}
            - {TagName.Method}
              - {TagName.IDENTITY} {TestParam.first_method_id}
            - {TagName.Method}
              - {TagName.IDENTITY} {TestParam.second_method_id}
    '''
    context = get_context_with_mocks()
    node = load_yaml(no_output_snippet)[0]
    assert node.tag_name == TagName.Step
    assert node.value[TagName.name].value == TestParam.step_name
    first_method_node = node.body.value[0]
    second_method_node = node.body.value[1]
    assert first_method_node.tag_name == TagName.Method
    assert first_method_node.value[TagName.IDENTITY] == deconstruct_identity(TestParam.first_method_id)
    assert second_method_node.tag_name == TagName.Method
    assert second_method_node.value[TagName.IDENTITY] == deconstruct_identity(TestParam.second_method_id)

    # verify methods render individually
    first_output = first_method_node.render(context)
    assert isinstance(first_output, MethodReturn) is True
    assert first_output.result == f'Mock-executed {TestParam.first_method_id}'
    assert first_output.resume == dict()

    second_output = second_method_node.render(context)
    assert isinstance(second_output, MethodReturn) is True
    assert second_output.result == f'Mock-executed {TestParam.second_method_id}'
    assert second_output.resume == dict()

    step_result = node.render(context)
    assert isinstance(step_result, StepReturn)
    # there is not !OUTPUT defined for this Step, so output will be handled by containing Method
    assert step_result.result == dict()
    # confirm that we ran both methods in order
    assert [item.result for item in context.debug[0]] == [first_output.result, second_output.result]

    # test steps with step output
    with_output_snippet = f'''
        - {TagName.Step}
          - {TagName.name} {TestParam.step_name}
          - {TagName.BODY}
            - {TagName.Method}
              - {TagName.IDENTITY} {TestParam.first_method_id}
            - {TagName.Method}
              - {TagName.IDENTITY} {TestParam.second_method_id}
          - {TagName.OUTPUT}
              {TestParam.step_output_key}: {TestParam.step_output_value}
    '''
    context = get_context_with_mocks()
    node = load_yaml(with_output_snippet)[0]
    step_result = node.render(context)
    assert isinstance(step_result, StepReturn)
    # because we do have an !OUTPUT defined for this Step, that output is held by StepResult
    assert step_result.result == {TestParam.step_output_key: TestParam.step_output_value}

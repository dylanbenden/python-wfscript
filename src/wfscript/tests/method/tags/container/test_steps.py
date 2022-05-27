from ....testing_tools.mocks import get_context_with_mocks
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....constants.payload import PayloadKey
from .....method.document_loader import load_yaml
from .....runtime.output import StepReturn


class TestParam(ConstantNamespace):
    method_identity = 'path/to::some_method==production'
    first_step_name = 'my_step_one'
    second_step_name = 'my_step_two'
    first_step_input_key = 'my_first_input_key'
    second_step_input_key = 'my_second_input_key'
    first_step_input_value = 'ABC:123'
    second_step_input_value = '456, pick up sticks'



def test_steps_tag():
    snippet = f'''
      - {TagName.STEPS}
        - {TagName.Step}
          - {TagName.name} {TestParam.first_step_name}
          - {TagName.INPUT}
            {TestParam.first_step_input_key}:
              data_type: string
              required: true
          - {TagName.BODY}
            - {TagName.State}
               {TestParam.first_step_input_key}: {TagName.Input} {TestParam.first_step_input_key}
          - {TagName.OUTPUT}
            message: First Step Success!
            got_input: {TagName.Input} {TestParam.first_step_input_key}

        - {TagName.Step}
          - {TagName.name} {TestParam.second_step_name}
          - {TagName.INPUT}
            {TestParam.second_step_input_key}:
              data_type: string
              required: true
          - {TagName.BODY}
            - {TagName.Method}
              - {TagName.IDENTITY} {TestParam.method_identity}
          - {TagName.OUTPUT}
            message: Second Step Success!
            got_input: {TagName.Input} {TestParam.second_step_input_key}
            retained_data: {TagName.State} {TestParam.first_step_input_key}
            
    '''
    context_no_resume = get_context_with_mocks(
        input_data={TestParam.first_step_input_key: TestParam.first_step_input_value},
        method=TestParam.method_identity
    )
    node = load_yaml(snippet)[0]
    first_step_output = node.render(context_no_resume)
    assert isinstance(first_step_output, StepReturn) is True
    assert first_step_output.result == {'got_input': TestParam.first_step_input_value, 'message': 'First Step Success!'}
    assert first_step_output.resume == {
        PayloadKey.METHOD: TestParam.method_identity,
        PayloadKey.STEP: TestParam.first_step_name
    }

    context_with_resume_and_state = get_context_with_mocks(
        input_data={TestParam.second_step_input_key: TestParam.second_step_input_value},
        # state / resume are managed by whoever creates the context
        state={TestParam.first_step_input_key: TestParam.first_step_input_value},
        method=TestParam.method_identity,
        resume_info=first_step_output.resume
    )
    node = load_yaml(snippet)[0]
    second_step_output = node.render(context_with_resume_and_state)
    assert isinstance(second_step_output, StepReturn) is True
    assert second_step_output.result == {
        'message': 'Second Step Success!',
        'got_input': TestParam.second_step_input_value,
        'retained_data': TestParam.first_step_input_value
    }
    assert second_step_output.resume == {
        PayloadKey.METHOD: TestParam.method_identity,
        PayloadKey.STEP: TestParam.second_step_name
    }

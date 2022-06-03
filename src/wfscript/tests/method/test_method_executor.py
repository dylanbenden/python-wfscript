from ..content_root.executing import executing_namespace_root
from ...constants.payload import PayloadKey
from ...runtime.output import StepReturn, MethodReturn


def test_method_properties():
    pass


def test_run():
    identity = 'content_root/executing::greet_user==1.0'
    executor = executing_namespace_root.get_method(identity)
    input_data = {
        'name': 'Alia'
    }
    output = executor.execute(input_data=input_data)
    assert isinstance(output, MethodReturn)
    assert output.result['greeting'] == 'Hello there, Alia!'
    assert output.resume == dict()


def test_multi_step():
    identity = 'content_root/executing::talent_pipeline==1.0'
    step_names = [
        'create_candidate_profile',
        'send_hire_letter'
    ]
    executor = executing_namespace_root.get_method(identity)

    first_input = {
        'first_name': 'Kira',
        'last_name': 'Nerys',
        'personal_email': 'maj.kira@bajor.alpha_quadrant'
    }
    first_step_output = executor.execute(input_data=first_input)
    assert isinstance(first_step_output, StepReturn) is True
    resume_info = first_step_output.resume
    assert resume_info == {PayloadKey.METHOD: identity, PayloadKey.STEP: step_names[0]}

    second_input = dict()
    expected_acceptance_code = 'CODE-98765'
    second_step_output = executor.execute(input_data=second_input, state=first_step_output.state,
                                          resume_info=resume_info)
    resume_info = second_step_output.resume
    assert resume_info == {PayloadKey.METHOD: identity, PayloadKey.STEP: step_names[1]}

    third_input = {
        'acceptance_code': expected_acceptance_code
    }
    expected_result = {
        'user_name': 'kira.nerys',
        'message': 'User kira.nerys has successfully accepted their offer'
    }
    third_result = executor.execute(input_data=third_input, state=second_step_output.state,
                                    resume_info=resume_info)
    resume_info = third_result.resume
    assert resume_info == {}
    assert third_result.result == expected_result

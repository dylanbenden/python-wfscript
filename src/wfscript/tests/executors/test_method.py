from ..content_root.executing import executing_namespace_root
from ...constants.payload import PayloadKey


def test_method_properties():
    pass


def test_run():
    identity = 'content_root/executing::greet_user==1.0'
    executor = executing_namespace_root.get_method(identity)
    input_data = {
        'name': 'Alia'
    }
    result = executor.run(input_data=input_data)
    assert isinstance(result, dict)
    assert result[PayloadKey.RESULT]['greeting'] == 'Hello there, Alia!'
    assert result[PayloadKey.RESUME] == dict()
    assert PayloadKey.RUN_ID in result
    assert PayloadKey.TIMESTAMP in result


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
    first_result = executor.run(input_data=first_input)
    resume_info = first_result[PayloadKey.RESUME]
    state = resume_info.pop(PayloadKey.STATE)
    assert resume_info == {PayloadKey.METHOD: identity, PayloadKey.STEP: step_names[0]}
    assert state == dict(first_input, user_name='kira.nerys')

    second_input = dict()
    expected_acceptance_code = 'CODE-98765'
    second_result = executor.run(input_data=second_input, state=state, resume_info=resume_info)
    resume_info = second_result[PayloadKey.RESUME]
    state = resume_info.pop(PayloadKey.STATE)
    assert resume_info == {PayloadKey.METHOD: identity, PayloadKey.STEP: step_names[1]}
    assert state == dict(first_input, user_name='kira.nerys', acceptance_code=expected_acceptance_code)

    third_input = {
        'acceptance_code': expected_acceptance_code
    }
    expected_result = {
        'user_name': 'kira.nerys',
        'message': 'User kira.nerys has successfully accepted their offer'
    }
    third_result = executor.run(input_data=third_input, state=state, resume_info=resume_info)
    resume_info = third_result[PayloadKey.RESUME]
    assert resume_info == {}
    assert third_result[PayloadKey.RESULT] == expected_result

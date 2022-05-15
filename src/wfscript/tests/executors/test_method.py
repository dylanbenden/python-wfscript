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


def test__sanity_check():
    pass


def test__get_context():
    pass


def test__load_next_items():
    pass


def test__process_result():
    pass


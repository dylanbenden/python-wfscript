from ...runtime.data import BaseRuntimeData, State


def test_data_properties():
    name_data = {
        'first_name': 'Kira',
        'last_name': 'Nerys'
    }
    data_obj = BaseRuntimeData(name_data)
    assert data_obj.value == name_data


def test_data_update():
    name_data = {
        'first_name': 'Kira',
        'last_name': 'Nerys'
    }
    state_obj = State(name_data)
    assert state_obj.value == name_data
    rank_value = {'rank': 'Major'}
    state_obj.update(rank_value)
    assert state_obj.value == dict(name_data, **rank_value)


def test_set_resume_state():
    name_data = {
        'first_name': 'Kira',
        'last_name': 'Nerys'
    }
    state_obj = State(name_data)
    assert state_obj.last_method is None
    assert state_obj.last_step is None
    last_method_id = 'fake/namespace::some_method==1.0'
    last_step_performed = 'Recalibrate the induction coils'
    state_obj.set_resume_state(last_method_id, last_step_performed)
    assert state_obj.last_method is last_method_id
    assert state_obj.last_step is last_step_performed

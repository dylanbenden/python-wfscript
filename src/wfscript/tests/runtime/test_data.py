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

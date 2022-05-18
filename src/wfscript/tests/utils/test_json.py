from decimal import Decimal

from ...materials.mixin import WorkflowMaterial
from ...utils.json import unfloat, preserialize

class BogusDomain(object):
    pass


class BogusMaterial(WorkflowMaterial):
    model_identity = 'bogus/model'
    identity_field = 'bogus_id_field'

    @property
    def bogus_id_field(self):
        return 123


def test_preserialize():
    bogus_material = BogusMaterial()
    expected_material_identity = 'bogus/model::123'
    assert bogus_material.identity == expected_material_identity

    to_preserialize = {
        'name': 'Kira Nerys',
        'lucky_numbers': [3, 8, Decimal('4.7')],
        'subdict': {
            'sublist': [Decimal(11.1), {'material': bogus_material}]
        }
    }
    expected = {
        'name': 'Kira Nerys',
        'lucky_numbers': [3, 8, 4.7],
        'subdict': {
            'sublist': [
                11.1,
                {'material': expected_material_identity}
            ]
        }
    }
    assert preserialize(to_preserialize) == expected

def test_unfloat():
    dict_with_floats = {'name': 'Will Riker', 'favorite_number': 1.0}
    list_with_floats = [14, 3.8, 'hello']
    float_data = 3.5

    assert unfloat(dict_with_floats) == {'name': 'Will Riker', 'favorite_number': Decimal('1')}
    assert unfloat(list_with_floats) == [14, Decimal('3.8'), 'hello']
    assert unfloat(float_data) == Decimal('3.5')

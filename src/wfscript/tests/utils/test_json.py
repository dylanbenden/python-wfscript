from decimal import Decimal

from ...constants.identity import IdentityDelimeter
from ...materials.mixin import MaterialMixin
from ...utils.json import unfloat, preserialize

class BogusDomain(object):
    pass


def test_preserialize():
    bogus_material = MaterialMixin()
    bogus_material.domain = BogusDomain()
    bogus_material.domain.identity = 'domid333'
    bogus_material.barcode_field_name = 'barcode'
    bogus_material.barcode = 'abc123'

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
                {'material': f'{bogus_material.domain.identity}{IdentityDelimeter.DOMAIN}{bogus_material.barcode}'}]
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

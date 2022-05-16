import pytest

from ...tests.content_root.validation import validation_namespace_root


def test_simple_input_validator():
    identity = 'content_root_validation/personnel::validate_person==1.0'
    validator = validation_namespace_root.get_validator(identity)

    valid_examples = [
        {
            'name': 'Q'
        },
        {
            'name': 'Kathryn Janeway',
            'favorite_drink': 'coffee',
        },
        {
            'name': 'William Riker',
            'favorite_number': 1
        },

    ]
    # happy paths
    for test_data in valid_examples:
        assert validator.validate(test_data) is True

    # fail paths
    # extra field provided
    invalid_extra_field = {
        'name': 'Seven',
        'designation': 'Seven of Nine, Tertiary Adjunct of Unimatrix 01'
    }
    with pytest.raises(RuntimeError) as excinfo:
        validator.validate(invalid_extra_field)
    assert 'Unexpected data/payload key(s) provided' in str(excinfo.value)

    # wrong data type: str for int
    invalid_wrong_data_type_1 = {
        'name': 'Will Riker',
        'favorite_number': 'Number One'
    }
    with pytest.raises(RuntimeError) as excinfo:
        validator.validate(invalid_wrong_data_type_1)
    assert 'Expected integer, got: Number One' in str(excinfo.value)

    # wrong data type: array of int, not int
    invalid_wrong_data_type_2 = {
        'name': 'Will Riker',
        'favorite_number': [1]
    }
    with pytest.raises(RuntimeError) as excinfo:
        validator.validate(invalid_wrong_data_type_2)
    assert 'Expected integer, got: [1]' in str(excinfo.value)



def test_validate_array_spec():
    identity = 'content_root_validation/personnel::spec_identify_people==1.0'
    validator = validation_namespace_root.get_validator(identity)

    valid_input = {
        'personnel': [
            {
                'name': 'Q'
            },
            {
                'name': 'Kathryn Janeway',
                'favorite_drink': 'coffee',
            },
            {
                'name': 'William Riker',
                'favorite_number': 1
            },
        ],
        'lucky_numbers': [42, 47, 127]
    }

    assert validator.validate(valid_input) is True

    # Fail paths: too few or too many members (min_size 2; max_size 3)
    not_enough_members = {
        'personnel': [
            {
                'name': 'Q'
            },
        ],
        'lucky_numbers': [42, 47, 127]
    }
    with pytest.raises(RuntimeError) as excinfo:
        validator.validate(not_enough_members)
    assert 'Not enough elements' in str(excinfo.value)

    too_many_members = {
        'personnel': [
            {
                'name': 'Q'
            },
            {
                'name': 'Kathryn Janeway',
                'favorite_drink': 'coffee',
            },
            {
                'name': 'William Riker',
                'favorite_number': 1
            },
            {
                'name': 'Neelix'
            }
        ],
        'lucky_numbers': [42, 47, 127]
    }
    with pytest.raises(RuntimeError) as excinfo:
        validator.validate(too_many_members)
    assert 'Too many elements' in str(excinfo.value)


def test_validate_nested_array_spec():
    identity = 'content_root_validation/assignments::validate_assignments==1.0'
    validator = validation_namespace_root.get_validator(identity)

    valid_input = {
        'duty_assignments': [
            {
                'ship_name': 'Enterprise',
                'hull_number': 'NCC-1701',
                'personnel': [
                    {
                        'name': 'Jean-Luc Picard',
                        'favorite_drink': 'Tea, Earl Grey, hot'
                    },
                    {
                        'name': 'William Riker',
                        'favorite_number': 1
                    },
                    {
                        'name': 'Dr. Beverly Crusher'
                    }
                ]
            },
            {
                'ship_name': 'Voyager',
                'hull_number': 'NCC-74656',
                'personnel': [
                    {
                        'name': 'Kathryn Janeway',
                        'favorite_drink': 'coffee',
                    },
                    {
                        'name': 'Harry Kim',
                    }
                ]
            },
        ]
    }
    assert validator.validate(valid_input) is True


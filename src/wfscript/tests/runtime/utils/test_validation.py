import pytest

from ....runtime.utils.validation import validate_expected_and_required_values


def test_validate_expected_and_required():
    required = ['b']
    expected = ['a', 'b', 'c']
    kw_configs = {
        'expected_values': expected,
        'required_values': required,
        'descriptor': 'item'
        }

    validator = validate_expected_and_required_values

    # happy paths
    assert validator(provided_values=['b'], **kw_configs) is True
    assert validator(provided_values=['a', 'b'], **kw_configs) is True
    assert validator(provided_values=['c', 'b'], **kw_configs) is True
    assert validator(provided_values=['c', 'a', 'b'], **kw_configs) is True
    assert validator(provided_values=['c', 'a', 'b'], **kw_configs) is True
    assert validator(provided_values=['a', 'c', 'a', 'b'], **kw_configs) is True

    # required element missing
    with pytest.raises(RuntimeError) as excinfo:
        validator(provided_values=['a', 'c'], **kw_configs)
    assert 'Required item(s) missing' in str(excinfo.value)

    # extra element provided
    with pytest.raises(RuntimeError) as excinfo:
        validator(provided_values=['a', 'b', 'c', 'd'], **kw_configs)
    assert 'Unexpected item(s) provided' in str(excinfo.value)

    # string provided instead of non-string iterable
    with pytest.raises(TypeError) as excinfo:
        validator(provided_values='abc', **kw_configs)
    assert 'Expecting non-string collection' in str(excinfo.value)


import decimal

from ...constants.validation import DataType, ValidatorKeyword
from ...method.nodes.base import WorkflowNode


def validate_input(spec_part, data_part, namespace_root):
    if isinstance(data_part, dict):
        return _validate_dict(spec_part, data_part, namespace_root)
    else:
        return _validate_list(spec_part, data_part, namespace_root)


def validate_expected_and_required_values(provided_values, expected_values=None, required_values=None, descriptor=None):
    if expected_values is None:
        expected_values = list()

    if required_values is None:
        required_values = list()

    if descriptor is None:
        descriptor = 'value'

    for arg in [expected_values, required_values, provided_values]:
        if isinstance(arg, str):
            raise TypeError(f'Expecting non-string collection, got {arg}')

    required = set(required_values)
    # if a name is required, it is presumed to also be expected
    expected = set(expected_values).union(required)
    provided = set(provided_values)

    missing = required - provided
    unexpected = provided - expected

    if missing:
        raise RuntimeError(f'Required {descriptor}(s) missing: {missing}; Provided: {provided}')

    if unexpected:
        raise RuntimeError(f'Unexpected {descriptor}(s) provided: {unexpected}; Expected: {expected}')

    return True


def int_or_none(value):
    if value is not None:
        return int(value)


def _validate_dict(spec_part, data_part, ns_root):
    if 'id' in spec_part:
        spec_part = ns_root.get_specification(spec_part['id']).input_section
    validate_expected_and_required_values(
        expected_values=spec_part.keys(),
        required_values=[k for k, v in spec_part.items() if isinstance(v, dict) and v.get(ValidatorKeyword.REQUIRED)],
        provided_values=data_part.keys(),
        descriptor='data/payload key'
    )
    # having confirmed that all required fields are provided and all provided fields are allowed,
    # we only need to step through the data that is actually provided
    for field_name, data_value in data_part.items():
        spec_details = spec_part[field_name]
        if spec_details[ValidatorKeyword.DATA_TYPE] == DataType.OBJECT:
            if spec_details[ValidatorKeyword.MEMBER_SPEC]:
                _validate_dict(spec_details[ValidatorKeyword.MEMBER_SPEC], data_value, ns_root)
            else:
                return True
        elif spec_details[ValidatorKeyword.DATA_TYPE] == DataType.ARRAY:
            _validate_list(spec_details, data_value, ns_root)
        elif spec_details[ValidatorKeyword.DATA_TYPE] == DataType.RECORD:
            validate_material(spec_details, data_value, ns_root)
        elif spec_details[ValidatorKeyword.DATA_TYPE] == DataType.TAG:
            _validate_dict(spec_details, data_value.value, ns_root)
        else:
            _validate_scalar(spec_details, data_value)
    return True

def _validate_scalar(spec_part, data_part):
    expected_data_type = spec_part[ValidatorKeyword.DATA_TYPE]
    required = spec_part.get(ValidatorKeyword.REQUIRED, False)
    validation_failure = False
    if required and data_part is None:
        validation_failure = True
    none_type = type(None)
    if expected_data_type == DataType.STRING:
        if not isinstance(data_part, (str, none_type)):
            validation_failure = True
    elif expected_data_type == DataType.NUMBER:
        if not isinstance(data_part, (int, float, decimal.Decimal, none_type)):
            validation_failure = True
    elif expected_data_type == DataType.INTEGER:
        if not isinstance(data_part, (int, none_type)):
            validation_failure = True
    elif expected_data_type == DataType.FLOAT:
        if not isinstance(data_part, (float, none_type)):
            validation_failure = True
    elif expected_data_type == DataType.BOOLEAN:
        if not isinstance(data_part, bool, none_type):
            validation_failure = True
    # elif expected_data_type == DataType.OTHER:
    #     raise NotImplementedError(f'Need to implement validation handling for DataType.OTHER')
    else:
        import ipdb; ipdb.set_trace()
        raise NotImplementedError(f'No validation handling implemented for data_type {expected_data_type}')
    if validation_failure:
        raise RuntimeError(f'Expected {expected_data_type}, got: {data_part} (type: {type(data_part)})')


def _validate_list(spec_part, data_part, ns_root):
    if isinstance(spec_part, WorkflowNode):
        import ipdb; ipdb.set_trace()
    min_size = int_or_none(spec_part.get(ValidatorKeyword.MIN_SIZE))
    max_size = int_or_none(spec_part.get(ValidatorKeyword.MAX_SIZE))
    count_elems_provided = len(data_part)
    if min_size and count_elems_provided < min_size:
        raise RuntimeError(f'Not enough elements provided; Required: {min_size}; Provided: {count_elems_provided}')
    if max_size and count_elems_provided > max_size:
        raise RuntimeError(f'Too many elements provided; Permitted: {max_size}; Provided: {count_elems_provided}')

    member_data_type = spec_part.get(ValidatorKeyword.MEMBER_DATA_TYPE)
    member_spec = spec_part.get(ValidatorKeyword.MEMBER_SPEC)
    if member_spec is not None and 'id' in member_spec:
        validator = ns_root.get_validator(member_spec['id'])
        map(validator.validate, data_part)
    elif member_data_type:
        if member_data_type == DataType.OBJECT:
            _ = [_validate_dict(member_spec, member, ns_root) for member in data_part]
        elif member_data_type == DataType.ARRAY:
            _ = [_validate_list(member_spec, member, ns_root) for member in data_part]
        elif member_data_type == DataType.RECORD:
            _ = [validate_material(member_spec, member, ns_root) for member in data_part]
        else:
            _ = [_validate_scalar({ValidatorKeyword.DATA_TYPE: member_data_type}, member) for member in data_part]

def validate_material(spec_part, data_part, ns_root):
    pass
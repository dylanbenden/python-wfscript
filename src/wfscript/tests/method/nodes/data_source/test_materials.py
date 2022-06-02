import pytest

from ....testing_tools.context import get_empty_context
from ....testing_tools.mocks import MockIdentifiedObject, get_context_with_mocks
from ....testing_tools.nodes import render_for_phase_and_shape, Phase, ConfigShape, assert_unsupported
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml


def test_material_retrieval_singular():
    # Phase.EXECUTE, ConfigShape.SCALAR
    # When rendered in ExecutePhase, we expect !Material to return an object
    obj1 = MockIdentifiedObject('one')
    obj2 = MockIdentifiedObject('two')
    obj3 = MockIdentifiedObject('three')
    obj4 = MockIdentifiedObject('four')
    context = get_empty_context(
        input_data={
            'key_in_input_only': obj1,
            'key_in_input_and_state': None
        },
        state={
            'key_in_state_only': obj2,
            'key_in_input_and_state': obj4
        }
    )
    context.output.update({'key_in_output_only': obj3})
    test_cases = {
        'key_in_input_only': obj1,
        'key_in_state_only': obj2,
        'key_in_output_only': obj3,
        'key_in_input_and_state': obj4,
    }
    for mat_name, expected_object in test_cases.items():
        node = load_yaml(
            f'''
              {TagName.Material} {mat_name}
            '''
        )
        output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
        assert output.identity == expected_object.identity

def test_material_retrieval_plural():
    # Phase.EXECUTE, ConfigShape.SCALAR
    # When rendered in ExecutePhase, we expect !Materials to return a collection of objects
    obj1 = MockIdentifiedObject('one')
    obj2 = MockIdentifiedObject('two')
    obj3 = MockIdentifiedObject('three')
    obj4 = MockIdentifiedObject('four')
    context = get_empty_context(
        input_data={
            'key_in_input_only': [obj1],
            'key_in_input_and_state': [None]
        },
        state={
            'key_in_state_only': [obj2],
            'key_in_input_and_state': [obj4]
        }
    )
    context.output.update({'key_in_output_only': [obj3]})
    test_cases = {
        'key_in_input_only': obj1,
        'key_in_state_only': obj2,
        'key_in_output_only': obj3,
        'key_in_input_and_state': obj4,
    }
    for mat_name, expected_object in test_cases.items():
        node = load_yaml(
            f'''
              {TagName.Materials} {mat_name}
            '''
        )
        output = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, node, context)
        assert [item.identity for item in output] == [expected_object.identity]


def test_material_serialization_singular():
    # Phase.OUTPUT, ConfigShape.SCALAR
    # When rendered in OutputPhase, we expect !Material to return an identity
    obj1 = MockIdentifiedObject('one')
    obj2 = MockIdentifiedObject('two')
    obj3 = MockIdentifiedObject('three')
    obj4 = MockIdentifiedObject('four')
    context = get_empty_context(
        input_data={
            'key_in_input_only': obj1,
            'key_in_input_and_state': None
        },
        state={
            'key_in_state_only': obj2,
            'key_in_input_and_state': obj4
        }
    )
    context.output.update({'key_in_output_only': obj3})
    test_cases = {
        'key_in_input_only': obj1,
        'key_in_state_only': obj2,
        'key_in_output_only': obj3,
        'key_in_input_and_state': obj4,
    }
    for mat_name, expected_object in test_cases.items():
        node = load_yaml(
            f'''
              {TagName.Material} {mat_name}
            '''
        )
        output = render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context)
        assert output == expected_object.identity


def test_material_serialization_plural():
    # Phase.OUTPUT, ConfigShape.SCALAR
    # When rendered in OutputPhase, we expect !Material to return a collection of identities
    obj1 = MockIdentifiedObject('one')
    obj2 = MockIdentifiedObject('two')
    obj3 = MockIdentifiedObject('three')
    obj4 = MockIdentifiedObject('four')
    context = get_empty_context(
        input_data={
            'key_in_input_only': [obj1],
            'key_in_input_and_state': [None]
        },
        state={
            'key_in_state_only': [obj2],
            'key_in_input_and_state': [obj4]
        }
    )
    context.output.update({'key_in_output_only': [obj3]})
    test_cases = {
        'key_in_input_only': obj1,
        'key_in_state_only': obj2,
        'key_in_output_only': obj3,
        'key_in_input_and_state': obj4,
    }
    for mat_name, expected_object in test_cases.items():
        node = load_yaml(
            f'''
              {TagName.Materials} {mat_name}
            '''
        )
        output = render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, node, context)
        assert output == [expected_object.identity]


class MatLoading(ConstantNamespace):
    single_mat_id = 'bogus/system::1'
    plural_mat_ids = ['bogus/system::2', 'bogus/system::3']
    single_mat_name = 'single_mat_id'
    plural_mats_name = 'list_of_mat_ids'
    unrendered_single_mat_id = 'bogus/system::4'
    unrendered_single_mat_name = 'unloaded_single_mat_id'
    unrendered_plural_mat_ids = ['bogus/system::5', 'bogus/system::6']
    unrendered_plural_mats_name = 'unloaded_list_of_mat_ids'


def test_material_domain_loading():
    # Phase.EXECUTE, ConfigShape.SCALAR
    context = get_context_with_mocks(
        input_data={
            MatLoading.single_mat_name: MatLoading.single_mat_id,
            MatLoading.plural_mats_name: MatLoading.plural_mat_ids
        }
    )
    snippet = f'''
      - {TagName.Material} {MatLoading.single_mat_name}
      - {TagName.Materials} {MatLoading.plural_mats_name}
    '''
    single_mat_node, plural_mat_node = load_yaml(snippet)
    single_result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, single_mat_node, context)
    assert isinstance(single_result, MockIdentifiedObject) is True
    assert single_result.value == MatLoading.single_mat_id

    plural_result = render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.SCALAR, plural_mat_node, context)
    assert all([isinstance(item, MockIdentifiedObject) for item in plural_result])
    assert [item.value for item in plural_result] == MatLoading.plural_mat_ids


def test_unsupported():
    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.LIST),
        (Phase.OUTPUT, ConfigShape.DICT),
        (Phase.OUTPUT, ConfigShape.LIST),
    ]
    context = get_empty_context()
    for tag_name in [TagName.Material, TagName.Materials]:
        node = load_yaml(
            f'''
              {tag_name} foo
            '''
        )
        assert_unsupported(unsupported, node, context)

import pytest

from ....constants.method import TagName
from ....method.document_loader import _load_yaml
from ....testing.context import get_empty_context
from ....testing.mocks import MockIdentifiedObject, get_context_with_mock_domain


def test_material_retrieval_singular():
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
    for tag in [TagName.Material, TagName.Asset]:
        for mat_name, expected_object in test_cases.items():
            snippet = f'''
              - {tag} {mat_name}
            '''
            node = _load_yaml(snippet)[0]
            assert node.render(context).value == expected_object.value

def test_material_retrieval_plural():
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
    for tag in [TagName.Materials, TagName.Assets]:
        for mat_name, expected_object in test_cases.items():
            snippet = f'''
              - {tag} {mat_name}
            '''
            node = _load_yaml(snippet)[0]
            assert node.render(context)[0].value == expected_object.value

def test_cardinality_checking():
    obj = MockIdentifiedObject('one')
    objs = [MockIdentifiedObject('two')]
    context = get_empty_context(
        input_data={
            'singular_obj': obj,
            'obj_collection': objs
        }
    )

    # singular tag, collection found
    for singular_tag in [TagName.Material, TagName.Asset]:
        snippet = f'''
          - {singular_tag} obj_collection
        '''
        node = _load_yaml(snippet)[0]
        with pytest.raises(RuntimeError) as excinfo:
            node.render(context)
        assert f'{singular_tag} expects single object' in str(excinfo)

    # plural tag, single obj found
    for plural_tag in [TagName.Materials, TagName.Assets]:
        snippet = f'''
          - {plural_tag} singular_obj
        '''
        node = _load_yaml(snippet)[0]
        with pytest.raises(RuntimeError) as excinfo:
            node.render(context)
        assert f'{plural_tag} expects an array' in str(excinfo)


def test_material_domain_loading():
    single_mat_id = 'bogus/system::1'
    plural_mat_ids = ['bogus/system::2', 'bogus/system::3']
    single_mat_name = 'single_mat_id'
    plural_mats_name = 'list_of_mat_ids'
    context = get_context_with_mock_domain(
        input_data={
            single_mat_name: single_mat_id,
            plural_mats_name: plural_mat_ids
        }
    )
    snippet = f'''
      - {TagName.Material} {single_mat_name}
      - {TagName.Materials} {plural_mats_name}
    '''
    single_mat_node, plural_mat_node = _load_yaml(snippet)
    single_result = single_mat_node.render(context)
    assert isinstance(single_result, MockIdentifiedObject) is True
    assert single_result.value == single_mat_id
    assert single_mat_node.render_for_output(context) == single_mat_id

    plural_result = plural_mat_node.render(context)
    assert all([isinstance(item, MockIdentifiedObject) for item in plural_result])
    assert [item.value for item in plural_result] == plural_mat_ids
    assert plural_mat_node.render_for_output(context) == plural_mat_ids


def test_render_for_output():
    single_mat_id = 'bogus/system::1'
    single_mat_name = 'single_mat_id'
    plural_mat_ids = ['bogus/system::2', 'bogus/system::3']
    plural_mats_name = 'list_of_mat_ids'

    unrendered_single_mat_id = 'bogus/system::4'
    unrendered_single_mat_name = 'unloaded_single_mat_id'
    unrendered_plural_mat_ids = ['bogus/system::5', 'bogus/system::6']
    unrendered_plural_mats_name = 'unloaded_list_of_mat_ids'

    context = get_context_with_mock_domain(
        input_data={
            single_mat_name: single_mat_id,
            unrendered_single_mat_name: unrendered_single_mat_id,
            plural_mats_name: plural_mat_ids,
            unrendered_plural_mats_name: unrendered_plural_mat_ids
        }
    )
    snippet = f'''
      - {TagName.Material} {single_mat_name}
      - {TagName.Materials} {plural_mats_name}
      - {TagName.Material} {unrendered_single_mat_name}
      - {TagName.Materials} {unrendered_plural_mats_name}
    '''
    single_mat_node, plural_mat_node, unrendered_single_node, unrendered_plural_node = _load_yaml(snippet)

    # render these first, then render output, get back identity/ies
    single_mat_node.render(context)
    assert single_mat_node.render_for_output(context) == single_mat_id
    plural_mat_node.render(context)
    assert plural_mat_node.render_for_output(context) == plural_mat_ids

    # don't render these first, then render output, get back identity/ies same as above
    assert unrendered_single_node.render_for_output(context) == unrendered_single_mat_id
    assert unrendered_plural_node.render_for_output(context) == unrendered_plural_mat_ids

from ....testing_tools.mocks import get_context_with_mock_domain
from .....constants.method import TagName
from .....method.document_loader import load_yaml


def test_output_tag():
    plain_scalar_value = 'some unrendered scalar'
    plain_scalar_output_key = 'plain_scalar_output'

    plain_scalar_input_value = 'some_scalar'
    plain_scalar_input_name = 'some_scalar_id'
    plain_scalar_input_output_key = 'scalar_output'

    single_mat_id = 'bogus/system::1'
    single_mat_name = 'single_mat_id'
    single_mat_output_key = 'single_mat_output'

    plural_mat_ids = ['bogus/system::2', 'bogus/system::3']
    plural_mats_name = 'list_of_mat_ids'
    plural_mats_output_key = 'plural_mats_output'

    unrendered_single_mat_id = 'bogus/system::4'
    unrendered_single_mat_name = 'unloaded_single_mat_id'
    unrendered_single_mat_output_key = 'unrendered_single_mat_output'

    unrendered_plural_mat_ids = ['bogus/system::5', 'bogus/system::6']
    unrendered_plural_mats_name = 'unloaded_list_of_mat_ids'
    unrendered_plural_mats_output_key = 'unrendered_plural_mats_output'

    context = get_context_with_mock_domain(
        input_data={
            plain_scalar_input_name: plain_scalar_input_value,
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

      - {TagName.OUTPUT}
        {plain_scalar_output_key}: {plain_scalar_value}
        {plain_scalar_input_output_key}: {TagName.Input} {plain_scalar_input_name}
        {single_mat_output_key}: {TagName.Material} {single_mat_name}
        {plural_mats_output_key}: {TagName.Materials} {plural_mats_name}
        {unrendered_single_mat_output_key}: {TagName.Material} {unrendered_single_mat_name}
        {unrendered_plural_mats_output_key}: {TagName.Materials} {unrendered_plural_mats_name}
    '''
    nodes = load_yaml(snippet)
    # first, render *some* materials to show prior rendering has no effect on output
    mat_nodes_to_render = nodes[:4]
    for to_render in mat_nodes_to_render:
        to_render.render(context)

    # render output and verify returned results
    output_node = nodes[4]
    result = output_node.render(context)
    assert result[plain_scalar_output_key] == plain_scalar_value
    assert result[plain_scalar_input_output_key] == plain_scalar_input_value
    assert result[single_mat_output_key] == single_mat_id
    assert result[plural_mats_output_key] == plural_mat_ids
    assert result[unrendered_single_mat_output_key] == unrendered_single_mat_id
    assert result[unrendered_plural_mats_output_key] == unrendered_plural_mat_ids

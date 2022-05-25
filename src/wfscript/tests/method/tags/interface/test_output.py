from ....testing_tools.mocks import get_context_with_mock_domain
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.document_loader import load_yaml


class PlainScalar(ConstantNamespace):
    value = 'some unrendered scalar'
    output_key = 'plain_scalar_output'


class ScalarInput(ConstantNamespace):
    value = 'some_scalar_input'
    name = 'some_scalar_input_id'
    output_key = 'scalar_input_output'


class SingleMat(ConstantNamespace):
    id = 'bogus/system::1'
    name = 'single_mat_id'
    output_key = 'single_mat_output'


class PluralMats(ConstantNamespace):
    ids = ['bogus/system::2', 'bogus/system::3']
    name = 'list_of_mat_ids'
    output_key = 'plural_mats_output'


class UnrenderedSingleMat(ConstantNamespace):
    id = 'bogus/system::4'
    name = 'unrendered_single_mat_id'
    output_key = 'unrendered_single_mat_output'


class UnrenderedPluralMats(ConstantNamespace):
    ids = ['bogus/system::5', 'bogus/system::6']
    name = 'unrendered_list_of_mat_ids'
    output_key = 'unrendered_plural_mats_output'


def test_output_tag():
    context = get_context_with_mock_domain(
        input_data={
            ScalarInput.name: ScalarInput.value,
            SingleMat.name: SingleMat.id,
            UnrenderedSingleMat.name: UnrenderedSingleMat.id,
            PluralMats.name: PluralMats.ids,
            UnrenderedPluralMats.name: UnrenderedPluralMats.ids
        }
    )
    snippet = f'''
      - {TagName.Material} {SingleMat.name}
      - {TagName.Materials} {PluralMats.name}
      - {TagName.Material} {UnrenderedSingleMat.name}
      - {TagName.Materials} {UnrenderedPluralMats.name}

      - {TagName.OUTPUT}
        {PlainScalar.output_key}: {PlainScalar.value}
        {ScalarInput.output_key}: {TagName.Input} {ScalarInput.name}
        {SingleMat.output_key}: {TagName.Material} {SingleMat.name}
        {PluralMats.output_key}: {TagName.Materials} {PluralMats.name}
        {UnrenderedSingleMat.output_key}: {TagName.Material} {UnrenderedSingleMat.name}
        {UnrenderedPluralMats.output_key}: {TagName.Materials} {UnrenderedPluralMats.name}
    '''
    nodes = load_yaml(snippet)
    # render *some* materials to show prior rendering has no effect on output
    mat_nodes_to_render = nodes[:4]
    for to_render in mat_nodes_to_render:
        to_render.render(context)

    # render output and verify returned results
    output_node = nodes[4]
    result = output_node.render(context)
    assert result[PlainScalar.output_key] == PlainScalar.value
    assert result[ScalarInput.output_key] == ScalarInput.value
    assert result[SingleMat.output_key] == SingleMat.id
    assert result[PluralMats.output_key] == PluralMats.ids
    assert result[UnrenderedSingleMat.output_key] == UnrenderedSingleMat.id
    assert result[UnrenderedPluralMats.output_key] == UnrenderedPluralMats.ids

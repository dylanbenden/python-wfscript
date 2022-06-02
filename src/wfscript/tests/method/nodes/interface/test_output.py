from ....testing_tools.context import get_empty_context
from ....testing_tools.mocks import get_context_with_mocks
from ....testing_tools.nodes import Phase, ConfigShape, assert_unsupported, method_for_phase_and_shape, \
    render_for_phase_and_shape
from .....constants import ConstantNamespace
from .....constants.method import TagName
from .....method.loading import load_yaml


class PlainScalar(ConstantNamespace):
    value = 'some unrendered scalar'
    output_key = 'plain_scalar_output'


class ScalarInput(ConstantNamespace):
    value = 'scalar input value'
    name = 'scalar_input_name'
    output_key = 'scalar_input_output_key'


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


def test_output_binding_node():
    # Phase.OUTPUT, ConfigShape.DICT
    context = get_context_with_mocks(
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
        render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.SCALAR, to_render, context)

    # render output and verify returned results
    output_node = nodes[4]
    result = render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.DICT, output_node, context)
    assert result[PlainScalar.output_key] == PlainScalar.value
    assert result[ScalarInput.output_key] == ScalarInput.value
    assert result[SingleMat.output_key] == SingleMat.id
    assert result[PluralMats.output_key] == PluralMats.ids
    assert result[UnrenderedSingleMat.output_key] == UnrenderedSingleMat.id
    assert result[UnrenderedPluralMats.output_key] == UnrenderedPluralMats.ids


    # Phase.OUTPUT, ConfigShape.LIST
    # Render output at the end of a Method, but with a list shape
    class TestParams(ConstantNamespace):
        SCALAR_INPUT_VALUE = 'hello there!'
        STATE_TARGET_NAME = 'my_target'
        OUTPUT_KEY_NAME = 'my_output_key'
        STATE_VALUE = 'my value'

    node = load_yaml(
        f'''
          {TagName.OUTPUT}
            - {TestParams.SCALAR_INPUT_VALUE}
            - {TagName.State} {TestParams.STATE_TARGET_NAME}
        '''
    )
    context = get_empty_context(state={TestParams.STATE_TARGET_NAME: TestParams.STATE_VALUE})
    assert render_for_phase_and_shape(Phase.OUTPUT, ConfigShape.LIST, node, context) == [TestParams.SCALAR_INPUT_VALUE,
                                                                                         TestParams.STATE_VALUE]

    # Phase.EXECUTE, ConfigShape.LIST
    # Bind to output from an executor
    # Case: Store output in its entirety at the !State name indicated
    node = load_yaml(
        f'''
          {TagName.OUTPUT}
            - {TagName.State}
              {TestParams.STATE_TARGET_NAME}: {TagName.Output}
        '''
    )
    context = get_empty_context()
    context.output.update({TestParams.OUTPUT_KEY_NAME: TestParams.STATE_VALUE})
    render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert context.state[TestParams.STATE_TARGET_NAME] == {TestParams.OUTPUT_KEY_NAME: TestParams.STATE_VALUE}

    # Case: Store a particular attribute/item/key from !Output at the !State name indicated
    node = load_yaml(
        f'''
          {TagName.OUTPUT}
            - {TagName.State}
              {TestParams.STATE_TARGET_NAME}: {TagName.Output} {TestParams.OUTPUT_KEY_NAME}
        '''
    )
    render_for_phase_and_shape(Phase.EXECUTE, ConfigShape.LIST, node, context)
    assert context.state[TestParams.STATE_TARGET_NAME] == TestParams.STATE_VALUE

    unsupported = [
        (Phase.EXECUTE, ConfigShape.DICT),
        (Phase.EXECUTE, ConfigShape.SCALAR),
        (Phase.OUTPUT, ConfigShape.SCALAR),
    ]
    assert_unsupported(unsupported, output_node, context)

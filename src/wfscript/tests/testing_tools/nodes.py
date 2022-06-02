import pytest

from ...constants import ConstantNamespace


class Phase(ConstantNamespace):
    EXECUTE = 'execute'
    OUTPUT = 'output'


class ConfigShape(ConstantNamespace):
    DICT = 'dict'
    LIST = 'list'
    SCALAR = 'scalar'


method_name_for_phase_and_shape = {
    (Phase.EXECUTE, ConfigShape.DICT): 'execute_render_from_dict',
    (Phase.EXECUTE, ConfigShape.LIST): 'execute_render_from_list',
    (Phase.EXECUTE, ConfigShape.SCALAR): 'execute_render_from_scalar',
    (Phase.OUTPUT, ConfigShape.DICT): 'output_render_from_dict',
    (Phase.OUTPUT, ConfigShape.LIST): 'output_render_from_list',
    (Phase.OUTPUT, ConfigShape.SCALAR): 'output_render_from_scalar',
}


def method_for_phase_and_shape(phase, shape, node):
    return getattr(node, method_name_for_phase_and_shape[(phase, shape)])


def render_for_phase_and_shape(phase, shape, node, context):
    method = method_for_phase_and_shape(phase, shape, node)
    return method(context)


def assert_unsupported(phase_shape_pairs, node, context):
    for phase, shape in phase_shape_pairs:
        method_name = method_name_for_phase_and_shape[(phase, shape)]
        if hasattr(node, method_name):
            with pytest.raises(RuntimeError) as execinfo:
                getattr(node, method_name)(context)
            assert f"{node.tag_name} does not support " in str(execinfo)

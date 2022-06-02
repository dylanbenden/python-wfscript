from collections import defaultdict

from ...constants import ConstantNamespace
from ...method.nodes.base import WorkflowNode


class OutputType(ConstantNamespace):
    DATA_SOURCE = 'data_source'
    NODE = 'node'
    MATERIAL = 'material'
    DICT = 'dict'
    LIST = 'list'
    SCALAR = 'scalar'


def output_render(data, context):
    output_type = identify_output_type(data)
    if output_type == OutputType.DICT:
        return _output_render_dict(data, context)
    elif output_type == OutputType.LIST:
        return _output_render_list(data, context)
    elif output_type == OutputType.NODE:
        return data.output_render(context)
    else:
        return _output_render_scalar(data, context)


def execute_render(data, context):
    output_type = identify_output_type(data)
    if output_type == OutputType.DICT:
        return _execute_render_dict(data, context)
    elif output_type == OutputType.LIST:
        return _execute_render_list(data, context)
    elif output_type == OutputType.NODE:
        return data.execute_render(context)
    else:
        return _execute_render_scalar(data, context)


def identify_output_type(output):
    if isinstance(output, WorkflowNode):
        return OutputType.NODE
    elif isinstance(output, dict):
        return OutputType.DICT
    elif isinstance(output, list):
        return OutputType.LIST
    else:
        return OutputType.SCALAR


def group_dict_outputs(value):
    grouped_outputs = defaultdict(dict)
    for name_key, output in value.items():
        grouped_outputs[identify_output_type(output)][name_key] = output
    return grouped_outputs


def _output_render_dict(data, context):
    grouped_outputs = group_dict_outputs(data)
    return dict(
        {
            key: value.output_render(context)
            for key, value in grouped_outputs[OutputType.NODE].items()
        },
        **{
            key: _output_render_dict(value, context)
            for key, value in grouped_outputs[OutputType.DICT].items()
        },
        **{
            key: _output_render_list(value, context)
            for key, value in grouped_outputs[OutputType.LIST].items()
        },
        **{
            key: value
            for key, value in grouped_outputs[OutputType.SCALAR].items()
        }
    )

def _output_render_list(data, context):
    output = list()
    for item in data:
        output_type = identify_output_type(item)
        if output_type == OutputType.NODE:
            output.append(item.output_render(context))
        elif output_type == OutputType.DICT:
            output.append(_output_render_dict(item, context))
        elif output_type == OutputType.LIST:
            output.append(_output_render_list(item, context))
        else:
            output.append(_output_render_scalar(item, context))
    return output


def _output_render_scalar(data, context):
    if isinstance(data, WorkflowNode):
        return data.output_render(context)
    else:
        return data


def _execute_render_dict(data, context):
    grouped_outputs = group_dict_outputs(data)
    return dict(
        {
            key: value.execute_render(context)
            for key, value in grouped_outputs[OutputType.NODE].items()
        },
        **{
            key: _execute_render_dict(value, context)
            for key, value in grouped_outputs[OutputType.DICT].items()
        },
        **{
            key: _execute_render_list(value, context)
            for key, value in grouped_outputs[OutputType.LIST].items()
        },
        **{
            key: value
            for key, value in grouped_outputs[OutputType.SCALAR].items()
        }
    )


def _execute_render_list(data, context):
    output = list()
    for item in data:
        output_type = identify_output_type(item)
        if output_type == OutputType.NODE:
            output.append(item.execute_render(context))
        elif output_type == OutputType.DICT:
            output.append(_execute_render_dict(item, context))
        elif output_type == OutputType.LIST:
            output.append(_execute_render_list(item, context))
        else:
            output.append(_execute_render_scalar(item, context))
    return output


def _execute_render_scalar(data, context):
    if isinstance(data, WorkflowNode):
        return data.execute_render(context)
    else:
        return data

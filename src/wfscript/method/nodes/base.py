import yaml


class WorkflowNode(object):
    def __init__(self, loader, tag, value):
        self._loader = loader
        self._tag = tag
        self._value = value
        self._node_for_tag = None

    @classmethod
    def construct_value(cls, loader, node):
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        elif isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        else:
            raise RuntimeError(f'Unexpected node type: {node}')

    @property
    def tag(self):
        return self._tag

    @property
    def tag_name(self):
        return self.tag.tag_name

    @property
    def value(self):
        return self._value

    @property
    def node_for_tag(self):
        if not isinstance(self._value, list):
            import ipdb; ipdb.set_trace()
            pass
        if self._node_for_tag is None:
            self._node_for_tag = {
                node.tag: node
                for node in self._value
            }
        return self._node_for_tag


class ExecutionPhase(object):
    def execute_render_from_dict(self, context):
        raise RuntimeError(f'{self.tag_name} does not support dict-configured rendering during ExecutionPhase; '
                           f'Value: {self.value}')

    def execute_render_from_list(self, context):
        raise RuntimeError(f'{self.tag_name} does not support list-configured rendering during ExecutionPhase; '
                           f'Value: {self.value}')

    def execute_render_from_scalar(self, context):
        raise RuntimeError(f'{self.tag_name} does not support scalar-configured rendering during ExecutionPhase; '
                           f'Value: {self.value}')

    def execute_render(self, context):
        if isinstance(self.value, dict):
            return self.execute_render_from_dict(context)
        elif isinstance(self.value, list):
            return self.execute_render_from_list(context)
        else:
            return self.execute_render_from_scalar(context)


class OutputPhase(object):
    def output_render_from_dict(self, context):
        raise RuntimeError(f'{self.tag_name} does not support dict-configured rendering during OutputPhase; '
                           f'Value: {self.value}')

    def output_render_from_list(self, context):
        raise RuntimeError(f'{self.tag_name} does not support list-configured rendering during OutputPhase; '
                           f'Value: {self.value}')

    def output_render_from_scalar(self, context):
        raise RuntimeError(f'{self.tag_name} does not support scalar-configured rendering during OutputPhase; '
                           f'Value: {self.value}')

    def output_render(self, context):
        if isinstance(self.value, dict):
            return self.output_render_from_dict(context)
        elif isinstance(self.value, list):
            return self.output_render_from_list(context)
        else:
            return self.output_render_from_scalar(context)


class DualPhase(ExecutionPhase, OutputPhase):
    pass

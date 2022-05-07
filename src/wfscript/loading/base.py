import yaml


class YAMLConfiguredObject(object):
    def __init__(self, loader, tag, value):
        self._loader = loader
        self._tag = tag
        self._value = value

    @property
    def tag(self):
        return self._tag

    @property
    def value(self):
        return self._value

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

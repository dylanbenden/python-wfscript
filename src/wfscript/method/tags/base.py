import yaml


class YAMLConfigured(object):
    def __init__(self, loader, tag, value):
        self._loader = loader
        self._tag = tag
        self._value = value

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
    def value(self):
        return self._value

    def render_from_scalar(self, context, **kwargs):
        raise NotImplementedError(f'{self.tag} may not be rendered from scalar configuration {self.value}')

    def render_from_list(self, context, **kwargs):
        raise NotImplementedError(f'{self.tag} may not be rendered from array configuration {self.value}')

    def render_from_dict(self, context, **kwargs):
        raise NotImplementedError(f'{self.tag} may not be rendered from mapping configuration {self.value}')

    def render_from_tag(self, context, **kwargs):
        raise NotImplementedError(f'{self.tag} may not be rendered from tag configuration: {self.value.tag}')

    def render(self, context, **kwargs):
        if isinstance(self.value, dict):
            return self.render_from_dict(context, **kwargs)
        elif isinstance(self.value, list):
            return self.render_from_list(context, **kwargs)
        elif isinstance(self.value, YAMLConfigured):
            return self.render_from_tag(context, **kwargs)
        return self.render_from_scalar(context, **kwargs)

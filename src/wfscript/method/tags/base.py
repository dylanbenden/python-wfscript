import yaml


class YAMLConfigured(object):
    use_child_tags_as_labels = False
    label_child_tags = False


    def __init__(self, loader, tag, value):
        self._loader = loader
        self._tag = tag
        self._value = value

    @classmethod
    def handle_child_tags(cls, sequence):
        if cls.label_child_tags:
            return {
                node.tag: node
                for node in sequence
            }
        elif cls.use_child_tags_as_labels:
            return {
                node.tag: node.value
                for node in sequence
            }
        return sequence

    @classmethod
    def construct_value(cls, loader, node):
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node)
        elif isinstance(node, yaml.SequenceNode):
            sequence = loader.construct_sequence(node)
            if all(isinstance(item, YAMLConfigured) for item in sequence):
                sequence = cls.handle_child_tags(sequence)
            return sequence
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

    def render_for_output(self, context):
        return self.render(context)

import yaml

from . import node_for_tag


_loader = yaml.SafeLoader


def _object_constructor(loader, node):
    klass = node_for_tag[node.tag]
    return klass(loader, node.tag, klass.construct_value(loader, node))


# tag value of None means "for all unmatched tags"
_loader.add_constructor(None, _object_constructor)


def load_yaml(yaml_format_text):
    return yaml.load(yaml_format_text, Loader=_loader)


def load_method(yaml_format_text):
    return {
        node.tag_name: node
        for node in load_yaml(yaml_format_text)
    }
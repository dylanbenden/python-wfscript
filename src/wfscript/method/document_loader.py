import yaml

from . import constructor_for_tag
from .tags.base import YAMLConfigured

_loader = yaml.SafeLoader


def _object_constructor(loader, node):
    klass = constructor_for_tag.get(node.tag, YAMLConfigured)
    return klass(loader, node.tag, klass.construct_value(loader, node))


# tag value of None means "for all unmatched tags"
_loader.add_constructor(None, _object_constructor)


def load_yaml(yaml_format_text):
    return yaml.load(yaml_format_text, Loader=_loader)


def load_method(yaml_format_text):
    return {
        node.tag: node
        for node in load_yaml(yaml_format_text)
    }
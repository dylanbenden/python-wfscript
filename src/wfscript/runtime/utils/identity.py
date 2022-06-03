from ...constants.method import TagName
from ...constants.identity import IdentityDelimeter, DocumentStatus
from ...method.nodes.labels.base import LabelNode


def deconstruct_identity(identity):
    namespace, remainder = identity.split(IdentityDelimeter.NAMESPACE)
    if IdentityDelimeter.VERSION in remainder:
        name, version = remainder.split(IdentityDelimeter.VERSION)
    else:
        name = remainder
        version = DocumentStatus.PRODUCTION
    if version in DocumentStatus.values():
        version_or_status = TagName.status
    else:
        version_or_status = TagName.version
    return {
        TagName.namespace: namespace,
        TagName.name: name,
        version_or_status: version
    }


def construct_identity(meta_values):
    if TagName.version in meta_values:
        version_or_status = TagName.version
    else:
        version_or_status = TagName.status
    if all(isinstance(item, LabelNode) for item in meta_values.values()):
        return '{namespace}{namespace_delim}{method}{version_delim}{version}'.format(
            namespace=meta_values[TagName.namespace].value,
            namespace_delim=IdentityDelimeter.NAMESPACE,
            method=meta_values[TagName.name].value,
            version_delim=IdentityDelimeter.VERSION,
            version=str(meta_values[version_or_status].value),
        )
    else:
        return '{namespace}{namespace_delim}{method}{version_delim}{version}'.format(
            namespace=meta_values[TagName.namespace],
            namespace_delim=IdentityDelimeter.NAMESPACE,
            method=meta_values[TagName.name],
            version_delim=IdentityDelimeter.VERSION,
            version=str(meta_values[version_or_status]),
        )

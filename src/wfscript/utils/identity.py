from ..constants.method import TagName
from ..constants.identity import IdentityDelimeter, DocumentStatus


def deconstruct_identity(identity):
    namespace, remainder = identity.split(IdentityDelimeter.NAMESPACE)
    if IdentityDelimeter.VERSION in remainder:
        name, version = remainder.split(IdentityDelimeter.VERSION)
    else:
        name = remainder
        version = DocumentStatus.PRODUCTION
    if version in DocumentStatus.values():
        version_or_status = TagName.STATUS
    else:
        version_or_status = TagName.VERSION
    return {
        TagName.NAMESPACE: namespace,
        TagName.NAME: name,
        version_or_status: version
    }


def construct_identity(meta_values):
    if TagName.VERSION in meta_values:
        version = str(meta_values[TagName.VERSION])
    else:
        version = meta_values[TagName.STATUS]
    return '{namespace}{namespace_delim}{method}{version_delim}{version}'.format(
        namespace=meta_values[TagName.NAMESPACE],
        namespace_delim=IdentityDelimeter.NAMESPACE,
        method=meta_values[TagName.NAME],
        version_delim=IdentityDelimeter.VERSION,
        version=version,
    )

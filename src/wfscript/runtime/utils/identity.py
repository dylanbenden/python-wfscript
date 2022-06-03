from ...constants.method import TagName
from ...constants.identity import IdentityDelimeter, DocumentStatus


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
        version = str(meta_values[TagName.version])
    else:
        try:
            version = meta_values[TagName.status]
        except:
            import ipdb; ipdb.set_trace()
            pass
    return '{namespace}{namespace_delim}{method}{version_delim}{version}'.format(
        namespace=meta_values[TagName.namespace],
        namespace_delim=IdentityDelimeter.NAMESPACE,
        method=meta_values[TagName.name],
        version_delim=IdentityDelimeter.VERSION,
        version=version,
    )

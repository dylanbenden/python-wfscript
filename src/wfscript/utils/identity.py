from ..constants.loading import MetaSectionKey
from ..constants.identity import IdentityDelimeter


def deconstruct_identity(identity):
    domain, remainder = identity.split(IdentityDelimeter.NAMESPACE)
    name, version = remainder.split(IdentityDelimeter.VERSION)
    return {
        MetaSectionKey.NAMESPACE: domain,
        MetaSectionKey.NAME: name,
        MetaSectionKey.VERSION: version
    }


def construct_identity(meta_values):
    return '{domain}{domain_delim}{method}{version_delim}{version}'.format(
        domain=meta_values[MetaSectionKey.NAMESPACE],
        domain_delim=IdentityDelimeter.NAMESPACE,
        method=meta_values[MetaSectionKey.NAME],
        version_delim=IdentityDelimeter.VERSION,
        version=str(meta_values[MetaSectionKey.VERSION]),
    )

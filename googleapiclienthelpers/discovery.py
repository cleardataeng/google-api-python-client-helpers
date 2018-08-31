from googleapiclient import discovery

from positional import positional

__all__ = [
    'build_subresource',
]


@positional(2)
def build_subresource(servicePath,
                      version,
                      **kargs):
    """Construct a Resource for interacting with an API's subresources.

    Construct a Resource object for interacting with an API. The
    servicePath is a dot-delimited string.  The first element is the
    serviceName from the Discovery service.  Subsequent elements are the
    names of subresources accessed via the resulting client.  The
    version is the version of the serviceName from the Discovery
    service.

    Some example servicePaths:
      iam.roles
      iam.projects.serviceAccounts.keys
      cloudresourcemanager
      cloudresourcemanager.projects

    Args:
      servicePath: string, see above description.
      version: string, the version of the service.
      kargs: all other arguments are passed on to build

    Returns:
      A Resource object with methods for interacting with the service.

    """
    splits = servicePath.split('.')
    serviceName = splits[0]
    subresources = splits[1:]

    client = discovery.build(serviceName, version, **kargs)

    for subresource in subresources:
        subresource_fn = getattr(client, subresource)
        client = subresource_fn()

    return client

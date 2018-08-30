import tenacity

from .exceptions import is_retryable_exception

__all__ = [
    'add_binding',
    'get_policy',
    'get_role_bindings',
    'remove_binding',
]


def get_role_bindings(policy, role):
    '''Find the given role's binding from the given IAM policy.

    Given an IAM policy and a desired role, return the binding
    associated with that role.  If the role is not present in the
    policy, return None.

    Args:
      policy: list, the result of any getIamPolicy method.
      role: string, the role to pull from the policy.

    Returns:
      A list of dictionaries, or None if the role is not present.

    '''

    for binding in policy.get('bindings', ()):
        if binding['role'] == role:
            return binding

    return None


def _api_requires_empty_body(client):
    '''Does the given client's getIamPolicy require an empty body param?

    This function examines the given client to determine if its
    getIamPolicy method must be called with {} as the body.

    Args:
      client: Resource, any googleapiclient resource or subresource.

    Returns:
      bool, True if client.getIamPolicy requires {} in the body.

    '''

    desc = client._resourceDesc.get('methods', {})
    getIamPolicy = desc.get('getIamPolicy')
    if not getIamPolicy:
        raise ValueError('The provided client has no getIamPolicy method.')

    # collect names of any required params
    required = [k for k, v in getIamPolicy.get('parameters', {}).items()
                if v.get('required')]

    return 'body' in required


def get_policy(client, **kargs):
    '''Retrieve a policy with GET or POST, as required

    Some getIamPolicy methods are called with GET, and must have an
    empty body.  Other getIamPolicy methods are called with POST, and
    must have a non-empty body equal to {}.  This function provides a
    common interface to both.

    Args:
      client: Resource, any googleapiclient resource or subresource.
      **kargs: passed onto client.getIamPolicy

    Returns:
      The result of client.getIamPolicy(**kargs).execute()
    '''

    if _api_requires_empty_body(client) and 'body' not in kargs:
        kargs['body'] = {}

    return client.getIamPolicy(**kargs).execute()


@tenacity.retry(
    retry=tenacity.retry_if_result(is_retryable_exception),
    wait=tenacity.wait_random_exponential(multiplier=0.2, max=10),
    stop=tenacity.stop_after_attempt(3),
)
def add_binding(client, role, member, **kargs):
    '''Generic function to add an IAM binding to any GCP resource.

    This function provides a simple, generic way to add a member to a
    role for any resource.  The caller must supply a client that
    provides getIamPolicy and setIamPolicy methods.  It preserves
    the policy's etag to prevent concurrent updates.

    Args:
      client: Resource, any googleapiclient resource or subresource.
      role: string, name of the role to modify (e.g., roles/viewer).
      member: string, the member to add (e.g., user:email@domain.com,
        serviceAccount:wooo@yea.iam.gserviceaccount.com).
      **kargs: passed onto client's getIamPolicy and setIamPolicy.
        This must include parameter that identifies the resource whose
        policy will be modified.  The parameter varies; check the docs
        on client.getIamPolicy for details.

    Returns:
      the result of client.setIamPolicy

    '''
    policy = get_policy(client, **kargs)

    # if the policy is empty, create the bindings list
    if 'bindings' not in policy:
        policy['bindings'] = []

    # get the bindings for the role and create/add as required
    bindings = get_role_bindings(policy, role)

    if bindings:
        if member in bindings['members']:
            return              # already in the desired state

        bindings['members'].append(member)

    else:
        policy['bindings'].append({
            'role': role,
            'members': [member],
        })

    return client.setIamPolicy(body={'policy': policy}, **kargs).execute()


@tenacity.retry(
    retry=tenacity.retry_if_result(is_retryable_exception),
    wait=tenacity.wait_random_exponential(multiplier=0.2, max=10),
    stop=tenacity.stop_after_attempt(3),
)
def remove_binding(client, role, member, **kargs):
    '''Generic function to remove an IAM binding from any GCP resource.

    This function provides a simple, generic way to remove a member
    from a role for any resource.  The caller must supply a client
    that provides getIamPolicy and setIamPolicy methods.  It preserves
    the policy's etag to prevent concurrent updates.

    Args:
      client: Resource, any googleapiclient resource or subresource.
      role: string, name of the role to modify (e.g., roles/viewer).
      member: string, the member to add (e.g., user:email@domain.com,
        serviceAccount:wooo@yea.iam.gserviceaccount.com).
      **kargs: passed onto client's getIamPolicy and setIamPolicy.
        This must include parameter that identifies the resource whose
        policy will be modified.  The parameter varies; check the docs
        on client.getIamPolicy for details.

    Returns:
      the result of client.setIamPolicy

    '''
    policy = get_policy(client, **kargs)
    binding = get_role_bindings(policy, role)

    # if no binding was found, we're done
    if not binding:
        return

    try:
        binding.get('members', []).remove(member)
    except ValueError:
        return                  # no member to remove, we're done

    return client.setIamPolicy(body={'policy': policy}, **kargs).execute()

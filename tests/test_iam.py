import datetime
import os

from googleapiclienthelpers.discovery import build_subresource
import googleapiclienthelpers.iam
import pytest

project_id = os.getenv('GOOGLE_PROJECT')
remote_tests = os.getenv('REMOTE_TESTS')
test_time = datetime.datetime.utcnow().strftime('%s')


@pytest.fixture(scope='module',
                params=['pubsub', 'cloudresourcemanager'])
def scenario(request):
    '''Generate an iam test scenario

    A test scenario consists of the client to use and a resource to
    operate on.

    This generates scenarios for pubsub and cloudresourcemanager,
    since one requires GET for getIamPolicy and the other uses POST.

    '''

    if request.param == 'pubsub':
        client = build_subresource('pubsub.projects.topics', 'v1')

        topic = client.create(
            name='projects/%s/topics/gapich-test-%s' % (project_id, test_time,),
            body={},
        ).execute()

        kwargs = {'resource': topic['name']}
        yield (client, kwargs)

        client.delete(topic=topic['name']).execute()

    elif request.param == 'cloudresourcemanager':
        client = build_subresource('cloudresourcemanager.projects', 'v1beta1')

        kwargs = {'resource': project_id}
        yield (client, kwargs)


@pytest.fixture(scope='module')
def member():
    client = build_subresource('iam.projects.serviceAccounts', 'v1')
    svcacct = client.create(
        name='projects/%s' % project_id,
        body={'accountId': 'gapich-test-%s' % test_time},
    ).execute()

    yield 'serviceAccount:%s' % svcacct['email']

    client.delete(name=svcacct['name']).execute()


@pytest.mark.skipif(not remote_tests or not project_id,
                    reason='GOOGLE_PROJECT is unset or empty')
def test_iam_helpers(scenario, member):
    client, kwargs = scenario

    # add a new binding
    googleapiclienthelpers.iam.add_binding(
        client,
        'roles/viewer',
        member,
        **kwargs
    )

    # prepare to call getIamPolicy, making up for nonuniform IAM APIs
    if googleapiclienthelpers.iam._api_requires_empty_body(client):
        kwargs['body'] = {}

    # check that the member was added
    policy = client.getIamPolicy(**kwargs).execute()
    binding = googleapiclienthelpers.iam.get_role_bindings(
        policy,
        'roles/viewer',
    )
    assert member in binding.get('members', ())

    # remove the binding
    googleapiclienthelpers.iam.remove_binding(
        client,
        'roles/viewer',
        member,
        **kwargs
    )

    # check that the member was removed
    policy = client.getIamPolicy(**kwargs).execute()
    binding = googleapiclienthelpers.iam.get_role_bindings(
        policy,
        'roles/viewer',
    )
    if binding:
        assert member not in binding.get('members', ())

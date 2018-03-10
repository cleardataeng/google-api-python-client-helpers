Examples
========

build_subresource
-----------------

Some of the Google APIs have multiple levels of subresources.  For
example, to manage a GCP service account's customer managed keys, you
can use :func:`googleapiclienthelpers.discovery.build_subresource`
like this:

.. code-block:: python

   from googleapiclienthelpers.discovery import build_subresource
   
   client = build_subresource('iam.projects.serviceAccounts.keys', 'v1')


IAM bindings
------------

Many GCP resources provide ``getIamPolicy`` and ``setIamPolicy``
methods to modify permissions.  To update a permission, you must fetch
the policy, modify it, and set the new policy.  A simpler, uniform
interface is provided by
:func:`googleapiclienthelpers.iam.add_binding` and
:func:`googleapiclienthelpers.iam.remove_binding`.  They make simple
policy changes straightfoward:

.. code-block:: python

   from googleapiclienthelpers.discovery import build_subresource
   import googleapiclienthelpers.iam

   client = build_subresource('cloudresourcemanager.projects', 'v1beta1')
   googleapiclienthelpers.iam.add_binding(
       client,
       'roles/viewer',
       'user:my.user@example.com',
       resource='my-cool-project',
   )


.. code-block:: python

   from googleapiclienthelpers.discovery import build_subresource
   import googleapiclienthelpers.iam

   client = build_subresource('pubsub.projects.topics', 'v1')

   googleapiclienthelpers.iam.remove_binding(
       client,
       'roles/viewer',
       'serviceAccount:my_svc_acct@my-cool-project.iam.gserviceaccount.com',
       topic='projects/my-cool-project/topics/interesting-stuff',
   )

The bindings you request must meet any underlying constraints on
``setIamPolicy`` calls.  For example, the API cannot be used to add a
user as a project owner.


Waiter
------

Sometimes you need to block for an operation to complete.  The
:class:`.Waiter` makes this easy to do in a generic way.  For instance,
suppose you want to launch a Deployment Manager deployment and wait
until it is complete:

.. code-block:: python

   from googleapiclienthelpers.discovery import build_subresource
   from googleapiclienthelpers.waiter import Waiter

   deployments = build_subresource('deploymentmanager.deployments', 'v2')
   r = deployments.insert(project='example', body={
       'name': 'example',
       'target': {...},
   }).execute()

   waiter = Waiter(deployments.get, project='example', deployment='example')
   waiter.wait('status', 'DONE')


To create a :class:`.Waiter`, you must
supply:

#. The resource method you want to wait on.
#. All positional and keyword arguments required to invoke it.

Then, call the :meth:`.wait()` method to start the process.  The first
argument is the response key that the waiter will look for.  The
second argument is the status it should wait for.

By default, this will poll the resource once every two seconds for a
max of 60 retries.  These values can be overridden.

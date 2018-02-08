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

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

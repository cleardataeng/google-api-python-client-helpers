google-api-python-client-helpers
================================

This library collects helpers that make google-api-python-client a bit
nicer to use.

|pypi| |travis| |versions| |docs|

Test suite
----------

The ``tests`` directory contains some tests.  By default, only local
tests will be run.  To test all offline scenarios::

  $ tox

The integration tests require GCP access.  It is suggested to use a
dedicated lab/testing project for this purpose.  The integration tests
currently:

  * create & delete service accounts
  * add, fetch, & remove project members
  * create, delete, and modify Pub/Sub topics

It is recommended that a dedicated test/lab project be used for the
remote tests.  To enable them, supply two environment variables:

  * set ``REMOTE_TESTS`` to any non-empty value.
  * set ``GOOGLE_PROJECT`` to the project ID of your test project.

The application default credentials must have appropriate access to
this project.  For example::

  $ REMOTE_TESTS=1 GOOGLE_PROJECT=my-test-project tox


License
-------

This library is Apache 2.0: details `here <https://github.com/cleardataeng/google-api-python-client-helpers/blob/master/LICENSE>`_.

.. |pypi| image:: https://img.shields.io/pypi/v/google-api-python-client-helpers.svg
   :target: https://pypi.org/project/google-api-python-client-helpers/
.. |travis| image:: https://travis-ci.org/cleardataeng/google-api-python-client-helpers.svg?branch=master
   :target: https://travis-ci.org/cleardataeng/google-api-python-client-helpers
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-api-python-client-helpers.svg
   :target: https://pypi.org/project/google-api-python-client-helpers/
.. |docs| image:: https://img.shields.io/readthedocs/google-api-python-client-helpers.svg
   :target: https://google-api-python-client-helpers.readthedocs.io/

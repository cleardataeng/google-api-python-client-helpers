# Copyright 2014 Google Inc. All Rights Reserved.
# Copyright 2018 Ross Vandegrift
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup script for Google API Python client helper library.

Also installs included versions of third party libraries, if those libraries
are not already installed.
"""
from __future__ import print_function

from setuptools import setup
from googleapiclienthelpers import __version__ as version

setup(
    name="google-api-python-client-helpers",
    version=version,
    description="Helpers for Google API Client Library for Python",
    long_description='The Google API Client for Python helper library provides convenience functions that make the base library a little nicer.',
    author="Ross  Vandegrift",
    url="http://github.com/cleardataeng/google-api-python-client-helpers/",
    install_requires=[
        'google-api-python-client',
        'httplib2',
        'positional',
        'tenacity',
    ],
    packages=[
        'googleapiclienthelpers',
    ],
    package_data={},
    license="Apache 2.0",
    keywords="google api client",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
)

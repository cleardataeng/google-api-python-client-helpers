import os
import unittest

from googleapiclient.discovery import Resource
from googleapiclient.http import HttpMock
from googleapiclienthelpers.discovery import build_subresource


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def datafile(filename):
    return os.path.join(DATA_DIR, filename)


class DiscoverySubresources(unittest.TestCase):

    def test_build_valid_subresources(self):
        self.http = HttpMock(datafile('iam.json'), {'status': '200'})

        client = build_subresource('iam.roles', 'v1', http=self.http)
        self.assertTrue(client)
        self.assertIsInstance(client, Resource)

        client = build_subresource('iam.projects.roles', 'v1', http=self.http)
        self.assertTrue(client)
        self.assertIsInstance(client, Resource)

    def test_build_nonexistent_subresource(self):
        self.http = HttpMock(datafile('iam.json'), {'status': '200'})

        with self.assertRaises(AttributeError):
            build_subresource('iam.bogus_subresource', 'v1', http=self.http)

from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentSSLCert(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.ssl_cert = SSLCertFactory(node=self.node)

    def test_first_ssl_cert_is_current(self):
        curr = CurrentSSLCert.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.ssl_cert, self.ssl_cert.ssl_cert)
    
    def test_replacement_ssl_cert_is_current(self):
        new_ssl_cert = SSLCertFactory(node=self.node)
        _ = SSLCertChangeFactory(node=self.node, old_ssl_cert=self.ssl_cert, new_ssl_cert=new_ssl_cert, user=self.user)

        ssl_certs = SSLCert.objects.filter(node=self.node)
        self.assertEqual(len(ssl_certs), 2)

        curr = CurrentSSLCert.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.ssl_cert, new_ssl_cert.ssl_cert)

from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentTelephonyIDs(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.tele = TelephonyIDsFactory(node=self.node)

    def test_first_tele_is_current(self):
        curr = CurrentTelephonyIDs.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.modem_imei, self.tele.modem_imei)
    
    def test_replacement_tele_is_current(self):
        new_tele = TelephonyIDsFactory(node=self.node)
        _ = TelephonyIDsChangeFactory(node=self.node, old_telephony_id=self.tele, new_telephony_id=new_tele, user=self.user)

        descs = TelephonyIDs.objects.filter(node=self.node)
        self.assertEqual(len(descs), 2)

        curr = CurrentTelephonyIDs.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.modem_imei, new_tele.modem_imei)

from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentSoftware(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.software = SoftwareFactory(node=self.node)

    def test_first_software_is_current(self):
        curr = CurrentSoftware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.software, self.software.software)
    
    def test_replacement_software_is_current(self):
        new_software = SoftwareFactory(node=self.node)
        _ = SoftwareChangeFactory(node=self.node, old_software=self.software, new_software=new_software, user=self.user)

        sfwrs = Software.objects.filter(node=self.node)
        self.assertEqual(len(sfwrs), 2)

        curr = CurrentSoftware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.software, new_software.software)

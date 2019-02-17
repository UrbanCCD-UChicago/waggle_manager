from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentDescription(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.desc = DescriptionFactory(node=self.node)

    def test_first_desc_is_current(self):
        curr = CurrentDescription.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.description, self.desc.description)
    
    def test_replacement_desc_is_current(self):
        new_desc = DescriptionFactory(node=self.node)
        _ = DescriptionChangeFactory(node=self.node, old_description=self.desc, new_description=new_desc, user=self.user)

        descs = Description.objects.filter(node=self.node)
        self.assertEqual(len(descs), 2)

        curr = CurrentDescription.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.description, new_desc.description)

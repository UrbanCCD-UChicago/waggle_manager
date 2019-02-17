from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentLocation(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.loc = LocationFactory(node=self.node)

    def test_first_loc_is_current(self):
        curr = CurrentLocation.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.location, self.loc.location)
    
    def test_replacement_loc_is_current(self):
        new_loc = LocationFactory(node=self.node)
        _ = LocationChangeFactory(node=self.node, old_location=self.loc, new_location=new_loc, user=self.user)

        descs = Location.objects.filter(node=self.node)
        self.assertEqual(len(descs), 2)

        curr = CurrentLocation.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.location, new_loc.location)

from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentHardware(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.hardware = HardwareFactory(node=self.node)

    def test_first_hardware_is_current(self):
        curr = CurrentHardware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.instance, self.hardware.instance)
    
    def test_replacement_hardware_is_current(self):
        new_hardware = HardwareFactory(node=self.node)
        _ = HardwareChangeFactory(node=self.node, old_instance=self.hardware, new_instance=new_hardware, user=self.user)

        hardwares = Hardware.objects.filter(node=self.node)
        self.assertEqual(len(hardwares), 2)

        curr = CurrentHardware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.instance, new_hardware.instance)
    
    def test_removed_without_replacement(self):
        _ = HardwareChangeFactory(node=self.node, old_instance=self.hardware, new_instance=None, removed_without_replacement=True, user=self.user)

        hardwares = Hardware.objects.filter(node=self.node)
        self.assertEqual(len(hardwares), 1)

        curr = CurrentHardware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 0)

    def test_nodes_have_multiple_pieces_of_hardware(self):
        _ = HardwareFactory(node=self.node)
        _ = HardwareFactory(node=self.node)
        _ = HardwareFactory(node=self.node)

        curr = CurrentHardware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 4)

        new_hardware = HardwareFactory(node=self.node)
        _ = HardwareChangeFactory(node=self.node, old_instance=self.hardware, new_instance=new_hardware, user=self.user)

        curr = CurrentHardware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 4)
    
    def test_new_hardware_can_replace_multiple_old_hardware(self):
        hdw2 = HardwareFactory(node=self.node)

        curr = CurrentHardware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 2)

        new_hardware = HardwareFactory(node=self.node)
        _ = HardwareChangeFactory(node=self.node, old_instance=self.hardware, new_instance=new_hardware, user=self.user)
        _ = HardwareChangeFactory(node=self.node, old_instance=hdw2, new_instance=new_hardware, user=self.user)

        curr = CurrentHardware.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

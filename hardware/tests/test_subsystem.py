from django.test import TestCase

from ..factories import *
from ..models import *


User = get_user_model()


class TestCurrentCalibration(TestCase):

    def setUp(self):
        self.comp1 = ComponentFactory()
        self.comp2 = ComponentFactory()
        self.comp3 = ComponentFactory()
    
    def test_normal_assembly_is_ok(self):
        Subsystem.objects.create(parent=self.comp1, child=self.comp2, child_quantity=1)
        Subsystem.objects.create(parent=self.comp1, child=self.comp3, child_quantity=1)
    
    def test_cycle_throws_error(self):
        Subsystem.objects.create(parent=self.comp1, child=self.comp2, child_quantity=1)
        Subsystem.objects.create(parent=self.comp2, child=self.comp3, child_quantity=1)
        
        with self.assertRaises(Exception):
            Subsystem.objects.create(parent=self.comp3, child=self.comp1, child_quantity=1)

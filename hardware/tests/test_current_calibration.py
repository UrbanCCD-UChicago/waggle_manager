from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentCalibration(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.comp = ComponentFactory()
        self.inst = InstanceFactory(component=self.comp)
        self.calib = CalibrationFactory(instance=self.inst)

    def test_first_calib_is_current(self):
        curr = CurrentCalibration.objects.filter(instance=self.inst)
        self.assertEqual(len(curr), 1)
        
        curr = curr[0]
        self.assertEqual(curr.value, self.calib.value)

    def test_replacement_calib_is_current(self):
        new_calib = CalibrationFactory(instance=self.inst)
        _ = CalibrationChangeFactory(instance=self.inst, old_calibration=self.calib, new_calibration=new_calib, user=self.user)

        calibs = Calibration.objects.filter(instance=self.inst)
        self.assertEqual(len(calibs), 2)

        curr = CurrentCalibration.objects.filter(instance=self.inst)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.value, new_calib.value)

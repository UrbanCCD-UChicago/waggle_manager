from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentSSHConfig(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.config = SSHConfigFactory(node=self.node)

    def test_first_desc_is_current(self):
        curr = CurrentSSHConfig.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.key, self.config.key)
    
    def test_replacement_desc_is_current(self):
        new_config = SSHConfigFactory(node=self.node)
        _ = SSHConfigChangeFactory(node=self.node, old_ssh_config=self.config, new_ssh_config=new_config, user=self.user)

        descs = SSHConfig.objects.filter(node=self.node)
        self.assertEqual(len(descs), 2)

        curr = CurrentSSHConfig.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.key, new_config.key)

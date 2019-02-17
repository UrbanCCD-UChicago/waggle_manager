from django.test import TestCase

from ..factories import *
from ..models import *


class TestCurrentState(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.node = NodeFactory()
        self.state = StateFactory(node=self.node)

    def test_first_state_is_current(self):
        curr = CurrentState.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.state, self.state.state)
    
    def test_replacement_state_is_current(self):
        new_state = StateFactory(node=self.node)
        _ = StateChangeFactory(node=self.node, old_state=self.state, new_state=new_state, user=self.user)

        states = State.objects.filter(node=self.node)
        self.assertEqual(len(states), 2)

        curr = CurrentState.objects.filter(node=self.node)
        self.assertEqual(len(curr), 1)

        curr = curr[0]
        self.assertEqual(curr.state, new_state.state)

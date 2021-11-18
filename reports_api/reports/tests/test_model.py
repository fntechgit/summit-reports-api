from django.test import TestCase
from ..models import Summit


class TestModels(TestCase):

    def test_get_summit_order_extra_questions(self):
        summit = Summit.objects.get(pk=4)
        self.assertTrue(summit is not None)

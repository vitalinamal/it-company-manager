from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Position


class PositionViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            position=self.position,
        )
        self.client.force_login(self.user)

        self.position1 = Position.objects.create(name="Developer")
        self.position2 = Position.objects.create(name="Manager")

    def test_position_list_view(self):
        response = self.client.get(reverse("tasks:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_list.html")
        self.assertContains(response, self.position1.name)
        self.assertContains(response, self.position2.name)

    def test_position_list_view_with_search(self):
        response = self.client.get(reverse("tasks:position-list"), {"name": "Dev"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position1.name)
        self.assertNotContains(response, self.position2.name)

    def test_position_create_view(self):
        response = self.client.get(reverse("tasks:position-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/generic_form.html")

        data = {"name": "Tester"}
        response = self.client.post(reverse("tasks:position-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Position.objects.filter(name="Tester").exists())

    def test_position_detail_view(self):
        response = self.client.get(
            reverse("tasks:position-detail", args=[self.position1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_detail.html")
        self.assertContains(response, self.position1.name)

    def test_position_delete_view(self):
        response = self.client.get(
            reverse("tasks:position-delete", args=[self.position1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/confirm_delete.html")

        response = self.client.post(
            reverse("tasks:position-delete", args=[self.position1.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(id=self.position1.id).exists())

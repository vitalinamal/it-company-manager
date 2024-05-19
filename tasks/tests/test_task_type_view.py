from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import TaskType, Position


class TaskTypeViewsTest(TestCase):
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

        self.task_type1 = TaskType.objects.create(name="Bug")
        self.task_type2 = TaskType.objects.create(name="Feature")

    def test_task_type_list_view(self):
        response = self.client.get(reverse("tasks:task-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_type_list.html")
        self.assertContains(response, self.task_type1.name)
        self.assertContains(response, self.task_type2.name)

    def test_task_type_list_view_with_search(self):
        response = self.client.get(reverse("tasks:task-type-list"), {"name": "Bug"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_type1.name)
        self.assertNotContains(response, self.task_type2.name)

    def test_task_type_create_view(self):
        response = self.client.get(reverse("tasks:task-type-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/generic_form.html")

        data = {"name": "Improvement"}
        response = self.client.post(reverse("tasks:task-type-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Improvement").exists())

    def test_task_type_detail_view(self):
        response = self.client.get(
            reverse("tasks:task-type-detail", args=[self.task_type1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_type_detail.html")
        self.assertContains(response, self.task_type1.name)

    def test_task_type_delete_view(self):
        response = self.client.get(
            reverse("tasks:task-type-delete", args=[self.task_type1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/confirm_delete.html")

        response = self.client.post(
            reverse("tasks:task-type-delete", args=[self.task_type1.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(id=self.task_type1.id).exists())

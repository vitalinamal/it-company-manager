from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskType, Worker, Position


class TaskViewsTest(TestCase):
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

        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = Worker.objects.create_user(
            username="workeruser",
            password="workerpassword",
            email="worker@example.com",
            position=self.position,
        )
        self.task1 = Task.objects.create(
            name="Fix issue",
            description="Fix the reported issue",
            deadline=timezone.now(),
            task_type=self.task_type,
            is_completed=False,
        )
        self.task2 = Task.objects.create(
            name="Develop feature",
            description="Develop the new feature",
            deadline=timezone.now(),
            task_type=self.task_type,
            is_completed=False,
        )

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)

    def test_task_list_view_with_search(self):
        response = self.client.get(reverse("tasks:task-list"), {"name": "Fix"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_task_create_view(self):
        response = self.client.get(reverse("tasks:task-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/generic_form.html")

        data = {
            "name": "Test task",
            "description": "This is a test task",
            "deadline": timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
            "priority": "Medium",
            "is_completed": False,
        }
        response = self.client.post(reverse("tasks:task-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Test task").exists())

    def test_task_detail_view(self):
        response = self.client.get(reverse("tasks:task-detail", args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertContains(response, self.task1.name)

    def test_task_update_view(self):
        response = self.client.get(reverse("tasks:task-update", args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/generic_form.html")

        data = {
            "name": "Updated task",
            "description": "This task has been updated",
            "deadline": timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
            "priority": "Medium",
            "is_completed": False,
        }
        response = self.client.post(
            reverse("tasks:task-update", args=[self.task1.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, "Updated task")

    def test_task_delete_view(self):
        response = self.client.get(reverse("tasks:task-delete", args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/confirm_delete.html")

        response = self.client.post(reverse("tasks:task-delete", args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

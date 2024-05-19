from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Worker, Position, Task, TaskType
from django.utils import timezone


class WorkerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            position=self.position,
        )
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser",
            password="superpassword",
            email="super@example.com",
            position=self.position,
        )
        self.client.force_login(self.user)

        self.worker1 = Worker.objects.create_user(
            username="worker1",
            password="workerpassword1",
            email="worker1@example.com",
            position=self.position,
        )
        self.worker2 = Worker.objects.create_user(
            username="worker2",
            password="workerpassword2",
            email="worker2@example.com",
            position=self.position,
        )

    def test_worker_list_view(self):
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_list.html")
        self.assertContains(response, self.worker1.username)
        self.assertContains(response, self.worker2.username)

    def test_worker_list_view_with_search(self):
        response = self.client.get(
            reverse("tasks:worker-list"), {"username": "worker1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker1.username)
        self.assertNotContains(response, self.worker2.username)

    def test_worker_detail_view(self):
        response = self.client.get(
            reverse("tasks:worker-detail", args=[self.worker1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_detail.html")
        self.assertContains(response, self.worker1.username)

    def test_worker_create_view(self):
        self.client.logout()
        response = self.client.get(reverse("tasks:worker-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_form.html")

        data = {
            "username": "newworker",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "first_name": "New",
            "last_name": "Worker",
            "email": "newworker@example.com",
            "position": self.position.id,
        }
        response = self.client.post(reverse("tasks:worker-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Worker.objects.filter(username="newworker").exists())

    def test_worker_update_view(self):
        self.client.force_login(self.worker1)
        response = self.client.get(
            reverse("tasks:worker-update", args=[self.worker1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/generic_form.html")

        data = {
            "username": "updatedworker",
            "first_name": "Updated",
            "last_name": "Worker",
            "email": "updatedworker@example.com",
            "position": self.position.id,
        }
        response = self.client.post(
            reverse("tasks:worker-update", args=[self.worker1.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.worker1.refresh_from_db()
        self.assertEqual(self.worker1.username, "updatedworker")

    def test_worker_delete_view(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("tasks:worker-delete", args=[self.worker1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/confirm_delete.html")

        response = self.client.post(
            reverse("tasks:worker-delete", args=[self.worker1.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Worker.objects.filter(id=self.worker1.id).exists())

    def test_upload_avatar_view(self):
        self.client.force_login(self.worker1)
        response = self.client.get(
            reverse("tasks:avatar-upload", args=[self.worker1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/upload_avatar.html")

        with open("static/images/user.jpg", "rb") as avatar:
            response = self.client.post(
                reverse("tasks:avatar-upload", args=[self.worker1.id]),
                {"avatar": avatar},
            )
            self.assertEqual(response.status_code, 302)
            self.worker1.refresh_from_db()
            self.assertTrue(self.worker1.avatar)

    def test_assign_or_remove_worker_view(self):
        task_type = TaskType.objects.create(name="Feature")
        task = Task.objects.create(
            name="Develop feature",
            description="Develop the new feature",
            deadline=timezone.now(),
            task_type=task_type,
            is_completed=False,
        )
        self.client.force_login(self.worker1)

        response = self.client.post(
            reverse("tasks:worker-assign-remove", args=[task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(task.assignees.filter(id=self.worker1.id).exists())

        response = self.client.post(
            reverse("tasks:worker-assign-remove", args=[task.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(task.assignees.filter(id=self.worker1.id).exists())

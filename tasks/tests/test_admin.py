from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from tasks.models import TaskType, Position, Worker, Task


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = Worker.objects.create_superuser(
            username="adminuser",
            password="password123",
            email="admin@example.com",
            position=Position.objects.create(name="Admin"),
        )
        self.client.force_login(self.admin_user)

        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Fix issue",
            description="Fix the reported issue",
            deadline=timezone.now(),
            task_type=self.task_type,
            is_completed=False,
        )

    def test_worker_listed(self):
        url = reverse("admin:tasks_worker_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.worker.username)
        self.assertContains(res, self.worker.position.name)

    def test_worker_change_page(self):
        url = reverse("admin:tasks_worker_change", args=[self.worker.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_worker_add_page(self):
        url = reverse("admin:tasks_worker_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

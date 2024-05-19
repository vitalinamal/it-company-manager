from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskType, Position, Commentary
from django.utils import timezone


class CommentViewsTest(TestCase):
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
        self.task = Task.objects.create(
            name="Fix issue",
            description="Fix the reported issue",
            deadline=timezone.now(),
            task_type=self.task_type,
            is_completed=False,
        )
        self.comment1 = Commentary.objects.create(
            content="First comment",
            user=self.user,
            task=self.task,
            created_time=timezone.now(),
        )
        self.comment2 = Commentary.objects.create(
            content="Second comment",
            user=self.user,
            task=self.task,
            created_time=timezone.now(),
        )

    def test_comment_list_view(self):
        response = self.client.get(reverse("tasks:comment-list", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/comment_list.html")
        self.assertContains(response, self.comment1.content)
        self.assertContains(response, self.comment2.content)
        self.assertContains(response, self.task.name)

    def test_comment_list_view_post_comment(self):
        response = self.client.post(
            reverse("tasks:comment-list", args=[self.task.id]),
            {"content": "New comment"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Commentary.objects.filter(content="New comment").exists())

    def test_delete_comment(self):
        response = self.client.post(
            reverse("tasks:comment-delete", args=[self.comment1.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Commentary.objects.filter(id=self.comment1.id).exists())

    def test_delete_comment_not_authorized(self):
        another_user = get_user_model().objects.create_user(
            username="anotheruser",
            password="anotherpassword",
            email="another@example.com",
            position=self.position,
        )
        self.client.force_login(another_user)

        response = self.client.post(
            reverse("tasks:comment-delete", args=[self.comment1.id])
        )
        self.assertEqual(response.status_code, 403)

        self.assertTrue(Commentary.objects.filter(id=self.comment1.id).exists())

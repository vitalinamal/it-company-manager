from django.test import TestCase
from django.utils import timezone
from tasks.forms import (
    WorkerCreateForm,
    AvatarForm,
    WorkerUpdateForm,
    TaskTypeCreateForm,
    TaskCreateForm,
    PositionCreateForm,
    WorkerSearchForm,
    PositionSearchForm,
    TaskSearchForm,
    TaskTypeSearchForm,
    CommentaryForm,
    CustomAuthenticationForm,
)
from tasks.models import Worker, Position, TaskType


class FormTests(TestCase):
    def setUp(self):
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

    def test_worker_create_form_valid_data(self):
        form_data = {
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@example.com",
            "position": self.position.id,
        }
        form = WorkerCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_worker_create_form_invalid_data(self):
        form = WorkerCreateForm(data={})
        self.assertFalse(form.is_valid())

    def test_avatar_form_empty(self):
        form = AvatarForm(data={})
        self.assertTrue(form.is_valid())

    def test_worker_update_form_valid_data(self):
        form = WorkerUpdateForm(
            instance=self.worker,
            data={
                "username": "testuser",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "position": self.position.id,
            },
        )
        self.assertTrue(form.is_valid())

    def test_task_type_create_form_valid_data(self):
        form = TaskTypeCreateForm(data={"name": "Bug"})
        self.assertTrue(form.is_valid())

    def test_task_type_create_form_invalid_data(self):
        form = TaskTypeCreateForm(data={})
        self.assertFalse(form.is_valid())

    def test_task_create_form_valid_data(self):
        form_data = {
            "name": "Fix issue",
            "description": "Fix the reported issue",
            "deadline": timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
            "priority": "High",
            "is_completed": False,
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_task_create_form_invalid_data(self):
        form = TaskCreateForm(data={})
        self.assertFalse(form.is_valid())

    def test_position_create_form_valid_data(self):
        form = PositionCreateForm(data={"name": "Manager"})
        self.assertTrue(form.is_valid())

    def test_position_create_form_invalid_data(self):
        form = PositionCreateForm(data={})
        self.assertFalse(form.is_valid())

    def test_worker_search_form_valid_data(self):
        form = WorkerSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())

    def test_worker_search_form_empty_data(self):
        form = WorkerSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_position_search_form_valid_data(self):
        form = PositionSearchForm(data={"name": "Developer"})
        self.assertTrue(form.is_valid())

    def test_position_search_form_empty_data(self):
        form = PositionSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_task_search_form_valid_data(self):
        form = TaskSearchForm(data={"name": "Fix issue"})
        self.assertTrue(form.is_valid())

    def test_task_search_form_empty_data(self):
        form = TaskSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_task_type_search_form_valid_data(self):
        form = TaskTypeSearchForm(data={"name": "Bug"})
        self.assertTrue(form.is_valid())

    def test_task_type_search_form_empty_data(self):
        form = TaskTypeSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_commentary_form_valid_data(self):
        form = CommentaryForm(data={"content": "This is a comment."})
        self.assertTrue(form.is_valid())

    def test_commentary_form_empty_data(self):
        form = CommentaryForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_authentication_form_valid_data(self):
        form = CustomAuthenticationForm(
            data={
                "username": "testuser",
                "password": "testpassword",
                "remember_me": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_authentication_form_empty_data(self):
        form = CustomAuthenticationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)

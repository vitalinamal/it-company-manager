from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="workers", null=False
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.username}"


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="Medium"
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tasks"
    )

    class Meta:
        ordering = ["name", "-deadline"]

    def __str__(self):
        return f"{self.name}"


class Commentary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commentaries"
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="commentaries")
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.user} {self.task} {self.created_time}"

from django.urls import path

from tasks.views import (
    index,
    PositionListView,
    PositionFormatCreateView,
    PositionDetailView,
    PositionFormatDeleteView,
    TaskListView,
    TaskFormatCreateView,
    TaskDetailView,
    TaskFormatDeleteView,
    TaskFormatUpdateView,
    WorkerListView,
    WorkerDetailView,
    WorkerFormatCreateView,
    WorkerFormatUpdateView,
    WorkerFormatDeleteView,
    TaskTypeListView,
    TaskTypeDetailView,
    TaskTypeFormatCreateView,
    TaskTypeFormatDeleteView,
    AssignOrRemoveWorkerView,
    CommentListView,
    upload_avatar,
    delete_comment,
    CustomLoginView,
)

urlpatterns = [
    path("welcome/", index, name="welcome"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/", PositionFormatCreateView.as_view(), name="position-create"
    ),
    path("positions/<int:pk>", PositionDetailView.as_view(), name="position-detail"),
    path(
        "positions/<int:pk>/delete/",
        PositionFormatDeleteView.as_view(),
        name="position-delete",
    ),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task-types/create/",
        TaskTypeFormatCreateView.as_view(),
        name="task-type-create",
    ),
    path("task-types/<int:pk>", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path(
        "task-types/<int:pk>/delete/",
        TaskTypeFormatDeleteView.as_view(),
        name="task-type-delete",
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskFormatCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskFormatUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskFormatDeleteView.as_view(), name="task-delete"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/avatar/", upload_avatar, name="avatar-upload"),
    path("workers/create/", WorkerFormatCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update/",
        WorkerFormatUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerFormatDeleteView.as_view(),
        name="worker-delete",
    ),
    path(
        "tasks/<int:pk>/assign-remove/",
        AssignOrRemoveWorkerView.as_view(),
        name="worker-assign-remove",
    ),
    path("tasks/<int:pk>/comments/", CommentListView.as_view(), name="comment-list"),
    path("comment/delete/<int:pk>/", delete_comment, name="comment-delete"),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
]

app_name = "tasks"

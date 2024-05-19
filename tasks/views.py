from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import (
    WorkerCreateForm,
    CommentaryForm,
    AvatarForm,
    WorkerUpdateForm,
    WorkerSearchForm,
    TaskTypeSearchForm,
    TaskSearchForm,
    PositionSearchForm,
    TaskCreateForm,
    TaskTypeCreateForm,
    PositionCreateForm,
    CustomAuthenticationForm,
)
from tasks.models import Position, TaskType, Task, Worker, Commentary


def index(request):
    return render(request, "tasks/welcome.html")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "tasks/position_list.html"
    paginate_by = 5
    queryset = Position.objects.annotate(worker_count=Count("workers")).order_by("name")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class PositionFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionCreateForm
    success_url = reverse_lazy("tasks:position-list")
    template_name = "tasks/generic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Position"
        return context


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    template_name = "tasks/position_detail.html"


class PositionFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5
    queryset = TaskType.objects.annotate(tasks_count=Count("tasks")).order_by("name")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TaskTypeFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    success_url = reverse_lazy("tasks:task-type-list")
    template_name = "tasks/generic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Task Type"
        return context


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    template_name = "tasks/task_type_detail.html"
    context_object_name = "task_type"
    paginate_by = 5


class TaskTypeFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "tasks/task_list.html"
    paginate_by = 5
    queryset = Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TaskFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks:task-list")
    template_name = "tasks/generic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Task Type"
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    paginate_by = 5
    queryset = Task.objects.prefetch_related("assignees")


class TaskFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/generic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Task"
        return context

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.pk})


class TaskFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "tasks/worker_list.html"
    paginate_by = 8
    queryset = Worker.objects.select_related("position")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "tasks/worker_detail.html"


class WorkerFormatCreateView(generic.CreateView):
    model = Worker
    template_name = "tasks/worker_form.html"
    form_class = WorkerCreateForm
    success_url = reverse_lazy("tasks:welcome")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "You have signed up successfully.")
        return response


class WorkerFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "tasks/generic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Profile"
        return context

    def get_success_url(self):
        return reverse_lazy("tasks:worker-detail", kwargs={"pk": self.object.pk})


class WorkerFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:worker-create")

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("tasks:worker-list")
        return reverse_lazy("tasks:worker-create")


def upload_avatar(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            return redirect("tasks:worker-detail", pk=pk)
    else:
        form = AvatarForm(instance=worker)
    return render(request, "tasks/upload_avatar.html", {"form": form})


class AssignOrRemoveWorkerView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        user = request.user
        if task.assignees.filter(pk=user.pk).exists():
            task.assignees.remove(user)
        else:
            task.assignees.add(user)
        return redirect("tasks:task-detail", pk=pk)


class CommentListView(LoginRequiredMixin, generic.ListView):
    model = Commentary
    template_name = "tasks/comment_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Commentary.objects.filter(task_id=self.kwargs["pk"]).order_by(
            "-created_time"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentaryForm()
        context["task"] = get_object_or_404(
            Task.objects.annotate(comment_count=Count("commentary")),
            pk=self.kwargs["pk"],
        )
        return context

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        form = CommentaryForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = self.request.user
            new_comment.task = task
            new_comment.save()
        return redirect("tasks:comment-list", pk=task.pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Commentary, pk=pk)
    if request.user != comment.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    comment.delete()
    return redirect("tasks:comment-list", pk=comment.task.pk)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            self.request.session.set_expiry(1209600)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

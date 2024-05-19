from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model
from tasks.models import Worker, Commentary, Task, TaskType, Position


class WorkerCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
            "avatar",
        )
        help_texts = {
            "username": None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("avatar",)


class WorkerUpdateForm(UserChangeForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position", "avatar")
        help_texts = {
            "username": None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class TaskTypeCreateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["class"] += " mb-3"


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "assignees": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "assignees":
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["class"] += " mb-3"
        self.fields["is_completed"].widget.attrs["class"] = "form-check-input"


class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["class"] += " mb-3"


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by username",
                "aria-label": "Search",
            }
        ),
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by name",
                "aria-label": "Search",
            }
        ),
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by name",
                "aria-label": "Search",
            }
        ),
    )


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by name",
                "aria-label": "Search",
            }
        ),
    )


class CommentaryForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["content"]
        labels = {
            "content": "",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "style": "width: 100%; "
                    "border-radius: 8px; "
                    "border: 1px solid #ccc; "
                    "padding: 10px;",
                }
            ),
        }


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

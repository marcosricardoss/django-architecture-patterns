from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "deadline_at",
            "finished_at"
        ]

    title = forms.CharField(
        label='Task Title',
        widget=forms.TextInput(
            attrs={
                "placeholder": "The Task Title"
            }
        )
    )
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "class-name-1 class-name-1",
                "id": "id-for-textarea",
                "rows": 4,
                "cols": 25,
                "placeholder": "The Task Description"
            }
        )
    )

    deadline_at = forms.DateTimeField(
        # format of datetime-local: yyyy-MM-ddThh:mm
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Deadline',
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    finished_at = forms.DateTimeField(
        required=False,
        # format of datetime-local: yyyy-MM-ddThh:mm
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Finished',
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    # def clean_deadline_at(self, *args, **kwargs):
    #     """ Example of validate method.
    # 
    #     Evaluating if the deadline datetime is greater than current time 
    #     """
    #
    #     deadline_at = self.cleaned_data.get("deadline_at")
    #     if not self.instance.pk:
    #         if deadline_at <= timezone.now():
    #             raise forms.ValidationError(
    #                 "This is not a valid deadline time.")
    #     return deadline_at


class RawTaskForm(forms.Form):
    title = forms.CharField(
        label='Task Title',
        widget=forms.TextInput(
            attrs={
                "placeholder": "The Task Title"
            }
        )
    )

    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "class-name-1 class-name-1",
                "id": "id-for-textarea",
                "rows": 4,
                "cols": 25,
                "placeholder": "The Task Description"
            }
        )
    )

    deadline_at = forms.DateTimeField(
        # format of datetime-local: yyyy-MM-ddThh:mm
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Deadline',
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    finished_at = forms.DateTimeField(
        required=False,
        # format of datetime-local: yyyy-MM-ddThh:mm
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Finished',
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    # def clean_deadline_at(self, *args, **kwargs):
    #     """ Example of validate method.
    # 
    #     Evaluating if the deadline datetime is greater than current time 
    #     """
    #
    #     deadline_at = self.cleaned_data.get("deadline_at")
    #     if not self.instance.pk:
    #         if deadline_at <= timezone.now():
    #             raise forms.ValidationError(
    #                 "This is not a valid deadline time.")
    #     return deadline_at

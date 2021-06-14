from datetime import datetime

from django import forms
from django.utils import timezone
timezone.make_aware

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title", 
            "description", 
            "deadline_at"
        ]

    title = forms.CharField(
        label='Task Title',
        widget=forms.TextInput(
            attrs= {
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
        label='Deadline',
        # TODO: Use the django timezone
        widget=forms.DateInput()
    )

    def clean_deadline_at(self, *args, **kwargs):
        """ Example of validate method """
        
        deadline_at = self.cleaned_data.get("deadline_at")        
        if deadline_at <= timezone.now():
            raise forms.ValidationError("This is not a valid deadline time.")   
        return deadline_at

class RawTaskForm(forms.Form):    
    title = forms.CharField(
        label='Task Title',
        widget=forms.TextInput(
            attrs= {
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
        label='Deadline',
        # TODO: Use the django timezone
        widget=forms.DateInput()
    )

    def clean_deadline_at(self, *args, **kwargs):
        """ Example of validate method """
        
        deadline_at = self.cleaned_data.get("deadline_at")        
        if deadline_at <= timezone.now():
            raise forms.ValidationError("This is not a valid deadline time.")   
        return deadline_at
    
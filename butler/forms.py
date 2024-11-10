from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task,employee,project
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True,help_text='Required. Provide a valid username.')
    email = forms.EmailField(required=True, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class TaskForm(forms.ModelForm):
    assignedEmployee = forms.ModelChoiceField(
        queryset=employee.objects.all(),
        label="Assigned Employee",
        empty_label = "Select Emplyoee",
    )
    project = forms.ModelChoiceField(
        queryset = project.objects.all(),
        label="project",
        empty_label="Select Project",
    )
    class Meta:
        model = Task
        fields = {'taskName', 'isCompleted', 'assignedEmployee', 'project'}
        widgets = {
            'taskName':forms.TextInput(attrs={'placeholder':'Enter task name'}),
            'isCompleted':forms.CheckboxInput(),
        }

class EmpForm(forms.ModelForm):
    class Meta:
        model = employee
        fields={'empName','empDesignation'}

class ProjectForm(forms.ModelForm):
    projectLead = forms.ModelChoiceField(
        queryset = employee.objects.all(),
        label="Project Lead",
        empty_label="Select Project Lead"
    )

    class Meta:
        model = project
        fields = {'projectName','projectProgress','projectDomain','projectLead'}

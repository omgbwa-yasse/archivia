from django import forms
from .models import Project, ProjectMember, ProjectTask, ProjectResource, TaskDependency, TaskComment, TimeEntry, Milestone
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'owner', 'status', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(is_active=True)
        self.fields['end_date'].required = False

class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['user', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_active=True)

class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = [
            'project', 'parent_task', 'title', 'description', 'status',
            'priority', 'estimated_hours', 'start_date', 'due_date', 'assigned_to'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'estimated_hours': forms.NumberInput(attrs={'step': '0.5', 'min': '0.5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
        self.fields['parent_task'].required = False
        self.fields['start_date'].required = False
        self.fields['due_date'].required = False
        self.fields['estimated_hours'].required = False

class ProjectResourceForm(forms.ModelForm):
    class Meta:
        model = ProjectResource
        fields = [
            'project', 'resource_type', 'user', 'name', 'description',
            'quantity', 'unit_cost', 'start_date', 'end_date'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'unit_cost': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_active=True)
        self.fields['user'].required = False
        self.fields['quantity'].required = False
        self.fields['unit_cost'].required = False
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False

class TaskDependencyForm(forms.ModelForm):
    class Meta:
        model = TaskDependency
        fields = ['task', 'depends_on_task', 'dependency_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['task'].disabled = True
            self.fields['depends_on_task'].queryset = ProjectTask.objects.exclude(id=self.instance.task.id)

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['task', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['task'].disabled = True

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['task', 'user', 'hours_spent', 'work_date', 'description']
        widgets = {
            'work_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'hours_spent': forms.NumberInput(attrs={'step': '0.5', 'min': '0.5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_active=True)
        if self.instance.pk:
            self.fields['task'].disabled = True
            self.fields['user'].disabled = True

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['project', 'title', 'description', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['project'].disabled = True 
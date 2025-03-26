from django import forms
from .models import Task, WorkflowDefinition, WorkflowInstance

class WorkflowDefinitionForm(forms.ModelForm):
    class Meta:
        model = WorkflowDefinition
        fields = ['name', 'description', 'bpmn_xml', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'bpmn_xml': forms.Textarea(attrs={'rows': 8, 'class': 'bpmn-editor'}),
        }

class WorkflowInstanceForm(forms.ModelForm):
    class Meta:
        model = WorkflowInstance
        fields = ['definition', 'name', 'status']
        widgets = {
            'current_state': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['definition'].queryset = WorkflowDefinition.objects.filter(status='active')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'workflow_instance', 'due_date', 'priority', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control' 
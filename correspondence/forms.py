from django import forms
from .models import Correspondence, Batch, CorrespondenceFolder, CorrespondenceTemplate

class CorrespondenceForm(forms.ModelForm):
    class Meta:
        model = Correspondence
        fields = ['code', 'name', 'date', 'description', 'document_type', 'status', 
                 'priority', 'typology', 'action', 'recipient_user', 'recipient_organisation']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['code', 'name', 'organisation_holder']

class CorrespondenceFolderForm(forms.ModelForm):
    class Meta:
        model = CorrespondenceFolder
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CorrespondenceTemplateForm(forms.ModelForm):
    class Meta:
        model = CorrespondenceTemplate
        fields = ['name', 'description', 'content']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10}),
        } 
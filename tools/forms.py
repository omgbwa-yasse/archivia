from django import forms
from .models import Communicability, Activity, Sort, Retention, LawType, Law, LawArticle, Organisation, OrganisationActivity, RetentionLawArticle

class CommunicabilityForm(forms.ModelForm):
    class Meta:
        model = Communicability
        fields = ['code', 'name', 'duration', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['code', 'name', 'parent', 'communicability', 'observation']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'communicability': forms.Select(attrs={'class': 'form-control'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class SortForm(forms.ModelForm):
    class Meta:
        model = Sort
        fields = ['code', 'name', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class RetentionForm(forms.ModelForm):
    class Meta:
        model = Retention
        fields = ['code', 'name', 'duration', 'sort']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'sort': forms.Select(attrs={'class': 'form-control'}),
        }

class LawTypeForm(forms.ModelForm):
    class Meta:
        model = LawType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class LawForm(forms.ModelForm):
    class Meta:
        model = Law
        fields = ['code', 'name', 'description', 'publish_date', 'law_type']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'law_type': forms.Select(attrs={'class': 'form-control'}),
        }

class LawArticleForm(forms.ModelForm):
    class Meta:
        model = LawArticle
        fields = ['code', 'name', 'description', 'law']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'law': forms.Select(attrs={'class': 'form-control'}),
        }

class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ['code', 'name', 'description', 'parent']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

class OrganisationActivityForm(forms.ModelForm):
    class Meta:
        model = OrganisationActivity
        fields = ['organisation', 'activity']
        widgets = {
            'organisation': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
        }

class RetentionLawArticleForm(forms.ModelForm):
    class Meta:
        model = RetentionLawArticle
        fields = ['retention', 'law_article']
        widgets = {
            'retention': forms.Select(attrs={'class': 'form-control'}),
            'law_article': forms.Select(attrs={'class': 'form-control'}),
        } 
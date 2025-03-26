from django import forms
from django.contrib.auth import get_user_model
from .models import Email, EmailTemplate, EmailAttachment, Folder, Contact, ContactGroup
from .widgets import MultipleFileInput

User = get_user_model()

class EmailForm(forms.ModelForm):
    attachments = forms.FileField(
        required=False,
        widget=MultipleFileInput(),
        label="Pièces jointes"
    )
    
    class Meta:
        model = Email
        fields = ['subject', 'body_html', 'body_text', 'recipients', 'cc', 'bcc', 'template']
        widgets = {
            'body_html': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'body_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'cc': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'bcc': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'template': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipients'].queryset = User.objects.all()
        self.fields['cc'].queryset = User.objects.all()
        self.fields['bcc'].queryset = User.objects.all()

class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body_html', 'body_text', 'variables', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body_html': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'body_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'variables': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body_text'].required = False
        self.fields['variables'].required = False
        self.fields['category'].required = False
        self.fields['is_system'].disabled = True  # Les templates système ne peuvent pas être modifiés 

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'description', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'groups']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class ContactGroupForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 
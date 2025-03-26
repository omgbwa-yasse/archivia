from django import forms
from .models import Email, EmailTemplate, EmailAttachment
from .widgets import MultipleFileInput

class EmailForm(forms.ModelForm):
    attachments = forms.FileField(
        required=False,
        widget=MultipleFileInput(),
        label="Pièces jointes"
    )
    
    class Meta:
        model = Email
        fields = [
            'recipient_email',
            'recipient_name',
            'cc',
            'bcc',
            'subject',
            'body_html',
            'body_text',
            'priority',
            'template',
            'related_entity_type',
            'related_entity_id',
        ]
        widgets = {
            'cc': forms.Textarea(attrs={'rows': 1}),
            'bcc': forms.Textarea(attrs={'rows': 1}),
            'body_html': forms.Textarea(attrs={'class': 'editor'}),
            'body_text': forms.Textarea(attrs={'rows': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body_text'].required = False
        self.fields['cc'].required = False
        self.fields['bcc'].required = False
        self.fields['related_entity_type'].required = False
        self.fields['related_entity_id'].required = False

class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = [
            'name',
            'subject',
            'body_html',
            'body_text',
            'variables',
            'category',
            'is_system',
        ]
        widgets = {
            'body_html': forms.Textarea(attrs={'class': 'editor'}),
            'body_text': forms.Textarea(attrs={'rows': 10}),
            'variables': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body_text'].required = False
        self.fields['variables'].required = False
        self.fields['category'].required = False
        self.fields['is_system'].disabled = True  # Les templates système ne peuvent pas être modifiés 
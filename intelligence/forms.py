from django import forms
from .models import (
    AIAgent, AIModel, AIPrompt, AIChat,
    AITool, AITask, AIReferenceData
)

class AIAgentForm(forms.ModelForm):
    class Meta:
        model = AIAgent
        fields = ['name', 'description', 'type', 'configuration', 'system_prompt', 'capabilities', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'system_prompt': forms.Textarea(attrs={'rows': 8}),
            'configuration': forms.Textarea(attrs={'rows': 4}),
            'capabilities': forms.Textarea(attrs={'rows': 4}),
        }

class AIModelForm(forms.ModelForm):
    class Meta:
        model = AIModel
        fields = ['name', 'description', 'provider', 'model_id', 'version', 'status', 'capabilities']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'capabilities': forms.Textarea(attrs={'rows': 4}),
        }

class AIPromptForm(forms.ModelForm):
    class Meta:
        model = AIPrompt
        fields = ['name', 'description', 'content', 'variables']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'content': forms.Textarea(attrs={'rows': 8}),
            'variables': forms.Textarea(attrs={'rows': 4}),
        }

class AIChatForm(forms.ModelForm):
    class Meta:
        model = AIChat
        fields = ['title', 'description', 'ai_agent', 'chat_settings', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'chat_settings': forms.Textarea(attrs={'rows': 4}),
        }

class AIToolForm(forms.ModelForm):
    class Meta:
        model = AITool
        fields = ['name', 'description', 'type', 'capabilities', 'configuration', 'api_endpoint', 'version', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'capabilities': forms.Textarea(attrs={'rows': 4}),
            'configuration': forms.Textarea(attrs={'rows': 4}),
        }

class AITaskForm(forms.ModelForm):
    class Meta:
        model = AITask
        fields = ['name', 'description', 'agent', 'model', 'priority', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AIReferenceDataForm(forms.ModelForm):
    class Meta:
        model = AIReferenceData
        fields = ['ai_agent', 'usage'] 
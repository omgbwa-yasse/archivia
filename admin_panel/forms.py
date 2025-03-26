from django import forms
from .models import (
    LDAPConfig, LDAPUserMapping, LDAPGroupMapping,
    BackupConfig
)

class LDAPConfigForm(forms.ModelForm):
    class Meta:
        model = LDAPConfig
        fields = ['name', 'host', 'port', 'bind_dn', 'bind_password', 'base_dn', 'active']
        widgets = {
            'bind_password': forms.PasswordInput(render_value=True),
        }

class LDAPUserMappingForm(forms.ModelForm):
    class Meta:
        model = LDAPUserMapping
        fields = ['ldap_attribute', 'application_field']

class LDAPGroupMappingForm(forms.ModelForm):
    class Meta:
        model = LDAPGroupMapping
        fields = ['ldap_group_dn', 'application_group']

class BackupConfigForm(forms.ModelForm):
    class Meta:
        model = BackupConfig
        fields = ['name', 'description', 'backup_type', 'schedule_type', 'schedule_day', 
                 'schedule_time', 'retention_count', 'storage_path', 'active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'schedule_time': forms.TimeInput(attrs={'type': 'time'}),
        } 
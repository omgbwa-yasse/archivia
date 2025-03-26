from django import forms
from .models import (
    LDAPConfig, LDAPUserMapping, LDAPGroupMapping,
    BackupConfig
)

class LDAPConfigForm(forms.ModelForm):
    class Meta:
        model = LDAPConfig
        fields = [
            'name', 'description', 'server_url', 'port', 'use_ssl',
            'bind_dn', 'bind_password', 'search_base', 'user_search_filter',
            'group_search_filter', 'user_id_attribute', 'user_email_attribute',
            'user_display_name_attribute', 'group_id_attribute', 'group_member_attribute',
            'enabled', 'connection_timeout'
        ]
        widgets = {
            'bind_password': forms.PasswordInput(render_value=True),
            'description': forms.Textarea(attrs={'rows': 3}),
            'user_search_filter': forms.Textarea(attrs={'rows': 2}),
            'group_search_filter': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('use_ssl') and cleaned_data.get('port') == 389:
            self.add_error('port', 'SSL requires port 636')
        return cleaned_data

class LDAPUserMappingForm(forms.ModelForm):
    class Meta:
        model = LDAPUserMapping
        fields = ['ldap_user_id', 'local_user']
        widgets = {
            'ldap_user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'local_user': forms.Select(attrs={'class': 'form-control'}),
        }

class LDAPGroupMappingForm(forms.ModelForm):
    class Meta:
        model = LDAPGroupMapping
        fields = ['ldap_group_id', 'local_group']
        widgets = {
            'ldap_group_id': forms.TextInput(attrs={'class': 'form-control'}),
            'local_group': forms.Select(attrs={'class': 'form-control'}),
        }

class BackupConfigForm(forms.ModelForm):
    class Meta:
        model = BackupConfig
        fields = [
            'name', 'description', 'storage_type', 'storage_path',
            'retention_days', 'max_backups', 'include_files', 'include_database',
            'compression_type', 'encryption_enabled', 'encryption_key',
            'schedule_type', 'schedule_time', 'schedule_day', 'enabled'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'encryption_key': forms.PasswordInput(render_value=True),
            'schedule_time': forms.TimeInput(attrs={'type': 'time'}),
            'schedule_day': forms.TextInput(attrs={'placeholder': 'e.g., MONDAY or 1-31'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        schedule_type = cleaned_data.get('schedule_type')
        schedule_day = cleaned_data.get('schedule_day')

        if schedule_type in ['WEEKLY', 'MONTHLY'] and not schedule_day:
            self.add_error('schedule_day', 'This field is required for weekly and monthly schedules')

        if schedule_type == 'WEEKLY' and schedule_day:
            valid_days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
            if schedule_day.upper() not in valid_days:
                self.add_error('schedule_day', 'Please enter a valid day of the week')

        if schedule_type == 'MONTHLY' and schedule_day:
            try:
                day = int(schedule_day)
                if not 1 <= day <= 31:
                    self.add_error('schedule_day', 'Please enter a valid day of the month (1-31)')
            except ValueError:
                self.add_error('schedule_day', 'Please enter a valid number for the day of the month')

        return cleaned_data 
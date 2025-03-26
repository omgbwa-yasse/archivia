from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import (
    LDAPConfig, LDAPUserMapping, LDAPGroupMapping, LDAPSyncLog,
    BackupConfig, BackupLog, RestoreLog
)
from .forms import (
    LDAPConfigForm, BackupConfigForm,
    LDAPUserMappingForm, LDAPGroupMappingForm
)

# LDAP Views
class LDAPConfigListView(LoginRequiredMixin, ListView):
    model = LDAPConfig
    template_name = 'settings/ldap_config_list.html'
    context_object_name = 'ldap_configs'
    ordering = ['-created_at']

class LDAPConfigDetailView(LoginRequiredMixin, DetailView):
    model = LDAPConfig
    template_name = 'settings/ldap_config_detail.html'
    context_object_name = 'ldap_config'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_mappings'] = self.object.user_mappings.all()
        context['group_mappings'] = self.object.group_mappings.all()
        context['sync_logs'] = self.object.sync_logs.all().order_by('-start_time')[:10]
        return context

class LDAPConfigCreateView(LoginRequiredMixin, CreateView):
    model = LDAPConfig
    form_class = LDAPConfigForm
    template_name = 'settings/ldap_config_form.html'
    success_url = reverse_lazy('settings:ldap_config_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class LDAPConfigUpdateView(LoginRequiredMixin, UpdateView):
    model = LDAPConfig
    form_class = LDAPConfigForm
    template_name = 'settings/ldap_config_form.html'
    success_url = reverse_lazy('settings:ldap_config_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

@login_required
@require_POST
def ldap_sync(request, pk):
    ldap_config = get_object_or_404(LDAPConfig, pk=pk)
    sync_type = request.POST.get('sync_type', 'ALL')
    
    try:
        # TODO: Implement actual LDAP sync logic here
        sync_log = LDAPSyncLog.objects.create(
            ldap_config=ldap_config,
            sync_type=sync_type,
            created_by=request.user
        )
        messages.success(request, f'LDAP sync started for {ldap_config.name}')
    except Exception as e:
        messages.error(request, f'Failed to start LDAP sync: {str(e)}')
    
    return redirect('settings:ldap_config_detail', pk=pk)

# Backup Views
class BackupConfigListView(LoginRequiredMixin, ListView):
    model = BackupConfig
    template_name = 'settings/backup_config_list.html'
    context_object_name = 'backup_configs'
    ordering = ['-created_at']

class BackupConfigDetailView(LoginRequiredMixin, DetailView):
    model = BackupConfig
    template_name = 'settings/backup_config_detail.html'
    context_object_name = 'backup_config'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['backup_logs'] = self.object.backup_logs.all().order_by('-start_time')[:10]
        return context

class BackupConfigCreateView(LoginRequiredMixin, CreateView):
    model = BackupConfig
    form_class = BackupConfigForm
    template_name = 'settings/backup_config_form.html'
    success_url = reverse_lazy('settings:backup_config_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class BackupConfigUpdateView(LoginRequiredMixin, UpdateView):
    model = BackupConfig
    form_class = BackupConfigForm
    template_name = 'settings/backup_config_form.html'
    success_url = reverse_lazy('settings:backup_config_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

@login_required
@require_POST
def start_backup(request, pk):
    backup_config = get_object_or_404(BackupConfig, pk=pk)
    
    try:
        # TODO: Implement actual backup logic here
        backup_log = BackupLog.objects.create(
            backup_config=backup_config,
            filename=f"backup_{backup_config.name}_{backup_config.id}.zip",
            created_by=request.user,
            initiated_by=request.user.username
        )
        messages.success(request, f'Backup started for {backup_config.name}')
    except Exception as e:
        messages.error(request, f'Failed to start backup: {str(e)}')
    
    return redirect('settings:backup_config_detail', pk=pk)

@login_required
@require_POST
def restore_backup(request, backup_log_id):
    backup_log = get_object_or_404(BackupLog, id=backup_log_id)
    
    try:
        # TODO: Implement actual restore logic here
        restore_log = RestoreLog.objects.create(
            backup_log=backup_log,
            restore_type=request.POST.get('restore_type', 'FULL'),
            created_by=request.user
        )
        messages.success(request, f'Restore started for backup {backup_log.filename}')
    except Exception as e:
        messages.error(request, f'Failed to start restore: {str(e)}')
    
    return redirect('settings:backup_config_detail', pk=backup_log.backup_config.pk)

# API Views for status updates
@login_required
def backup_status(request, backup_log_id):
    backup_log = get_object_or_404(BackupLog, id=backup_log_id)
    return JsonResponse({
        'status': backup_log.status,
        'progress': {
            'total': backup_log.total_items,
            'processed': backup_log.items_processed,
            'created': backup_log.items_created,
            'updated': backup_log.items_updated,
            'deleted': backup_log.items_deleted,
            'failed': backup_log.items_failed
        }
    })

@login_required
def restore_status(request, restore_log_id):
    restore_log = get_object_or_404(RestoreLog, id=restore_log_id)
    return JsonResponse({
        'status': restore_log.status,
        'restored_items': restore_log.restored_items
    }) 
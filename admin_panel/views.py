from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import (
    LDAPConfig, LDAPUserMapping, LDAPGroupMapping, LDAPSyncLog,
    BackupConfig, BackupLog, RestoreLog
)
from .forms import (
    LDAPConfigForm, BackupConfigForm,
    LDAPUserMappingForm, LDAPGroupMappingForm
)

# LDAP Configuration Views
@login_required
def ldap_config_list(request):
    ldap_configs = LDAPConfig.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/ldap_config_list.html', {
        'ldap_configs': ldap_configs
    })

@login_required
def ldap_config_detail(request, pk):
    ldap_config = get_object_or_404(LDAPConfig, pk=pk)
    user_mappings = ldap_config.user_mappings.all()
    group_mappings = ldap_config.group_mappings.all()
    sync_logs = ldap_config.sync_logs.all().order_by('-start_time')[:10]
    
    return render(request, 'admin_panel/ldap_config_detail.html', {
        'ldap_config': ldap_config,
        'user_mappings': user_mappings,
        'group_mappings': group_mappings,
        'sync_logs': sync_logs
    })

@login_required
def ldap_config_create(request):
    if request.method == 'POST':
        form = LDAPConfigForm(request.POST)
        if form.is_valid():
            ldap_config = form.save(commit=False)
            ldap_config.created_by = request.user
            ldap_config.save()
            messages.success(request, 'LDAP configuration created successfully.')
            return redirect('settings:ldap_config_detail', pk=ldap_config.pk)
    else:
        form = LDAPConfigForm()
    
    return render(request, 'admin_panel/ldap_config_form.html', {
        'form': form,
        'title': 'Create LDAP Configuration'
    })

@login_required
def ldap_config_edit(request, pk):
    ldap_config = get_object_or_404(LDAPConfig, pk=pk)
    
    if request.method == 'POST':
        form = LDAPConfigForm(request.POST, instance=ldap_config)
        if form.is_valid():
            ldap_config = form.save(commit=False)
            ldap_config.updated_by = request.user
            ldap_config.save()
            messages.success(request, 'LDAP configuration updated successfully.')
            return redirect('settings:ldap_config_detail', pk=ldap_config.pk)
    else:
        form = LDAPConfigForm(instance=ldap_config)
    
    return render(request, 'admin_panel/ldap_config_form.html', {
        'form': form,
        'ldap_config': ldap_config,
        'title': 'Edit LDAP Configuration'
    })

@login_required
@require_POST
def ldap_sync(request, pk):
    ldap_config = get_object_or_404(LDAPConfig, pk=pk)
    sync_type = request.POST.get('sync_type', 'ALL')
    
    try:
        # Simulate LDAP sync for now
        sync_log = LDAPSyncLog.objects.create(
            ldap_config=ldap_config,
            sync_type=sync_type,
            status='COMPLETED',
            end_time=timezone.now(),
            users_created=5,
            users_updated=3,
            created_by=request.user
        )
        messages.success(request, f'LDAP sync completed for {ldap_config.name}')
    except Exception as e:
        messages.error(request, f'Failed to start LDAP sync: {str(e)}')
    
    return redirect('settings:ldap_config_detail', pk=pk)

# Backup Configuration Views
@login_required
def backup_config_list(request):
    backup_configs = BackupConfig.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/backup_config_list.html', {
        'backup_configs': backup_configs
    })

@login_required
def backup_config_detail(request, pk):
    backup_config = get_object_or_404(BackupConfig, pk=pk)
    backup_logs = backup_config.backup_logs.all().order_by('-start_time')[:10]
    
    return render(request, 'admin_panel/backup_config_detail.html', {
        'backup_config': backup_config,
        'backup_logs': backup_logs
    })

@login_required
def backup_config_create(request):
    if request.method == 'POST':
        form = BackupConfigForm(request.POST)
        if form.is_valid():
            backup_config = form.save(commit=False)
            backup_config.created_by = request.user
            backup_config.save()
            messages.success(request, 'Backup configuration created successfully.')
            return redirect('settings:backup_config_detail', pk=backup_config.pk)
    else:
        form = BackupConfigForm()
    
    return render(request, 'admin_panel/backup_config_form.html', {
        'form': form,
        'title': 'Create Backup Configuration'
    })

@login_required
def backup_config_edit(request, pk):
    backup_config = get_object_or_404(BackupConfig, pk=pk)
    
    if request.method == 'POST':
        form = BackupConfigForm(request.POST, instance=backup_config)
        if form.is_valid():
            backup_config = form.save(commit=False)
            backup_config.updated_by = request.user
            backup_config.save()
            messages.success(request, 'Backup configuration updated successfully.')
            return redirect('settings:backup_config_detail', pk=backup_config.pk)
    else:
        form = BackupConfigForm(instance=backup_config)
    
    return render(request, 'admin_panel/backup_config_form.html', {
        'form': form,
        'backup_config': backup_config,
        'title': 'Edit Backup Configuration'
    })

@login_required
@require_POST
def backup_start(request, pk):
    backup_config = get_object_or_404(BackupConfig, pk=pk)
    
    try:
        # Simulate backup for now
        backup_log = BackupLog.objects.create(
            backup_config=backup_config,
            filename=f"backup_{backup_config.name}_{backup_config.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.zip",
            status='COMPLETED',
            end_time=timezone.now(),
            total_items=100,
            items_processed=100,
            items_created=80,
            items_updated=20,
            file_size=1024 * 1024 * 5,  # 5MB
            initiated_by=request.user.username,
            created_by=request.user
        )
        messages.success(request, f'Backup completed for {backup_config.name}')
    except Exception as e:
        messages.error(request, f'Failed to start backup: {str(e)}')
    
    return redirect('settings:backup_config_detail', pk=pk)

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
@require_POST
def restore_backup(request, backup_log_id):
    backup_log = get_object_or_404(BackupLog, id=backup_log_id)
    
    try:
        # Simulate restore for now
        restore_log = RestoreLog.objects.create(
            backup_log=backup_log,
            restore_type=request.POST.get('restore_type', 'FULL'),
            status='COMPLETED',
            end_time=timezone.now(),
            restored_items=50,
            created_by=request.user
        )
        messages.success(request, f'Restore completed for backup {backup_log.filename}')
    except Exception as e:
        messages.error(request, f'Failed to start restore: {str(e)}')
    
    return redirect('settings:backup_config_detail', pk=backup_log.backup_config.pk)

@login_required
def restore_status(request, restore_log_id):
    restore_log = get_object_or_404(RestoreLog, id=restore_log_id)
    return JsonResponse({
        'status': restore_log.status,
        'restored_items': restore_log.restored_items
    }) 
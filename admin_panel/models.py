from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LDAPConfig(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=389)
    bind_dn = models.CharField(max_length=255)
    bind_password = models.CharField(max_length=255)
    base_dn = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_ldap_configs")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_ldap_configs")

    def __str__(self):
        return self.name

class LDAPUserMapping(models.Model):
    ldap_config = models.ForeignKey(LDAPConfig, on_delete=models.CASCADE, related_name="user_mappings")
    ldap_attribute = models.CharField(max_length=100)
    application_field = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ldap_attribute} -> {self.application_field}"

class LDAPGroupMapping(models.Model):
    ldap_config = models.ForeignKey(LDAPConfig, on_delete=models.CASCADE, related_name="group_mappings")
    ldap_group_dn = models.CharField(max_length=255)
    application_group = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ldap_group_dn} -> {self.application_group}"

class LDAPSyncLog(models.Model):
    SYNC_TYPES = (
        ('ALL', 'All'),
        ('USERS', 'Users only'),
        ('GROUPS', 'Groups only'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    
    ldap_config = models.ForeignKey(LDAPConfig, on_delete=models.CASCADE, related_name="sync_logs")
    sync_type = models.CharField(max_length=10, choices=SYNC_TYPES, default='ALL')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    users_created = models.IntegerField(default=0)
    users_updated = models.IntegerField(default=0)
    users_disabled = models.IntegerField(default=0)
    groups_created = models.IntegerField(default=0)
    groups_updated = models.IntegerField(default=0)
    groups_deleted = models.IntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.ldap_config.name} - {self.get_sync_type_display()} - {self.start_time}"

class BackupConfig(models.Model):
    BACKUP_TYPES = (
        ('FULL', 'Full backup'),
        ('INCREMENTAL', 'Incremental backup'),
    )
    
    SCHEDULE_TYPES = (
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('MANUAL', 'Manual only'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    backup_type = models.CharField(max_length=15, choices=BACKUP_TYPES, default='FULL')
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_TYPES, default='MANUAL')
    schedule_day = models.IntegerField(null=True, blank=True, help_text="Day of week (1-7) or day of month (1-31)")
    schedule_time = models.TimeField(null=True, blank=True)
    retention_count = models.IntegerField(default=5)
    storage_path = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_backup_configs")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_backup_configs")

    def __str__(self):
        return self.name

class BackupLog(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    
    backup_config = models.ForeignKey(BackupConfig, on_delete=models.CASCADE, related_name="backup_logs")
    filename = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_items = models.IntegerField(default=0)
    items_processed = models.IntegerField(default=0)
    items_created = models.IntegerField(default=0)
    items_updated = models.IntegerField(default=0)
    items_deleted = models.IntegerField(default=0)
    items_failed = models.IntegerField(default=0)
    file_size = models.BigIntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    initiated_by = models.CharField(max_length=100, help_text="Username or 'system'")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.backup_config.name} - {self.start_time}"

class RestoreLog(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    
    RESTORE_TYPES = (
        ('FULL', 'Full restore'),
        ('SELECTIVE', 'Selective restore'),
    )
    
    backup_log = models.ForeignKey(BackupLog, on_delete=models.CASCADE, related_name="restore_logs")
    restore_type = models.CharField(max_length=10, choices=RESTORE_TYPES, default='FULL')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    restored_items = models.IntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Restore of {self.backup_log.filename} - {self.start_time}" 
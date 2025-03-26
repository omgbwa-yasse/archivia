from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class LDAPConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    server_url = models.CharField(max_length=255)
    port = models.IntegerField(default=389)
    use_ssl = models.BooleanField(default=False)
    bind_dn = models.CharField(max_length=255, blank=True)
    bind_password = models.CharField(max_length=255, blank=True)
    search_base = models.CharField(max_length=255)
    user_search_filter = models.CharField(max_length=255)
    group_search_filter = models.CharField(max_length=255, blank=True)
    user_id_attribute = models.CharField(max_length=50, default='uid')
    user_email_attribute = models.CharField(max_length=50, default='mail')
    user_display_name_attribute = models.CharField(max_length=50, default='cn')
    group_id_attribute = models.CharField(max_length=50, default='cn')
    group_member_attribute = models.CharField(max_length=50, default='member')
    enabled = models.BooleanField(default=False)
    connection_timeout = models.IntegerField(
        default=5000,
        validators=[MinValueValidator(1000), MaxValueValidator(30000)]
    )
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_ldap_configs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_ldap_configs', null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'LDAP Configuration'
        verbose_name_plural = 'LDAP Configurations'

    def __str__(self):
        return self.name

class LDAPUserMapping(models.Model):
    ldap_config = models.ForeignKey(LDAPConfig, on_delete=models.CASCADE, related_name='user_mappings')
    ldap_user_id = models.CharField(max_length=255)
    local_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ldap_mappings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sync_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = [['ldap_config', 'ldap_user_id'], ['ldap_config', 'local_user']]
        verbose_name = 'LDAP User Mapping'
        verbose_name_plural = 'LDAP User Mappings'

    def __str__(self):
        return f"{self.ldap_user_id} -> {self.local_user.username}"

class LDAPGroupMapping(models.Model):
    ldap_config = models.ForeignKey(LDAPConfig, on_delete=models.CASCADE, related_name='group_mappings')
    ldap_group_id = models.CharField(max_length=255)
    local_group = models.ForeignKey('auth.Group', on_delete=models.CASCADE, related_name='ldap_mappings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sync_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = [['ldap_config', 'ldap_group_id'], ['ldap_config', 'local_group']]
        verbose_name = 'LDAP Group Mapping'
        verbose_name_plural = 'LDAP Group Mappings'

    def __str__(self):
        return f"{self.ldap_group_id} -> {self.local_group.name}"

class LDAPSyncLog(models.Model):
    SYNC_TYPES = [
        ('USERS', 'Users'),
        ('GROUPS', 'Groups'),
        ('ALL', 'All'),
    ]
    
    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    ldap_config = models.ForeignKey(LDAPConfig, on_delete=models.CASCADE, related_name='sync_logs')
    sync_type = models.CharField(max_length=10, choices=SYNC_TYPES)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RUNNING')
    total_items = models.IntegerField(default=0)
    items_processed = models.IntegerField(default=0)
    items_created = models.IntegerField(default=0)
    items_updated = models.IntegerField(default=0)
    items_deleted = models.IntegerField(default=0)
    items_failed = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'LDAP Sync Log'
        verbose_name_plural = 'LDAP Sync Logs'

    def __str__(self):
        return f"{self.ldap_config.name} - {self.sync_type} - {self.status}"

class BackupConfig(models.Model):
    STORAGE_TYPES = [
        ('LOCAL', 'Local Storage'),
        ('FTP', 'FTP'),
        ('SFTP', 'SFTP'),
        ('S3', 'Amazon S3'),
        ('CLOUD', 'Cloud Storage'),
    ]

    COMPRESSION_TYPES = [
        ('NONE', 'No Compression'),
        ('GZIP', 'Gzip'),
        ('ZIP', 'Zip'),
    ]

    SCHEDULE_TYPES = [
        ('MANUAL', 'Manual'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    storage_type = models.CharField(max_length=10, choices=STORAGE_TYPES)
    storage_path = models.CharField(max_length=255)
    retention_days = models.IntegerField(default=30)
    max_backups = models.IntegerField(null=True)
    include_files = models.BooleanField(default=True)
    include_database = models.BooleanField(default=True)
    compression_type = models.CharField(max_length=10, choices=COMPRESSION_TYPES, default='GZIP')
    encryption_enabled = models.BooleanField(default=False)
    encryption_key = models.CharField(max_length=255, blank=True)
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_TYPES, default='MANUAL')
    schedule_time = models.TimeField(default='00:00:00')
    schedule_day = models.CharField(max_length=20, blank=True)
    enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_backup_configs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_backup_configs', null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Backup Configuration'
        verbose_name_plural = 'Backup Configurations'

    def __str__(self):
        return self.name

class BackupLog(models.Model):
    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    TYPE_CHOICES = [
        ('FULL', 'Full Backup'),
        ('DATABASE', 'Database Only'),
        ('FILES', 'Files Only'),
    ]

    backup_config = models.ForeignKey(BackupConfig, on_delete=models.CASCADE, related_name='backup_logs')
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RUNNING')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='FULL')
    storage_path = models.CharField(max_length=255)
    error_message = models.TextField(blank=True)
    includes_database = models.BooleanField(default=True)
    includes_files = models.BooleanField(default=True)
    is_compressed = models.BooleanField(default=True)
    is_encrypted = models.BooleanField(default=False)
    checksum = models.CharField(max_length=64, blank=True)
    initiated_by = models.CharField(max_length=50, default='SYSTEM')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Backup Log'
        verbose_name_plural = 'Backup Logs'

    def __str__(self):
        return f"{self.backup_config.name} - {self.filename} - {self.status}"

class RestoreLog(models.Model):
    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    TYPE_CHOICES = [
        ('FULL', 'Full Restore'),
        ('DATABASE', 'Database Only'),
        ('FILES', 'Files Only'),
        ('PARTIAL', 'Partial Restore'),
    ]

    backup_log = models.ForeignKey(BackupLog, on_delete=models.CASCADE, related_name='restore_logs')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RUNNING')
    restore_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    restored_items = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Restore Log'
        verbose_name_plural = 'Restore Logs'

    def __str__(self):
        return f"Restore of {self.backup_log.filename} - {self.status}" 